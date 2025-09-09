"""
URL configuration for TaskFlowAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from tasks.views import overview
from django.conf import settings
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path("", overview),
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    
]

"""Development only"""
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls))    
    ]

"""If the Djoser library is being used, auth can also be handled manually with simple jwt, albeit easier with Djoser"""
if settings.DJOSER:
    urlpatterns += [
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.authtoken')),
    ]

"""For Simplejwt"""
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]