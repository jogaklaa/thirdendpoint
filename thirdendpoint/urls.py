from django.conf.urls import include, url
from django.contrib import admin
from thirdendpt import views


api_patterns = [
    url(
        r'receive_fabrication_metadata/',
        views.FabricationData.as_view(),
        name='receive_fabrication_metadata'
    )
]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_patterns, namespace='api')),
]
