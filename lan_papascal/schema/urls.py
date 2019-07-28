from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer


schema_view_json = get_schema_view(
                title="API Lan Papascal",
                renderer_classes=[JSONOpenAPIRenderer]
                )

urlpatterns = [
    path('openapi/', schema_view_json),
]