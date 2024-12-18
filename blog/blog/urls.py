"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

# 127.0.0.1:8000/api/account/
urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/post/', include('post.api.urls'), name='post'),
                  path('api/comment/', include('comment.api.urls'), name='comment'),
                  path('api/favorite/', include('favorite.api.urls'), name='favorite'),
                  path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/account/', include('account.api.urls'), name='account')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
