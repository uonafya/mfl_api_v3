from datetime import timedelta, datetime

from django.utils import timezone
from django.db.models import Q

from rest_framework.views import APIView, Response
from common.models import County, SubCounty, Ward
from chul.models import CommunityHealthUnit

from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    FacilityType,
    Facility,
    KephLevel
)
from ..views import QuerysetFilterMixin


class DashBoard(QuerysetFilterMixin, APIView):
    queryset = Facility.objects.all()

    def get_chu_count_in_county_summary(self, county):
        return CommunityHealthUnit.objects.filter(
            facility__ward__sub_county__county=county).count()

    def get_chu_count_in_constituency_summary(self, const):
        return CommunityHealthUnit.objects.filter(
            facility__ward__sub_county=const).count()

    def get_chu_count_in_ward_summary(self, ward):
        return CommunityHealthUnit.objects.filter(
            facility__ward=ward).count()

    def get_facility_county_summary(self):
        if not self.request.query_params.get('county'):
            counties = County.objects.all()
            if not self.request.user.is_national:
                counties = counties.filter(id=self.request.user.county.id)
                queryset = Facility.objects.filter(county=self.request.user.county)
        else:
            counties = [County.objects.get(id=self.request.query_params.get('county'))]
            queryset = self.get_queryset().filter(county=counties[0])
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.get_queryset().filter(
                ward__sub_county__county=county).count()
            facility_county_summary[str(county.name)] = facility_county_count
        top_10_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        facility_county_summary
        top_10_counties_summary = []
        for item in top_10_counties:
            county = County.objects.get(name=item[0])
            chu_count = self.get_chu_count_in_county_summary(county)
            top_10_counties_summary.append(
                {
                    "name": item[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_counties_summary if self.request.user.is_national else []

    def get_facility_constituency_summary(self):
        constituencies = SubCounty.objects.filter(
            county=self.request.user.county)
        constituencies = constituencies if self.request.user.county else []

        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = self.get_queryset().filter(
                ward__sub_county=const).count()
            facility_constituency_summary[
                str(const.name)] = facility_const_count
        top_10_consts = sorted(
            facility_constituency_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_consts_summary = []
        for item in top_10_consts:
            const = SubCounty.objects.get(name=item[0])
            chu_count = self.get_chu_count_in_constituency_summary(const)
            top_10_consts_summary.append(
                {
                    "name": item[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_consts_summary

    def get_facility_ward_summary(self):
        wards = Ward.objects.filter(
            sub_county=self.request.user.sub_county) \
            if self.request.user.sub_county else []
        facility_ward_summary = {}
        for ward in wards:
            facility_ward_count = self.get_queryset().filter(
                ward=ward).count()
            facility_ward_summary[
                str(ward.name + "|" + str(ward.code))] = facility_ward_count
        top_10_wards = sorted(
            facility_ward_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_wards_summary = []
        for item in top_10_wards:
            ward = Ward.objects.get(code=item[0].split('|')[1])
            chu_count = self.get_chu_count_in_ward_summary(ward)
            top_10_wards_summary.append(
                {
                    "name": item[0].split('|')[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_wards_summary

    def get_facility_type_summary(self, cty):
        facility_type_parents_names = []
        for f_type in FacilityType.objects.all():
            if f_type.sub_division:
                facility_type_parents_names.append(f_type.sub_division)

        facility_types = FacilityType.objects.filter(
            sub_division__in=facility_type_parents_names)

        facility_type_summary = []
        summaries = {}
        for parent in facility_type_parents_names:
            summaries[parent] = 0

        for facility_type in facility_types:
            if not cty:
                summaries[facility_type.sub_division] = summaries.get(
                    facility_type.sub_division) + self.get_queryset().filter(
                    facility_type=facility_type).count()
            else:
                summaries[facility_type.sub_division] = self.get_queryset().filter(
                    facility_type=facility_type, ward__sub_county__county=cty).count()

        facility_type_summary = [
            {"name": key, "count": value} for key, value in summaries.items()
        ]

        facility_type_summary_sorted = sorted(
            facility_type_summary,
            key=lambda x: x['count'], reverse=True)

        return facility_type_summary_sorted

    def get_facility_owner_summary(self, cty):
        owners = Owner.objects.all()
        facility_owners_summary = []
        for owner in owners:
            if not cty:
                facility_owners_summary.append(
                    {
                        "name": owner.name,
                        "count": self.get_queryset().filter(
                            owner=owner).count()
                    })
            else:
                facility_owners_summary.append(
                    {
                        "name": owner.name,
                        "count": self.get_queryset().filter(
                            ward__sub_county__county=cty, owner=owner).count()
                    })
        return facility_owners_summary

    def get_facility_status_summary(self, cty):
        statuses = FacilityStatus.objects.all()
        status_summary = []
        for status in statuses:
            if not cty:
                status_summary.append(
                    {
                        "name": status.name,
                        "count": self.get_queryset().filter(
                            operation_status=status).count()
                    })
            else:
                status_summary.append(
                    {
                        "name": status.name,
                        "count": self.get_queryset().filter(
                            ward__sub_county__county=cty,
                            operation_status=status).count()
                    })

        return status_summary

    def get_facility_owner_types_summary(self, cty):
        owner_types = OwnerType.objects.all()
        owner_types_summary = []
        for owner_type in owner_types:
            if not cty:
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": self.get_queryset().filter(
                            owner__owner_type=owner_type).count()
                    })
            else:
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": self.get_queryset().filter(
                            ward__sub_county__county=cty,
                            owner__owner_type=owner_type).count()
                    })

        return owner_types_summary

    def get_recently_created_facilities(self, cty):
        right_now = timezone.now()
        last_week = self.request.query_params.get('last_week', None)
        last_month = self.request.query_params.get('last_month', None)
        last_three_months = self.request.query_params.get(
            'last_three_months', None)
        three_months_ago = right_now - timedelta(days=90)
        if not cty:
            if last_week:
                weekly = right_now - timedelta(days=7)
                return self.get_queryset().filter(
                    created__gte=weekly).count()

            if last_month:
                monthly = right_now - timedelta(days=30)
                return self.get_queryset().filter(
                    created__gte=monthly).count()

            if last_three_months:
                return self.get_queryset().filter(
                    created__gte=three_months_ago).count()

            return self.get_queryset().filter(
                created__gte=three_months_ago).count()
        else:
            if last_week:
                weekly = right_now - timedelta(days=7)
                return self.get_queryset().filter(
                    ward__sub_county__county=cty,
                    created__gte=weekly).count()

            if last_month:
                monthly = right_now - timedelta(days=30)
                return self.get_queryset().filter(
                    ward__sub_county__county=cty,
                    created__gte=monthly).count()

            if last_three_months:
                return self.get_queryset().filter(
                    ward__sub_county__county=cty,
                    created__gte=three_months_ago).count()

            return self.get_queryset().filter(
                ward__sub_county__county=cty,
                created__gte=three_months_ago).count()

    def get_recently_created_chus(self, cty):
        right_now = timezone.now()
        last_week = self.request.query_params.get('last_week', None)
        last_month = self.request.query_params.get('last_month', None)
        last_three_months = self.request.query_params.get(
            'last_three_months', None)
        three_months_ago = right_now - timedelta(days=90)
        if not cty:
            if last_week:
                weekly = right_now - timedelta(days=7)
                return CommunityHealthUnit.objects.filter(
                    facility__in=self.get_queryset(),
                    created__gte=weekly).count()

            if last_month:
                monthly = right_now - timedelta(days=30)
                return CommunityHealthUnit.objects.filter(
                    facility__in=self.get_queryset(),
                    created__gte=monthly).count()

            if last_three_months:
                return CommunityHealthUnit.objects.filter(
                    facility__in=self.get_queryset(),
                    date_established__gte=three_months_ago).count()

            return CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset(),
                date_established__gte=three_months_ago).count()
        else:
            if last_week:
                weekly = right_now - timedelta(days=7)
                return CommunityHealthUnit.objects.filter(
                    facility__ward__sub_county__county=cty,
                    facility__in=self.get_queryset(),
                    created__gte=weekly).count()

            if last_month:
                monthly = right_now - timedelta(days=30)
                return CommunityHealthUnit.objects.filter(
                    facility__ward__sub_county__county=cty,
                    facility__in=self.get_queryset(),
                    created__gte=monthly).count()

            if last_three_months:
                return CommunityHealthUnit.objects.filter(
                    facility__ward__sub_county__county=cty,
                    facility__in=self.get_queryset(),
                    date_established__gte=three_months_ago).count()

            return CommunityHealthUnit.objects.filter(
                facility__ward__sub_county__county=cty,
                facility__in=self.get_queryset(),
                date_established__gte=three_months_ago).count()

    def facilities_pending_approval_count(self, cty):
        if not cty:
            updated_pending_approval = self.get_queryset().filter(has_edits=True)
            newly_created = self.queryset.filter(approved=False, rejected=False)
        else:
            updated_pending_approval = self.get_queryset().filter(
                ward__sub_county__county=cty, has_edits=True)
            newly_created = self.queryset.filter(
                ward__sub_county__county=cty, approved=False, rejected=False)
        return len(
            list(set(list(updated_pending_approval) + list(newly_created)))
        )

    def get_facilities_approved_count(self, cty):
        if not cty:
            return self.queryset.filter(approved=True, rejected=False).count()
        else:
            return self.queryset.filter(approved=True, rejected=False, ward__sub_county__county=cty).count()

    def get_chus_pending_approval(self, cty):
        """
        Get the number of CHUs pending approval
        """
        if not cty:
            return CommunityHealthUnit.objects.filter(
                Q(is_approved=False, is_rejected=False) |
                Q(has_edits=True)).distinct().filter(
                facility__in=self.get_queryset()).count()
        else:
            return CommunityHealthUnit.objects.filter(
                Q(is_approved=False, is_rejected=False) |
                Q(has_edits=True)).distinct().filter(
                facility__in=self.get_queryset(),
                facility__ward__sub_county__county=cty).count()

    def get_rejected_chus(self, cty):
        """
        Get the number of CHUs that have been rejected
        """
        if not cty:
            return CommunityHealthUnit.objects.filter(is_rejected=True).count()
        else:
            return CommunityHealthUnit.objects.filter(
                is_rejected=True,
                facility__ward__sub_county__county=cty).count()

    def get_rejected_facilities_count(self, cty):
        if not cty:
            return self.get_queryset().filter(rejected=True).count()
        else:
            return self.get_queryset().filter(rejected=True, ward__sub_county__county=cty).count()

    def get_closed_facilities_count(self, cty):
        if not cty:
            return self.get_queryset().filter(closed=True).count()
        else:
            return self.get_queryset().filter(closed=True, ward__sub_county__county=cty).count()

    def get_facilities_kephlevel_count(self, county_name, period_start, period_end):
        """
        Function to get facilities by keph level
        """
        keph_level = KephLevel.objects.values("id", "name")
        keph_array = []
        print (self.request.user.sub_county, self.request.user.user_groups)
        for keph in keph_level:
            if self.request.query_params.get('ward'):
                keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                     keph_level_id=keph.get("id"),
                                                     ward=self.request.query_params.get('ward')).count()
                keph_array.append({"name": keph.get("name"), "count": keph_count})
            elif self.request.query_params.get('sub_county'):
                keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                     keph_level_id=keph.get("id"),
                                                     sub_county=self.request.query_params.get('sub_county')).count()
                keph_array.append({"name": keph.get("name"), "count": keph_count})
            elif self.request.query_params.get('county'):
                keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                     keph_level_id=keph.get("id"),
                                                     county=self.request.query_params.get('county')).count()
                keph_array.append({"name": keph.get("name"), "count": keph_count})
            elif self.request.user.is_national:
                keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                     keph_level_id=keph.get("id")).count()
                keph_array.append({"name": keph.get("name"), "count": keph_count})
            else:
                if (self.request.user.user_groups.get('is_sub_county_level')):
                    keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                         keph_level_id=keph.get("id"),
                                                         sub_county=self.request.user.sub_county).count()
                    keph_array.append({"name": keph.get("name"), "count": keph_count})
                elif (self.request.user.user_groups.get('is_county_level')):
                    keph_count = Facility.objects.filter(created__gte=period_start, created__lte=period_end,
                                                         keph_level_id=keph.get("id"), county=self.request.user.county).count()
                    keph_array.append({"name": keph.get("name"), "count": keph_count})
                else:
                    keph_count = 0
                    keph_array.append({"name": keph.get("name"), "count": keph_count})

        return keph_array

    def get(self, *args, **kwargs):
        user = self.request.user
        county_ = user.county
        if not self.request.query_params.get('county'):
            county_ = user.county
        else:
            county_ = County.objects.get(id=self.request.query_params.get('county'))
        if not county_:
            total_facilities = self.get_queryset().count()
        else:
            total_facilities = self.get_queryset().filter(
                ward__sub_county__county=county_).count()
        if not county_:
            total_chus = CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset()).count()
        else:
            total_chus = CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset().filter(
                    ward__sub_county__county=county_)).count()

        period_start = self.request.query_params.get('datefrom')
        period_end = self.request.query_params.get('dateto')
        if not period_end:
            period_end = datetime.max
        if not period_start:
            period_start = datetime.min

        data = {
            "total_facilities": total_facilities,
            "keph_level": self.get_facilities_kephlevel_count(county_, period_start, period_end),
            "county_summary": self.get_facility_county_summary()
            if user.is_national else [],
            "constituencies_summary": self.get_facility_constituency_summary()
            if user.county and not user.sub_county else [],
            "wards_summary": self.get_facility_ward_summary()
            if user.sub_county else [],
            "owners_summary": self.get_facility_owner_summary(county_),
            "types_summary": self.get_facility_type_summary(county_),
            "status_summary": self.get_facility_status_summary(county_),
            "owner_types": self.get_facility_owner_types_summary(county_),
            "recently_created": self.get_recently_created_facilities(county_),
            "recently_created_chus": self.get_recently_created_chus(county_),
            "pending_updates": self.facilities_pending_approval_count(county_),
            "rejected_facilities_count": self.get_rejected_facilities_count(county_),
            "closed_facilities_count": self.get_closed_facilities_count(county_),
            "rejected_chus": self.get_rejected_chus(county_),
            "chus_pending_approval": self.get_chus_pending_approval(county_),
            "total_chus": total_chus,
            "approved_facilities": self.get_facilities_approved_count(county_),

        }

        fields = self.request.query_params.get("fields", None)
        if fields:
            required = fields.split(",")
            required_data = {
                i: data[i] for i in data if i in required
            }
            return Response(required_data)
        return Response(data)