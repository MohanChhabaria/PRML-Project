from django.urls import path, include
from .views import home, predict


urlpatterns =[
    path('', home, name= 'index'),
    path('predict', predict, name = 'make predictions')
]