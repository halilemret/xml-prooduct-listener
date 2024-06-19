from django.urls import path
from .views import urun_listesi

urlpatterns = [
    path('', urun_listesi, name='urun_listesi'),
]
