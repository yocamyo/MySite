from django.contrib import admin
from django.urls import path

import contact

from .views import contactView, successView

urlpatterns = [
    path("", contactView, name="contact"),
    path("success/", successView, name="success"),
]
