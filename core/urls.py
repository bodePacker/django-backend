from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_user_profile_data, get_user_mappings, create_mapping
app_name = 'core'

urlpatterns = [
    path('users/<str:pk>', get_user_profile_data, name='user-profile'),
    
    # Keyboard mapping endpoints
    path('users/<str:pk>/mappings', get_user_mappings, name='list-mappings'),
    path('users/<str:pk>/mappings/new', create_mapping, name='create-mapping'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)