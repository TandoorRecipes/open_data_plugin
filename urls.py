from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view

from recipes.plugins.open_data_plugin import views, api
from recipes.settings import DEBUG

open_data_router = routers.DefaultRouter()
open_data_router.register(r'open-data-version', api.OpenDataVersionViewSet)
open_data_router.register(r'open-data-unit', api.OpenDataUnitViewSet)
open_data_router.register(r'open-data-category', api.OpenDataCategoryViewSet)
open_data_router.register(r'open-data-store', api.OpenDataStoreViewSet)
open_data_router.register(r'open-data-property', api.OpenDataPropertyViewSet)
open_data_router.register(r'open-data-conversion', api.OpenDataConversionViewSet)
open_data_router.register(r'open-data-food', api.OpenDataFoodViewSet)
open_data_router.register(r'open-data-FDC', api.FDCViewSet, basename='open-data-FDC')
open_data_router.register(r'open-data-stats', api.OpenDataStatisticsViewSet, basename='open-data-stats')

urlpatterns = [
    path('', views.test, name='open_data_index'),

]

if DEBUG:
    urlpatterns.append(path('test/', views.test, name='view_test'))
