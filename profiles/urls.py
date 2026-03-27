from django.urls import path
from .views import portfolio

app_name = 'profiles'


urlpatterns = [
    path('portfolio/<str:username>/', portfolio, name='portfolio'),
]