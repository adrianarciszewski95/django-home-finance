from django.urls import path
from homefinance.views import main_view
urlpatterns = [
    path('', main_view)
]
