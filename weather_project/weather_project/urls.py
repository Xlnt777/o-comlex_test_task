from django.contrib import admin
from django.urls import path, include
from weather import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('autocomplete/', views.autocomplete_city, name = 'autocomplete_city'),
    path('api/v1/city-stats/', views.city_stats_api, name = 'city_stats_api'),
]
