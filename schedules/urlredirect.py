from django.urls import path
from.views import main_redirect


urlpatterns = [
    path('', main_redirect, name='main redirect')
]
