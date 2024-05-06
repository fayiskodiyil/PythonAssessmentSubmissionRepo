
from django.views.static import serve
from django.urls import include, path, re_path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include(('web.urls'),namespace='web')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]

handler400 = views.error_400
handler404 = views.error_404
handler500 = views.error_500