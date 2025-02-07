from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name='home'),
    path('business/<int:business_id>/', views.business_profile, name='business_profile'),
    path('register/', views.registerPage, name='register'),  # Ensure this matches the name used in templates
    path('login/', views.loginPage, name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('create/', views.business_create_view, name='business_create'),
    ]



# Only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


