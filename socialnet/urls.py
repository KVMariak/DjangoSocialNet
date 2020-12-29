from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


from home.views import (
    home_screen_view,
)


from profiles.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
)

urlpatterns = [
    path('', home_screen_view, name="home"),
    path('admin/', admin.site.urls),
    path('account/', account_view, name="account"),
    path('login/', login_view, name="login"),
    path('publications/', include('publications.urls', 'publications')),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),
    path('api/publications/', include('publications.api.urls', 'post_api')),
    path('api/profiles/', include('profiles.api.urls', 'profiles_api')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
