from django.urls import path
from .views import solicitar


urlpatterns = [
    path('solicitar/', solicitar, name='solicitar_exame'),
]
