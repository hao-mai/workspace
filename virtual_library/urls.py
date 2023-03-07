"""virtual_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from django.urls import include, path
from django.conf import settings

from virtual_library import viewsets
# from virtual_library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", lambda request: HttpResponseRedirect("/admin/")),
]

router = routers.DefaultRouter()
router.register('books', viewsets.BookViewSet, basename='book')
# router.register('checkout', viewsets.CheckoutViewSet, basename='checkout')


if settings.DEBUG or settings.ENVIRONMENT == "test":
    schema_view = SpectacularAPIView.as_view(
        patterns=[path("virtual_library/", include("virtual_library.urls"))],
        )
    swagger_view = SpectacularSwaggerView.as_view(
        title="Library API",
        url_name="library_schema",
    )
    urlpatterns += [
        path("virtual_library/", include(router.urls)),
        path("docs/", swagger_view, name="library_docs"),
        path("schema/", schema_view, name="library_schema"),
        # path('book_view/', views.book_view, name='book_view'),
        
    ]
