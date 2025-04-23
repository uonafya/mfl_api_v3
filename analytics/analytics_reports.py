import itertools
import functools
from django.db.models import Q
import uuid

from datetime import timedelta
from collections import OrderedDict
from django.apps import apps
from django.db.models import Sum, Case, When, IntegerField, Count, ExpressionWrapper, Q, F
from django.utils import timezone
from django.core.paginator import Paginator

from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound, ValidationError

from facilities.models import (
    Facility,
    FacilityType,
    KephLevel,
    FacilityUpgrade, OwnerType, Owner, RegulatingBody, Service, FacilityInfrastructure, FacilityService, Infrastructure)
from common.constants import TRUTH_NESS, FALSE_NESS
from common.models import (
    County, Constituency, Ward, SubCounty
)
from chul.models import CommunityHealthUnit, Status, CHUService, CHUServiceLink
from mfl_gis.models import FacilityCoordinates

from .report_config import REPORTS
from collections import defaultdict


class FilterReportMixin(object):
    queryset = Facility.objects.all()
    row_comparison_options = {
        'county': {
            'name_field': 'ward__sub_county__county__name',
            'id_field': 'ward__sub_county__county',
            'filter_field': 'ward__sub_county__county__id'
        },
        'subcounty': {
            'name_field': 'ward__sub_county__name',
            'id_field': 'ward__sub_county',
            'filter_field': 'ward__sub_county__id'
        },
        'ward': {
            'name_field': 'ward__name',
            'id_field': 'ward',
            'filter_field': 'ward__id'
        }
    }
    allowed_col_dimensions = [
        'facility_type__name',
        'owner__name',
        'keph_level__name',
        'regulatory_body__name',
        'infrastructure',
        'services',
        'bed_types'
    ]
    allowed_metrics = ['number_of_facilities']  # Add more metrics if needed
    bed_type_mapping = {
        'number_of_beds': 'beds',
        'number_of_cots': 'cots',
        'number_of_maternity_beds': 'maternity_beds',
        'number_of_isolation_beds': 'isolation_beds',
        'number_of_emergency_casualty_beds': 'emergency_casualty_beds',
        'number_of_icu_beds': 'icu_beds',
        'number_of_hdu_beds': 'hdu_beds',
        'number_of_inpatient_beds': 'inpatient_beds'
    }

    def _prepare_filters(self, filtering_data):
        filtering_data = filtering_data.split('=')
        return filtering_data[0], filtering_data[1]

    def _build_dict_filter(self, filter_field_name, value):
        return {filter_field_name: value}

    def _filter_queryset(self, filter_dict):
        return self.queryset.filter(**filter_dict)

    def _filter_relation_obj(self, model, field_name, value):
        filter_dict = {field_name: value}
        return model.objects.filter(**filter_dict)

    def _filter_by_extra_params(self, report_config, more_filters_params, model):
        more_filters = self._prepare_filters(more_filters_params)
        requested_filters = report_config.get('extra_filters')[more_filters[0]]
        requested_filters_filter_field_name = requested_filters.get('filter_field_name')
        filtering_dict = self._build_dict_filter(requested_filters_filter_field_name, more_filters[1])
        self.queryset = self._filter_queryset(filtering_dict)
        model_instances = self._filter_relation_obj(model, more_filters[0], more_filters[1])
        return model_instances

    def _get_return_data(self, filter_field_name, model_instances, return_instance_name, return_count_name):
        data = []
        for instance in model_instances:
            filter_data = {filter_field_name: instance}
            count = self.queryset.filter(**filter_data).count()
            instance_name = instance.name
            data.append({
                return_instance_name: instance_name,
                return_count_name: count
            })
        return data

    def _get_matrix_report(self, filters={}):
        # Get query parameters
        row_comparison = self.request.query_params.get('row_comparison', 'county')
        col_dims = self.request.query_params.get('col_dims', 'facility_type__name,owner__name,keph_level__name').split(
            ',')
        metric = self.request.query_params.get('metric', 'number_of_facilities')
        infrastructure_category = self.request.query_params.get('infrastructure_category', None)
        service_category = self.request.query_params.get('service_category', None)

        # Validate parameters
        if row_comparison not in self.row_comparison_options:
            raise ValidationError(f"Invalid row_comparison. Choose from {list(self.row_comparison_options.keys())}")
        if not all(dim in self.allowed_col_dimensions for dim in col_dims):
            raise ValidationError(f"Invalid col_dims. Choose from {self.allowed_col_dimensions}")
        if metric not in self.allowed_metrics:
            raise ValidationError(f"Invalid metric. Choose from {self.allowed_metrics}")

        # Get row dimension fields
        row_config = self.row_comparison_options[row_comparison]
        row_name_field = row_config['name_field']
        row_id_field = row_config['id_field']

        # Initialize queryset
        base_queryset = self.queryset.filter(**filters).select_related(
            'facility_type', 'owner', 'keph_level', 'regulatory_body',
            'ward__sub_county__county'
        )

        # Prepare column dimensions and querysets
        col_fields = []
        headers = []
        for dim in col_dims:
            if dim == 'infrastructure':
                qs = FacilityInfrastructure.objects.filter(
                    facility__in=base_queryset
                ).select_related('infrastructure__category')
                if infrastructure_category:
                    qs = qs.filter(infrastructure__category__id=infrastructure_category)
                col_field = 'infrastructure__category__name'
                col_values = qs.values(col_field).distinct().order_by(col_field)
                headers.append([v[col_field] for v in col_values])
                col_fields.append(col_field)
            elif dim == 'services':
                qs = FacilityService.objects.filter(
                    facility__in=base_queryset
                ).select_related('service__category')
                if service_category:
                    qs = qs.filter(service__category__id=service_category)
                col_field = 'service__category__name'
                col_values = qs.values(col_field).distinct().order_by(col_field)
                headers.append([v[col_field] for v in col_values])
                col_fields.append(col_field)
            elif dim == 'bed_types':
                bed_types = list(self.bed_type_mapping.values())
                headers.append(bed_types)
                col_field = 'bed_type_label'
                col_fields.append(col_field)
            else:
                col_fields.append(dim)
                col_values = base_queryset.values(dim).distinct().order_by(dim)
                headers.append([v[dim] for v in col_values])

        # Aggregate data
        counts = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

        if 'infrastructure' in col_dims or 'services' in col_dims:
            if 'infrastructure' in col_dims:
                queryset = FacilityInfrastructure.objects.filter(
                    facility__in=base_queryset
                ).select_related('infrastructure__category', 'facility')
                if infrastructure_category:
                    queryset = queryset.filter(infrastructure__category__id=infrastructure_category)
                group_fields = ['facility__' + row_name_field] + [
                    'infrastructure__category__name' if dim == 'infrastructure' else (
                        'service__category__name' if dim == 'services' else
                        'facility__' + dim
                    ) for dim in col_dims
                ]
                aggregations = queryset.values(*group_fields).annotate(total=Count('facility__id'))
            elif 'services' in col_dims:
                queryset = FacilityService.objects.filter(
                    facility__in=base_queryset
                ).select_related('service__category', 'facility')
                if service_category:
                    queryset = queryset.filter(service__category__id=service_category)
                group_fields = ['facility__' + row_name_field] + [
                    'service__category__name' if dim == 'services' else (
                        'infrastructure__category__name' if dim == 'infrastructure' else
                        'facility__' + dim
                    ) for dim in col_dims
                ]
                aggregations = queryset.values(*group_fields).annotate(total=Count('facility__id'))

            for agg in aggregations:
                row_value = agg['facility__' + row_name_field] or 'Unknown'
                col_values = [
                    agg[
                        'infrastructure__category__name' if dim == 'infrastructure' else (
                            'service__category__name' if dim == 'services' else
                            'facility__' + dim
                        )
                    ] or 'Unknown' for dim in col_dims
                ]
                count = agg['total']
                current = counts[row_value]
                for i, value in enumerate(col_values[:-1]):
                    current = current[value]
                current[col_values[-1]] = count

        elif 'bed_types' in col_dims:
            # Handle bed_types by annotating each bed type
            bed_annotations = {}
            bed_type_mapping = {
                'number_of_beds': 'beds',
                'number_of_cots': 'cots',
                'number_of_maternity_beds': 'maternity_beds',
                'number_of_isolation_beds': 'isolation_beds',
                'number_of_emergency_casualty_beds': 'emergency_casualty_beds',
                'number_of_icu_beds': 'icu_beds',
                'number_of_hdu_beds': 'hdu_beds',
                'number_of_inpatient_beds': 'inpatient_beds'
            }
            for field, label in self.bed_type_mapping.items():
                alias = bed_type_mapping[field]
                bed_annotations[alias] = Sum(
                    Case(
                        When(**{field + '__gt': 0}, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )

            group_fields = [row_name_field] + [
                dim for dim in col_dims if dim != 'bed_types'
            ]
            aggregations = base_queryset.values(*group_fields).annotate(**bed_annotations)

            for agg in aggregations:
                row_value = agg[row_name_field] or 'Unknown'
                for field, label in self.bed_type_mapping.items():
                    col_values = []
                    for dim in col_dims:
                        if dim == 'bed_types':
                            col_values.append(label)
                        else:
                            col_values.append(agg[dim] or 'Unknown')
                    count = agg[bed_type_mapping[field]] or 0  # Handle potential None
                    current = counts[row_value]
                    for i, value in enumerate(col_values[:-1]):
                        current = current[value]
                    current[col_values[-1]] = count

        else:
            # Facility count logic
            aggregations = base_queryset.values(row_name_field, *col_dims).annotate(total=Count('id'))
            for agg in aggregations:
                row_value = agg[row_name_field] or 'Unknown'
                col_values = [agg[dim] or 'Unknown' for dim in col_dims]
                count = agg['total']
                current = counts[row_value]
                for i, value in enumerate(col_values[:-1]):
                    current = current[value]
                current[col_values[-1]] = count

        # Get distinct row values
        row_values = base_queryset.values(row_name_field, row_id_field).distinct().order_by(row_name_field)
        row_comparison_data = [
            {'id': str(row[row_id_field]), 'name': row[row_name_field] or 'Unknown'}
            for row in row_values
        ]

        # Convert defaultdict to regular dict for JSON serialization
        def defaultdict_to_dict(d):
            if isinstance(d, defaultdict):
                d = {k: defaultdict_to_dict(v) for k, v in d.items()}
            return d

        counts = defaultdict_to_dict(counts)

        # Prepare response
        data = {
            'row_comparison': row_comparison_data,
            'counts': counts
        }

        # Calculate totals
        totals = {
            'rows': [
                {
                    'name': row['name'],
                    'total': sum(
                        functools.reduce(
                            lambda d, k: d.get(k, {}) if isinstance(d, dict) else 0,
                            [counts.get(row['name'], {})] + list(c),
                            0
                        )
                        for c in itertools.product(*headers)
                    )
                }
                for row in row_comparison_data
            ],
            'columns': [
                {
                    'key': '_'.join(c),
                    'total': sum(
                        functools.reduce(
                            lambda d, k: d.get(k, {}) if isinstance(d, dict) else 0,
                            [counts.get(row['name'], {})] + list(c),
                            0
                        )
                        for row in row_comparison_data
                    )
                }
                for c in itertools.product(*headers)
            ]
        }

        return data, totals

    def get_report_data(self, *args, **kwargs):
        '''Route reports based on report_type param.'''
        report_type = self.request.query_params.get('report_type', 'facility_count_by_county')

        # Matrix report
        if report_type == 'matrix_report':
            county_id = self.request.query_params.get('county', None)
            filters = {}
            if county_id:
                row_comparison = self.request.query_params.get('row_comparison', 'county')
                if row_comparison not in self.row_comparison_options:
                    raise ValidationError(f"Invalid row_comparison. Choose from {list(self.row_comparison_options.keys())}")
                filters[self.row_comparison_options[row_comparison]['filter_field']] = county_id
            return self._get_matrix_report(filters=filters)

        # Placeholder for other report types
        raise NotFound(detail='Report not found.')


class MatrixReportView(FilterReportMixin, APIView):
    def get(self, *args, **kwargs):
        data, totals = self.get_report_data()
        return Response(data={
            'results': data,
            'totals': totals
        })
class TestReportView(FilterReportMixin, APIView):
    def get(self, *args, **kwargs):
        data, totals = self.get_report_data()
        return Response(data={
            'results': data,
            'totals': totals
        })
