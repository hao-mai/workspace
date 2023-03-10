
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from django.urls import include, path
from django.conf import settings

from virtual_library import viewsets
from virtual_library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", lambda request: HttpResponseRedirect("/admin/")),
]

##################################


router = routers.DefaultRouter()
router.register(r'books', viewsets.BookViewSet, basename='book')
router.register('checkout', viewsets.CheckoutViewSet, basename='checkout')

urlpatterns = [
    path("virtual_library/", include(router.urls)),
    path('home/', views.home, name='home'),
    path('library/', views.libraryhomepage, name='library'),
    path('resume/', views.resume, name='resume'),
]

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
        path("", include(router.urls)),
        path("virtual_library/docs/", swagger_view, name="library_docs"),
        path("virtual_library/schema/", schema_view, name="library_schema"),

    ]
