import json
import datetime
import reversion
import logging

from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils import timezone, encoding
from django.conf import settings 

from common.models import AbstractBase, Contact, SequenceMixin
from common.fields import SequenceField
from facilities.models import Facility


LOGGER = logging.getLogger(__name__) 


@reversion.register
# @encoding.python_2_unicode_compatible
class Status(AbstractBase):

    """
    Indicates the operation status of a community health unit.
    e.g  fully-functional, semi-functional, functional
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'statuses'


@reversion.register(follow=['health_unit', 'contact'])
# @encoding.python_2_unicode_compatible
class CommunityHealthUnitContact(AbstractBase):

    """
    The contacts of the health unit may be email, fax mobile etc.
    """
    health_unit = models.ForeignKey('CommunityHealthUnit', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: ({})".format(self.health_unit, self.contact)

    class Meta(object):
        unique_together = ('health_unit', 'contact', )
        # a hack since the view_communityhealthunitcontact
        # is disappearing into thin air
        '''
        permissions = (
            (
                # "view_communityhealthunitcontact",
                "Can view community health_unit contact"
            ),
        )
        '''


@reversion.register(follow=['facility', 'status'])
# @encoding.python_2_unicode_compatible
class CommunityHealthUnit(SequenceMixin, AbstractBase):

    """
    This is a health service delivery structure within a defined geographical
    area covering a population of approximately 5,000 people.

    Each unit is assigned 2 Community Health Extension Workers (CHEWs) and
    community health volunteers who offer promotive, preventative and basic
    curative health services
    """
    name = models.CharField(max_length=100)
    code = SequenceField(unique=True, editable=False,
        help_text='A sequential number allocated to each chu',
	null=True, blank=True)
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE,
        help_text='The facility on which the health unit is tied to.')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    households_monitored = models.PositiveIntegerField(
        default=0,
        help_text='The number of house holds a CHU is in-charge of')
    date_established = models.DateField(default=timezone.now)
    date_operational = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(null=True, blank=True, help_text='Determines if a chu has been approved')
    approval_comment = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closing_comment = models.TextField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)
    has_edits = models.BooleanField(
        default=False,
        help_text='Indicates that a community health unit has updates that are'
                  ' pending approval')
    number_of_chvs = models.PositiveIntegerField(
        default=0,
        help_text='Number of Community Health volunteers in the CHU')

    def __str__(self):
        return self.name

    @property
    def workers(self):
        from .serializers import CommunityHealthWorkerPostSerializer
        return CommunityHealthWorkerPostSerializer(
            self.health_unit_workers, many=True).data

    def validate_facility_is_not_closed(self):
        if self.facility.closed:
            raise ValidationError(
                {
                    "facility":
                    [
                        "A Community Unit cannot be attached to a closed "
                        "facility"
                    ]
                }
            )

    def validate_either_approved_or_rejected_and_not_both(self):
        error = {
            "approve/reject": [
                "A Community Unit cannot be approved and"
                " rejected at the same time "]
        }
        values = [self.is_approved, self.is_rejected]
        if values.count(True) > 1:
            raise ValidationError(error)

    def validate_date_operation_is_less_than_date_established(self):
        if self.date_operational and self.date_established:
            if self.date_established > self.date_operational:
                raise ValidationError(
                    {
                        "date_operational": [
                            "Date operation cannot be greater than date "
                            "established"
                        ]
                    })

    def validate_date_established_not_in_future(self):
        """
        Only the date operational needs to be validated.

        date_established should always be less then the date_operational.
        Thus is the date_operational is not in future the date_established
        is also not in future
        """

        today = datetime.datetime.now().date()

        if self.date_operational and self.date_operational > today:
            raise ValidationError(
                {
                    "date_operational": [
                        "The date operational cannot be in the future"
                    ]
                })

    def validate_comment_required_on_rejection(self):
        """
        Comments will only be required on the rejection of a community health
        unit. The approvals will not require comments.

        """
        if self.is_rejected and not self.rejection_reason:
            raise ValidationError(
                {
                    "rejection_reason": [
                        "Please provide the reason for rejecting the CHU"
                    ]
                })

    @property
    def contacts(self):
        return [
            {
                "id": con.id,
                "contact_id": con.contact.id,
                "contact": con.contact.contact,
                "contact_type": con.contact.contact_type.id,
                "contact_type_name": con.contact.contact_type.name

            }
            for con in CommunityHealthUnitContact.objects.filter(
                health_unit=self)
        ]

    @property
    def json_features(self):
        return {
            "geometry": {
                "coordinates": [
                    self.facility.facility_coordinates_through.coordinates[0],
                    self.facility.facility_coordinates_through.coordinates[1]
                ]
            },
            "properties": {
                "ward": self.facility.ward.id,
                "constituency": self.facility.ward.constituency.id,
                "county": self.facility.ward.county.id
            }
        }

    def clean(self):
        super(CommunityHealthUnit, self).clean()
        self.validate_facility_is_not_closed()
        self.validate_either_approved_or_rejected_and_not_both()
        self.validate_date_operation_is_less_than_date_established()
        self.validate_date_established_not_in_future()
        self.validate_comment_required_on_rejection()

    @property
    def pending_updates(self):
        try:
            chu = ChuUpdateBuffer.objects.filter(is_approved=False, is_rejected=False, health_unit=self)[0] if len(ChuUpdateBuffer.objects.filter(is_approved=False, is_rejected=False, health_unit=self)) else ChuUpdateBuffer.objects.get(is_approved=False, is_rejected=False, health_unit=self)
            return chu.updates
        except ChuUpdateBuffer.DoesNotExist:
            return {}

    @property
    def latest_update(self):
        try:
            chu = ChuUpdateBuffer.objects.filter(is_approved=False, is_rejected=False, health_unit=self)[0] if len(ChuUpdateBuffer.objects.filter(is_approved=False, is_rejected=False, health_unit=self)) else ChuUpdateBuffer.objects.get(is_approved=False, is_rejected=False, health_unit=self)
            return chu
        except ChuUpdateBuffer.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
	 # new chus that have just been added but not approved yet
        if not self.code and not self.is_approved:
            super(CommunityHealthUnit, self).save(*args, **kwargs)
        # existing chus that were approved previously and have been updated
        if self.code and self.is_approved:
            if settings.PUSH_TO_DHIS:
                self.push_chu_to_dhis2()
            super(CommunityHealthUnit, self).save(*args, **kwargs)
        # chus that have just been approved but don't have a code yet
        # and have not been pushed to DHIS yet
        if self.is_approved and not self.code:
            self.code = self.generate_next_code_sequence()
        if settings.PUSH_TO_DHIS:
            self.push_chu_to_dhis2()
        super(CommunityHealthUnit, self).save(*args, **kwargs)

    @property
    def average_rating(self):
        return self.chu_ratings.aggregate(r=models.Avg('rating'))['r'] or 0

    @property
    def rating_count(self):
        return self.chu_ratings.count()

    def push_chu_to_dhis2(self):
        from facilities.models.facility_models import DhisAuth
        import requests
        dhisauth = DhisAuth()
        dhisauth.get_oauth2_token()
        facility_dhis_id = self.get_facility_dhis2_parent_id()
        unit_uuid_status = dhisauth.get_org_unit_id(self.code)
        unit_uuid = unit_uuid_status[0]
        new_chu_payload = {
            "id": unit_uuid,
            "code": str(self.code),
            "name": str(self.name),
            "shortName": str(self.name),
            "displayName": str(self.name),
            "parent": {
                "id": facility_dhis_id
            },
            "openingDate": self.date_operational.strftime("%Y-%m-%d"),
        }
        
        metadata_payload = {
            "keph": 'axUnguN4QDh'
        }

        if unit_uuid_status[1] == 'retrieved':
            r = requests.put(
                settings.DHIS_ENDPOINT + "api/organisationUnits/" + new_chu_payload.pop('id'),
                auth=(settings.DHIS_USERNAME, settings.DHIS_PASSWORD),
                headers={
                    "Accept": "application/json"
                },
                json=new_chu_payload
            )
            print("Update CHU Response", r.url, r.status_code, r.json())
            LOGGER.info("Update CHU Response: %s" % r.text)
        else:
            r = requests.post(
                settings.DHIS_ENDPOINT + "api/organisationUnits",
                auth=(settings.DHIS_USERNAME, settings.DHIS_PASSWORD),
                headers={
                    "Accept": "application/json"
                },
                json=new_chu_payload
            )

            print("Create CHU Response", r.url, r.status_code, r.json())
            LOGGER.info("Create CHU Response: %s" % r.text)

        if r.json()["status"] != "OK":
            LOGGER.error("Failed PUSH: error -> {}".format(r.text))
            raise ValidationError(
                {
                    "Error!": ["An error occured while pushing Community Unit to DHIS2. This is may be caused by the "
                               "existance of an organisation unit with as similar name as to the one you are creating. "
                               "Or some specific information like codes are not unique"]
                }
            )
        self.push_chu_metadata(metadata_payload, unit_uuid)

    def push_chu_metadata(self, metadata_payload, chu_uid):
        # Keph Level
        import requests
        r_keph = requests.post(
            settings.DHIS_ENDPOINT + "api/organisationUnitGroups/" + metadata_payload[
                'keph'] + "/organisationUnits/" + chu_uid,
            auth=(settings.DHIS_USERNAME, settings.DHIS_PASSWORD),
            headers={
                "Accept": "application/json"
            },
        )
        LOGGER.info('Metadata CUs pushed successfullly')

    def get_facility_dhis2_parent_id(self):
        from facilities.models.facility_models import DhisAuth
        LOGGER.info('[ERROR] Facility Code : {}'.format(self.facility.code))
        r = requests.get(
            settings.DHIS_ENDPOINT + "api/organisationUnits.json",
            auth=(settings.DHIS_USERNAME, settings.DHIS_PASSWORD),
            headers={
                "Accept": "application/json"
            },
            params={
                "query": self.facility.code,
                "fields": "[id,name]",
                "filter": "level:in:[5]",
                "paging": "false"
            }
        )

        if len(r.json()["organisationUnits"]) is 1:
            if r.json()["organisationUnits"][0]["id"]:
                return r.json()["organisationUnits"][0]["id"]
        else:
            raise ValidationError(
                {
                    "Error!": ["Unable to resolve exact Facility linked to the CHU in DHIS2"]
                }
            )


    class Meta(AbstractBase.Meta):
        unique_together = ('name', 'facility', )
        permissions = (
            (
                "view_rejected_chus",
                "Can see the rejected community health units"
            ),
            (
                "can_approve_chu",
                "Can approve or reject a Community Health Unit"
            ),

        )


@reversion.register(follow=['health_worker', 'contact'])
# @encoding.python_2_unicode_compatible
class CommunityHealthWorkerContact(AbstractBase):

    """
    The contacts of the health worker.

    They may be as many as the health worker has.
    """
    health_worker = models.ForeignKey(
        'CommunityHealthWorker', on_delete=models.PROTECT,)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT,)

    def __str__(self):
        return "{}: ({})".format(self.health_worker, self.contact)


@reversion.register(follow=['health_unit'])
# @encoding.python_2_unicode_compatible
class CommunityHealthWorker(AbstractBase):

    """
    A person who is in-charge of a certain community health area.

    The status of the worker that is whether still active or not will be
    shown by the active field inherited from abstract base.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_incharge = models.BooleanField(default=False)
    health_unit = models.ForeignKey(
        CommunityHealthUnit, on_delete=models.PROTECT,
        help_text='The health unit the worker is in-charge of',
        related_name='health_unit_workers')

    def __str__(self):
        return "{} ({})".format(self.first_name, self.health_unit.name)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name).strip()
        else:
            return self.first_name


@reversion.register
# @encoding.python_2_unicode_compatible
class CHUService(AbstractBase):

    """
    The services offered by the Community Health Units

    Examples:
        1. First Aid Administration
        2. De-worming e.t.c.

    All the community health units offer these services. Hence, there is
    no need to link a COmmunity Health Unit to a CHUService instance
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


@reversion.register
# @encoding.python_2_unicode_compatible
class CHURating(AbstractBase):

    """Rating of a CHU"""

    chu = models.ForeignKey(
        CommunityHealthUnit, related_name='chu_ratings',
        on_delete=models.PROTECT,)
    rating = models.PositiveIntegerField(
        validators=[
            validators.MaxValueValidator(5),
            validators.MinValueValidator(0)
        ]
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.chu, self.rating)


class ChuUpdateBuffer(AbstractBase):
    """
    Buffers a community units updates until they are approved by the CHRIO
    """
    health_unit = models.ForeignKey(CommunityHealthUnit, on_delete=models.CASCADE)
    workers = models.TextField(null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)
    basic = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    services = models.TextField(null=True, blank=True)

    def validate_atleast_one_attribute_updated(self):
        if not self.workers and not self.contacts and not \
                self.basic and not self.is_new:
            raise ValidationError({"__all__": ["Nothing was edited"]})

    def update_basic_details(self):
        if self.basic:
            basic_details = json.loads(self.basic)
            if 'status' in basic_details:
                basic_details['status_id'] = basic_details.get(
                    'status').get('status_id')
                basic_details.pop('status')
            if 'facility' in basic_details:
                basic_details['facility_id'] = basic_details.get(
                    'facility').get('facility_id')
                basic_details.pop('facility')
           
            
            for key, value in basic_details.iteritems():
                setattr(self.health_unit, key, value)
            if 'basic' in basic_details:
                setattr(self.health_unit, 'facility_id', basic_details.get('basic').get('facility'))
            self.health_unit.save()

    def update_workers(self):
        chews = json.loads(self.workers)
        for chew in chews:
            chew['health_unit'] = self.health_unit
            chew['created_by_id'] = self.created_by_id
            chew['updated_by_id'] = self.updated_by_id
            chew.pop('created_by', None)
            chew.pop('updated_by', None)
            if 'id' in chew:
                chew_obj = CommunityHealthWorker.objects.get(
                    id=chew['id'])
                chew_obj.first_name = chew['first_name']
                chew_obj.last_name = chew['last_name']
                if 'is_incharge' in chew:
                    chew_obj.is_incharge = chew['is_incharge']
                chew_obj.save()
            else:
                CommunityHealthWorker.objects.create(**chew)

    def update_services(self):
        services = json.loads(self.services)
        CHUServiceLink.objects.filter(health_unit=self.health_unit).delete()
        for service in services:
            service['health_unit'] = self.health_unit
            service['created_by_id'] = self.created_by_id
            service['updated_by_id'] = self.updated_by_id
            service.pop('created_by', None)
            service.pop('updated_by', None)
            service.pop('name', None)
            try:
                CHUServiceLink.objects.get(
                    service_id=service['service'],
                    health_unit=self.health_unit)
            except CHUServiceLink.DoesNotExist:
                service['service_id'] = service.pop('service')
                CHUServiceLink.objects.create(**service)

    def update_contacts(self):
        contacts = json.loads(self.contacts)
        for contact in contacts:
            contact['updated_by_id'] = self.updated_by_id
            contact['created_by_id'] = self.created_by_id
            contact['contact_type_id'] = contact['contact_type']
            contact.pop('contact_type', None)
            contact.pop('contact_id', None)
            contact.pop('contact_type_name', None)
            contact['contact'] = contact['contact']
            contact_data = {
                'contact_type_id': contact['contact_type_id'],
                'contact': contact['contact']
            }
            try:
                contact_obj = Contact.objects.get(**contact_data)
            except Contact.DoesNotExist:
                contact_obj = Contact.objects.create(**contact)
            try:
                CommunityHealthUnitContact.objects.filter(
                    contact=contact_obj)[0]
            except IndexError:
                CommunityHealthUnitContact.objects.create(
                    contact=contact_obj,
                    health_unit=self.health_unit,
                    created_by_id=self.created_by_id,
                    updated_by_id=self.updated_by_id)

    @property
    def updates(self):
        updates = {}
        if self.basic:
            updates['basic'] = json.loads(self.basic)
        if self.contacts:
            updates['contacts'] = json.loads(self.contacts)
        if self.workers:
            updates['workers'] = json.loads(self.workers)
        if self.services:
            updates['services'] = json.loads(self.services)
        updates['updated_by'] = self.updated_by.get_full_name
        return updates

    def clean(self, *args, **kwargs):
        if not self.is_approved and not self.is_rejected:
            self.health_unit.has_edits = True
            self.health_unit.save()
        if self.is_approved and self.contacts:
            self.update_contacts()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_approved and self.workers:
            self.update_workers()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_approved and self.basic:
            self.update_basic_details()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_approved and self.services:
            self.update_services()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_rejected:
            self.health_unit.has_edits = False
            self.health_unit.save()

        self.validate_atleast_one_attribute_updated()

    def __str__(self):
        return self.health_unit.name

    # class Meta:
    #     get_latest_by = ['health_unit']


class CHUServiceLink(AbstractBase):
    """
    Links a CommunityHealthUnit to a CHUService.

    This ensures that CHU can offer a subset of the services available
    for CHUs.
    """
    health_unit = models.ForeignKey(
        CommunityHealthUnit, on_delete=models.PROTECT, related_name='services')
    service = models.ForeignKey(
        CHUService, on_delete=models.PROTECT)

    class Meta(AbstractBase.Meta):
        unique_together = ('health_unit', 'service')

    def __str__(self):
        return "{} - {}".format(self.health_unit.name, self.service.name)
