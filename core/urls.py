from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_user_profile_data, get_user_mappings, create_mapping, delete_mapping
app_name = 'core'

urlpatterns = [
    path('users/<str:pk>', get_user_profile_data, name='user-profile'),
    
    # Keyboard mapping endpoints
    path('users/<str:pk>/mappings', get_user_mappings, name='list-mappings'),
    path('users/<str:pk>/mappings/new', create_mapping, name='create-mapping'),
    path('users/<str:pk>/mappings/delete', delete_mapping, name='delete-mapping'),
    path('users/<str:pk>/mappings/set_active', delete_mapping, name='activate-mapping'), # Not used at the moment, likely used on the Electron App tho
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)