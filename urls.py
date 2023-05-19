from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view

from recipes.plugins.open_data_plugin import views, api
from recipes.settings import DEBUG

router = routers.DefaultRouter()
router.register(r'open-data-unit', api.OpenDataUnitViewSet)

urlpatterns = [
    path('', views.test, name='index'),


    path('openapi/', get_schema_view(title="Tandoor Open Data Plugin", version=1, public=True,
                                     permission_classes=(permissions.AllowAny,)), name='openapi-schema'),

    path('api/', include((router.urls, 'api'))),
]

if DEBUG:
    urlpatterns.append(path('test/', views.test, name='view_test'))
