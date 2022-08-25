from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.apps.app.urls')),
    path('pdu/', include('project.apps.pdu.urls')),
    path('env/', include('project.apps.env.urls')),
    path('sensor/', include('project.apps.sensor.urls'))
]
