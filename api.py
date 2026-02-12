import datetime
import json
import traceback

import requests
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets, permissions, decorators
from rest_framework.permissions import SAFE_METHODS

from cookbook.views.api import DefaultPagination
from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataConversion, OpenDataVersion, \
    OpenDataFoodProperty
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer, OpenDataFoodSerializer, OpenDataCategorySerializer, OpenDataStoreSerializer, \
    OpenDataPropertySerializer, OpenDataConversionSerializer, OpenDataVersionSerializer
from recipes.settings import FDC_API_KEY
from cookbook.helper.HelperFunctions import safe_request


class OpenDataIsOwner(permissions.BasePermission):
    message = 'You cannot interact with this object as it is not owned by you!'

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.method in SAFE_METHODS


class OpenDataIsModerator(permissions.BasePermission):
    message = 'You cannot interact with this object as you are not a moderator'

    def has_permission(self, request, view):
        return request.user.opendatauser.moderator_user or request.method in SAFE_METHODS


class OpenDataIsVerified(permissions.BasePermission):
    message = 'You cannot interact with this object as you are not verified'

    def has_permission(self, request, view):
        return request.user.opendatauser.verified_user or request.method in SAFE_METHODS


class OpenDataVersionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataVersion.objects.all()
    serializer_class = OpenDataVersionSerializer
    permission_classes = [OpenDataIsModerator]
    pagination_class = DefaultPagination


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects.all()
    serializer_class = OpenDataUnitSerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination


class OpenDataCategoryViewSet(viewsets.ModelViewSet):
    queryset = OpenDataCategory.objects.all()
    serializer_class = OpenDataCategorySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination


class OpenDataStoreViewSet(viewsets.ModelViewSet):
    queryset = OpenDataStore.objects.all()
    serializer_class = OpenDataStoreSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination


class OpenDataPropertyViewSet(viewsets.ModelViewSet):
    queryset = OpenDataProperty.objects.all()
    serializer_class = OpenDataPropertySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination


class OpenDataFoodViewSet(viewsets.ModelViewSet):
    queryset = OpenDataFood.objects.all()
    serializer_class = OpenDataFoodSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination

    def get_queryset(self):
        self.queryset = self.queryset.prefetch_related(
            'version',
            'created_by',

            'store_category',
            'store_category__version',
            'store_category__created_by',

            'preferred_unit_metric',
            'preferred_unit_metric__version',
            'preferred_unit_metric__created_by',

            'preferred_shopping_unit_metric',
            'preferred_shopping_unit_metric__version',
            'preferred_shopping_unit_metric__created_by',

            'preferred_unit_imperial',
            'preferred_unit_imperial__version',
            'preferred_unit_imperial__created_by',

            'preferred_shopping_unit_imperial',
            'preferred_shopping_unit_imperial__version',
            'preferred_shopping_unit_imperial__created_by',

            'properties',
            'properties__created_by',

            'properties__property',
            'properties__property__version',
            'properties__property__created_by',

            'properties_food_unit',
            'properties_food_unit__version',
            'properties_food_unit__created_by',

        )
        return self.queryset

    @decorators.action(detail=True, methods=['POST'], )
    def fdc(self, request, pk):
        """
        updates the food with all possible data from the FDC Api
        if properties with a fdc_id already exist they will be overridden, if existing properties don't have a fdc_id they won't be changed
        """
        food = self.get_object()

        if request.data['fdc_id']:
            food.fdc_id = request.data['fdc_id']

        if not food.fdc_id:
            return JsonResponse({'msg': 'Food has no FDC ID associated.'}, status=400, json_dumps_params={'indent': 4})

        response = safe_request('GET', f'https://api.nal.usda.gov/fdc/v1/food/{food.fdc_id}?api_key={FDC_API_KEY}')
        if response.status_code == 429:
            return JsonResponse(
                {
                    'msg':
                        'API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information. \
                                Configure your key in Tandoor using environment FDC_API_KEY variable.'
                },
                status=429,
                json_dumps_params={'indent': 4})
        if response.status_code != 200:
            return JsonResponse({
                'msg': f'Error while requesting FDC data using url https://api.nal.usda.gov/fdc/v1/food/{food.fdc_id}?api_key=****'},
                status=response.status_code,
                json_dumps_params={'indent': 4})

        try:
            data = json.loads(response.content)

            food.version = OpenDataVersion.objects.filter(name='base').first()
            food.slug = f"food-{data['description'].lower().replace(' ', '-').replace(',', '')}"
            food.name = data['description']
            food.plural_name = data['description']
            food.properties_source = f'https://fdc.nal.usda.gov/fdc-app.html#/food-details/{food.fdc_id}/nutrients'
            food.properties_food_amount = 100
            food.properties_food_unit = OpenDataUnit.objects.filter(base_unit='g').first()

            food.save()

            food_property_list = []

            # delete all properties where the property type has a fdc_id as these should be overridden
            for fp in food.properties.all():
                if fp.property.fdc_id:
                    fp.delete()

            for pt in OpenDataProperty.objects.filter(fdc_id__gte=0).all():
                if pt.fdc_id:
                    property_found = False
                    for fn in data['foodNutrients']:
                        if fn['nutrient']['id'] == pt.fdc_id:
                            property_found = True
                            # sometimes FDC might return negative values which make no sense, set to 0
                            food_property_list.append(OpenDataFoodProperty(property_id=pt.id, property_amount=max(0, round(fn['amount'], 2)), created_by=request.user))
                    if not property_found:
                        # if field not in FDC data the food does not have that property
                        food_property_list.append(OpenDataFoodProperty(property_id=pt.id, property_amount=0, created_by=request.user))

            properties = OpenDataFoodProperty.objects.bulk_create(food_property_list, unique_fields=('property',))

            food.properties.set(properties)

            return self.retrieve(request, pk)
        except Exception:
            traceback.print_exc()
            return JsonResponse({'msg': 'there was an error parsing the FDC data, please check the server logs'},
                                status=500, json_dumps_params={'indent': 4})


class OpenDataConversionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataConversion.objects.all()
    serializer_class = OpenDataConversionSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]
    pagination_class = DefaultPagination


class FDCViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        pk = pk.strip()
        response = safe_request('GET', f'https://api.nal.usda.gov/fdc/v1/food/{pk}?api_key={FDC_API_KEY}')
        if response.status_code == 429:
            return JsonResponse({'error', 'API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information'}, status=429,
                                json_dumps_params={'indent': 4})

        try:
            data = json.loads(response.content)

            parsed_data = {
                'version': {'id': 1, 'name': 'base', 'code': 'base'},
                'slug': f"food-{data['description'].lower().replace(' ', '-').replace(',', '')}",
                'name': data['description'],
                'plural_name': data['description'],
                'properties_food_amount': 100,
                'properties_source': f'https://fdc.nal.usda.gov/fdc-app.html#/food-details/{pk}/nutrients',
                'properties': [],
                'fdc_id': pk
            }

            unit_g = OpenDataUnit.objects.filter(base_unit='G').first()
            if unit_g:
                parsed_data['properties_food_unit'] = {'id': unit_g.id, 'slug': unit_g.slug, 'name': unit_g.name, 'plural_name': unit_g.plural_name, 'type': unit_g.type,
                                                       'version': {'id': unit_g.version.id, 'name': unit_g.version.name, 'code': unit_g.version.code}}

            if OpenDataProperty.objects.filter(fdc_id__isnull=False).count() == 0:  # TODO better solution with cache
                base_version = OpenDataVersion.objects.first()
                OpenDataProperty.objects.create(slug='property-calories', name='Calories', unit='kcal', fdc_id=1008, created_by=request.user, version=base_version)
                OpenDataProperty.objects.create(slug='property-proteins', name='Proteins', unit='g', fdc_id=1003, created_by=request.user, version=base_version)
                OpenDataProperty.objects.create(slug='property-carbohydrates', name='Carbohydrates', unit='g', fdc_id=1005, created_by=request.user, version=base_version)
                OpenDataProperty.objects.create(slug='property-fats', name='Fats', unit='g', fdc_id=1004, created_by=request.user, version=base_version)

            for fn in data['foodNutrients']:
                if fn['nutrient']['id'] == 1008:
                    p = OpenDataProperty.objects.get(fdc_id=1008)
                    parsed_data['properties'].append(
                        {"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}},
                         "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1003:
                    p = OpenDataProperty.objects.get(fdc_id=1003)
                    parsed_data['properties'].append(
                        {"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}},
                         "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1005:
                    p = OpenDataProperty.objects.get(fdc_id=1005)
                    parsed_data['properties'].append(
                        {"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}},
                         "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1004:
                    p = OpenDataProperty.objects.get(fdc_id=1004)
                    parsed_data['properties'].append(
                        {"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}},
                         "property_amount": round(fn['amount'], 2)})

            try:
                parsed_data[
                    'comment'] = f"FDC Measure: 1 {data['foodPortions'][0]['measureUnit']['name']} = {data['foodPortions'][0]['gramWeight']} gram (#{data['foodPortions'][0]['id']} {data['foodPortions'][0]['minDateAcquired']})"
            except:
                pass

            return JsonResponse(parsed_data, json_dumps_params={'indent': 4})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'{e} - check server log'}, status=500, json_dumps_params={'indent': 4})


class OpenDataStatisticsViewSet(viewsets.ViewSet):

    def list(self, request):
        stats = {
            'food_stats_total': [],
            'conversion_stats_total': [],
            'food_stats_last_30': [],
            'conversion_stats_last_30': [],
            'object_counts': {
                'food': OpenDataFood.objects.all().count(),
                'unit': OpenDataUnit.objects.all().count(),
                'conversion': OpenDataConversion.objects.all().count(),
                'category': OpenDataCategory.objects.all().count(),
                'store': OpenDataStore.objects.all().count(),
                'property': OpenDataProperty.objects.all().count(),
                'version': OpenDataVersion.objects.all().count(),
            },
        }

        food_stats_total = OpenDataFood.objects.all().values('created_by__username').annotate(total=Count('created_by')).order_by('-total')[:3]
        conversion_stats_total = OpenDataConversion.objects.all().values('created_by__username').annotate(total=Count('created_by')).order_by('-total')[:3]

        for f in food_stats_total:
            stats['food_stats_total'].append({'username': f['created_by__username'], 'count': f['total']})

        for f in conversion_stats_total:
            stats['conversion_stats_total'].append({'username': f['created_by__username'], 'count': f['total']})

        food_stats_last_30 = OpenDataFood.objects.filter(created_at__gt=datetime.datetime.today() - datetime.timedelta(days=30)).all().values('created_by__username').annotate(
            total=Count('created_by')).order_by('-total')[:3]
        conversion_stats_last_30 = OpenDataConversion.objects.filter(created_at__gt=datetime.datetime.today() - datetime.timedelta(days=30)).all().values(
            'created_by__username').annotate(total=Count('created_by')).order_by('-total')[:3]

        for f in food_stats_last_30:
            stats['food_stats_last_30'].append({'username': f['created_by__username'], 'count': f['total']})

        for f in conversion_stats_last_30:
            stats['conversion_stats_last_30'].append({'username': f['created_by__username'], 'count': f['total']})

        return JsonResponse(stats, json_dumps_params={'indent': 4})
