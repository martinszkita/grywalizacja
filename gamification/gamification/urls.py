from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), 
    path('statystyki/', views.stats, name='stats'),
    path('o_pracy/', views.o_pracy, name='o_pracy'),
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
