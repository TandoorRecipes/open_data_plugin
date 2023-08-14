import datetime
import json
import traceback

import requests
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataConversion, OpenDataVersion
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer, OpenDataFoodSerializer, OpenDataCategorySerializer, OpenDataStoreSerializer, OpenDataPropertySerializer, OpenDataConversionSerializer, OpenDataVersionSerializer
from recipes.settings import FDA_API_KEY


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


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects.all()
    serializer_class = OpenDataUnitSerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataCategoryViewSet(viewsets.ModelViewSet):
    queryset = OpenDataCategory.objects.all()
    serializer_class = OpenDataCategorySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataStoreViewSet(viewsets.ModelViewSet):
    queryset = OpenDataStore.objects.all()
    serializer_class = OpenDataStoreSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]


class OpenDataPropertyViewSet(viewsets.ModelViewSet):
    queryset = OpenDataProperty.objects.all()
    serializer_class = OpenDataPropertySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataFoodViewSet(viewsets.ModelViewSet):
    queryset = OpenDataFood.objects.all()
    serializer_class = OpenDataFoodSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]

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


class OpenDataConversionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataConversion.objects.all()
    serializer_class = OpenDataConversionSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]


class FDCViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        pk = pk.strip()
        response = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{pk}?api_key={FDA_API_KEY}')
        if response.status_code == 429:
            return JsonResponse({'error', 'API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information'}, status=429, json_dumps_params={'indent': 4})

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
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1003:
                    p = OpenDataProperty.objects.get(fdc_id=1003)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1005:
                    p = OpenDataProperty.objects.get(fdc_id=1005)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1004:
                    p = OpenDataProperty.objects.get(fdc_id=1004)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name, 'version': {'id': p.version.id, 'name': p.version.name, 'code': p.version.code}}, "property_amount": round(fn['amount'], 2)})

            try:
                parsed_data['comment'] = f"FDC Measure: 1 {data['foodPortions'][0]['measureUnit']['name']} = {data['foodPortions'][0]['gramWeight']} gram (#{data['foodPortions'][0]['id']} {data['foodPortions'][0]['minDateAcquired']})"
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

        food_stats_last_30 = OpenDataFood.objects.filter(created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).all().values('created_by__username').annotate(total=Count('created_by')).order_by('-total')[:3]
        conversion_stats_last_30 = OpenDataConversion.objects.filter(created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).all().values('created_by__username').annotate(total=Count('created_by')).order_by('-total')[:3]

        for f in food_stats_last_30:
            stats['food_stats_last_30'].append({'username': f['created_by__username'], 'count': f['total']})

        for f in conversion_stats_last_30:
            stats['conversion_stats_last_30'].append({'username': f['created_by__username'], 'count': f['total']})

        return JsonResponse(stats, json_dumps_params={'indent': 4})
