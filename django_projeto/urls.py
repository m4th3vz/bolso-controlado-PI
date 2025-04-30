# django_projeto/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('', include('expenses.urls')),
    path('', include('calculator.urls')),
    path('', include('staticpages.urls')),
    path('', include('shopping_list.urls')),
    path('', include('chatbot.urls')),
]
