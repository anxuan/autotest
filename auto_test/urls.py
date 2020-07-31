from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, \
    OpenAPIRenderer

from api_test import urls as api_test_urls


from api_test.api.ApiDoc import MockRequest

schema_view = get_schema_view(title='测试平台 API',
                              renderer_classes=[OpenAPIRenderer,
                                                SwaggerUIRenderer],
                              permission_classes=())
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^docs/', schema_view, name="docs"),
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api/', include(api_test_urls)),
    path('mock/<path:apiAdr>', MockRequest.as_view()),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
