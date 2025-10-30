from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    get_user_profile_data, 
    get_user_mappings, 
    create_mapping, 
    delete_mapping,
    set_active_mapping,
    CustomTokenObtainParView, 
    CustomTokenRefreshView, 
    register, 
    authenticated, 
    get_all_community_mappings, 
    join_waitlist, 
    get_specific_mapping, 
    add_tags, 
    rename_mapping, 
    update_mapping_visibility,
    ElectronTokenObtainView,
    ElectronTokenRefreshView,
    update_user_profile,
    update_user_preferences,
    change_password,
    delete_account,
    sync_mappings
)
app_name = 'core'

urlpatterns = [
    # User info 
    path('users/<str:pk>', get_user_profile_data, name='user-profile'),
    path('users/<str:pk>/profile/', update_user_profile, name='update-profile'),
    path('users/<str:pk>/preferences/', update_user_preferences, name='update-preferences'),
    path('users/<str:pk>/change-password/', change_password, name='change-password'),
    path('users/<str:pk>/account/', delete_account, name='delete-account'),
    path('users/<str:pk>/sync/', sync_mappings, name='sync-mappings'),
    
    # Keyboard mapping endpoints
    path('users/<str:pk>/mappings', get_user_mappings, name='list-mappings'),
    path('users/mappings/<str:mapping_id>', get_specific_mapping, name='get-mapping'),
    path('users/<str:pk>/mappings/new', create_mapping, name='create-mapping'),
    path('users/<str:pk>/mappings/delete', delete_mapping, name='delete-mapping'),
    path('users/<str:pk>/mappings/set_active', set_active_mapping, name='activate-mapping'), # Not used at the moment, likely used on the Electron App tho
    path('users/mappings/<str:mapping_id>/add_tags', add_tags, name='add-tags'),
    path('users/mappings/<str:mapping_id>/rename', rename_mapping, name='rename-mapping'),
    path('users/mappings/<str:mapping_id>/visibility', update_mapping_visibility, name='update-mapping-visibility'),
    
    # Login and Auth
    path('register/', register, name='register-user'),
    path('token/', CustomTokenObtainParView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('authenticated/', authenticated),
    
    # Electron-specific auth with extended refresh tokens
    path('electron/token/', ElectronTokenObtainView.as_view(), name='electron_token_obtain'),
    path('electron/token/refresh/', ElectronTokenRefreshView.as_view(), name='electron_token_refresh'),

    # Community 
    path('community/', get_all_community_mappings, name='community-mappings'),

    # Email Gathering
    path('waitlist/', join_waitlist, name='join-waitlist'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)