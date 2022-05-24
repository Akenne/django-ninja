from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Form, Schema, Query
from datetime import datetime, timezone
from .models import Loss
from django.db.models import Q
from django.core.serializers import serialize
from django.http import JsonResponse
from http import HTTPStatus
from typing import List
from django.shortcuts import get_object_or_404

api = NinjaAPI()

# Here we define the input using django-ninja's magical schemas
class FilterSchema(Schema):
    filter_name: str
    value: str
    op: str = 'exact'

class SortSchema(Schema):
    sort_name: str
    reverse: bool = False

class LossIn(Schema):
    uuid: str = None
    nlosses: int = None
    filters: List[FilterSchema] = []
    sorts: List[SortSchema] = []

# our response schema
class TaskSchema(Schema):
    uuid: str
    company_id: str
    company_name: str
    scenario: int
    total: float
    hurricane: float
    flood: float
    storm: float
    wildfire: float

    @staticmethod
    def resolve_uuid(obj):
        return str(obj.uuid)


# assumption: if you specify "fields" you only want those fields returned
# "fetch a single record" -> no specification of what you are using as a key here, so I will assume UUID
# because if you wanted to filter it on other fields you can use the filters

# declare the endpoint and it's response
@api.post("/company_loss", response = List[TaskSchema])
def company_loss(request, payload: LossIn): # our schema is used here
    payload = payload.dict()

    # if we specify a uuid just return the single object
    if payload['uuid']:
        obj = Loss.objects.filter(uuid=payload['uuid'])
        return obj

    q = {}
    for filtr in payload['filters']:
        # sanity check the operator before we filter the database
        if filtr['op'] not in ['exact','lte','lt','gte','gt']:
            continue
        # generate the filter FIELDNAME__OPERATOR: VALUE
        q.update({filtr['filter_name'] + '__' + filtr['op']:filtr['value']})

    # get our queryset based on our filters (or no filters)
    qs = Loss.objects.filter(**q)

    # if we have any sorts we handle them now
    if payload['sorts']:
        # first construct the list of sorts
        sort_final = []
        for sort in payload['sorts']:
            if sort['reverse']:
                sort_final.append('-' + sort['sort_name'])
            else:
                sort_final.append(sort['sort_name'])

        # then we sort the queryset
        qs.order_by(*sort_final)

    # if nlosses is present only return that many
    if payload['nlosses']:
        return qs[:payload['nlosses']]
    else:
        return qs
        