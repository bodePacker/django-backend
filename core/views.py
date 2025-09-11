from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

from .models import MyUser, KeyboardMapping
from .serializers import MyUserProfileSeralizer, KeyboardMappingSerializer, RegisterUserSerializer, WaitlistSerializer

@api_view(['POST'])
@permission_classes([])
def join_waitlist(request):
    try:
        serializer = WaitlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully joined waitlist'}, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile_data(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error':'user does not exist'})
        serializer = MyUserProfileSeralizer(user, many=False)
        return Response(serializer.data)
    except:
        return Response({'error':'error getting user data'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_mappings(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error':'user does not exist'})
        
        # Get all mappings for the user
        mappings = KeyboardMapping.objects.filter(user=user)
        serializer = KeyboardMappingSerializer(mappings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'error getting user mappings: {str(e)}'})
    
@api_view(['GET'])
@permission_classes([])
def get_specific_mapping(request, mapping_id):
    try:
        mapping = KeyboardMapping.objects.get(id=mapping_id)
        # Check if mapping is public or user owns it
        if not mapping.is_public:
            # If mapping is private, user must be authenticated and own it
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required for private mappings'}, status=401)
            if mapping.user != request.user:
                return Response({'error': 'Access denied - you do not own this mapping'}, status=403)
        
        serializer = KeyboardMappingSerializer(mapping)
        return Response(serializer.data)
    except KeyboardMapping.DoesNotExist:
        return Response({'error': 'Mapping not found'}, status=404)
    except Exception as e:
        return Response({'error': f'error getting mapping: {str(e)}'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_mapping(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=404)
        
        # Create new mapping
        mapping_data = {
            'user': user,
            'name': request.data.get('name'),
            'description': request.data.get('description', ''),
            'mappings': request.data.get('mappings', {}),
            'is_active': request.data.get('is_active', False),
            'tags': request.data.get('tags', [])
        }
        
        mapping = KeyboardMapping.objects.create(**mapping_data)
        serializer = KeyboardMappingSerializer(mapping)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'error': f'error creating mapping: {str(e)}'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_mapping(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=404)
        
        mapping_id = request.data.get('mapping_id')
        if not mapping_id:
            return Response({'error': 'mapping_id is required'}, status=400)
            
        try:
            mapping = KeyboardMapping.objects.get(id=mapping_id, user=user)
            mapping.delete()
            return Response({'message': 'Mapping deleted successfully'}, status=200)
        except KeyboardMapping.DoesNotExist:
            return Response({'error': 'mapping not found'}, status=404)
            
    except Exception as e:
        return Response({'error': f'error deleting mapping: {str(e)}'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_active_mapping(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=404)
        
        mapping_id = request.data.get('mapping_id')
        if not mapping_id:
            return Response({'error': 'mapping_id is required'}, status=400)
            
        try:
            # First, set all user's mappings to inactive
            KeyboardMapping.objects.filter(user=user).update(is_active=False)
            
            # Then set the selected mapping to active
            mapping = KeyboardMapping.objects.get(id=mapping_id, user=user)
            mapping.is_active = True
            mapping.save()
            
            return Response({'message': 'Mapping set as active successfully'}, status=200)
        except KeyboardMapping.DoesNotExist:
            return Response({'error': 'mapping not found'}, status=404)
            
    except Exception as e:
        return Response({'error': f'error setting active mapping: {str(e)}'}, status=400)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_tags(request, mapping_id):
    try:
        mapping = KeyboardMapping.objects.get(id=mapping_id)
        mapping.tags = request.data.get('tags', [])
        mapping.save()
        return Response({'message': 'Tags added successfully'}, status=200)
    except Exception as e:
        return Response({'error': f'error adding tags: {str(e)}'}, status=400)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_mapping(request, mapping_id):
    try:
        mapping = KeyboardMapping.objects.get(id=mapping_id)
        mapping.name = request.data.get('name', '')
        mapping.save()
        return Response({'message': 'Mapping renamed successfully'}, status=200)
    except Exception as e:
        return Response({'error': f'error renaming mapping: {str(e)}'}, status=400)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_mapping_visibility(request, mapping_id):
    try:
        mapping = KeyboardMapping.objects.get(id=mapping_id)
        mapping.is_public = request.data.get('is_public')
        mapping.save()
        return Response({'message': 'Mapping visibility updated successfully'}, status=200)
    except Exception as e:
        return Response({'error': f'error updating mapping visibility: {str(e)}'}, status=400)

# Community
@api_view(['GET'])
@permission_classes([])
def get_all_community_mappings(request):
    try:
        mappings = KeyboardMapping.objects.filter(is_public=True)
        serializer = KeyboardMappingSerializer(mappings, many=True)
        return Response(serializer.data)
    except:
        return Response({'error':'error getting user data'})


# Login and register
@api_view(['POST'])
@authentication_classes([])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Check if username already exists
            username = request.data.get('username')
            if MyUser.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=400)
                
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': f'Registration failed: {str(e)}'}, status=400)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticated(request):
    return Response('authenticated')

class CustomTokenObtainParView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']
            username = request.data['username']
            
            try:
                user = MyUser.objects.get(username=username)
            except MyUser.DoesNotExist:
                return Response({'error':'user does not exist'})
            
            # Return tokens in response body
            return Response({
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "username": user.username,
                    "email": user.email,
                }
            })
        except Exception as e:
            print(f"Login error: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            # Get refresh token from request body
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=400)
            
            # Standard refresh process
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            
            # Return new access token in response body
            return Response({
                "success": True,
                "access_token": access_token,
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)

class ElectronTokenObtainView(TokenObtainPairView):
    """
    Custom token view for Electron app that provides extended refresh tokens
    """
    def post(self, request, *args, **kwargs):
        try:
            # Verify this is coming from Electron app
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            client_type = request.data.get('client_type', '')
            
            # Check if request is from Electron app
            is_electron = 'electron' in user_agent.lower() or client_type == 'electron'
            
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return Response({'error': 'Username and password are required'}, status=400)
            
            try:
                user = MyUser.objects.get(username=username)
            except MyUser.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=401)
            
            # Verify password
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=401)
            
            # Create tokens
            refresh = RefreshToken.for_user(user)
            
            # Set extended lifetime for Electron app
            if is_electron:
                # Set refresh token to last 30 days for Electron
                refresh.set_exp(lifetime=timedelta(days=30))
            
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "token_type": "electron_extended" if is_electron else "standard"
            })
            
        except Exception as e:
            print(f"Electron login error: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)

class ElectronTokenRefreshView(TokenRefreshView):
    """
    Custom refresh view for Electron app that maintains extended refresh token lifetime
    """
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            client_type = request.data.get('client_type', '')
            
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=400)
            
            # Verify this is from Electron
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            is_electron = 'electron' in user_agent.lower() or client_type == 'electron'
            
            try:
                # Decode the refresh token to get user
                token = RefreshToken(refresh_token)
                username = token.get('username')
                
                if not username:
                    return Response({'error': 'Invalid refresh token'}, status=401)
                
                try:
                    user = MyUser.objects.get(username=username)
                except MyUser.DoesNotExist:
                    return Response({'error': 'User not found'}, status=401)
                
                # Create new tokens
                new_refresh = RefreshToken.for_user(user)
                
                # Set extended lifetime for Electron app
                if is_electron:
                    new_refresh.set_exp(lifetime=timedelta(days=30))
                
                new_access_token = str(new_refresh.access_token)
                new_refresh_token = str(new_refresh)
                
                # # Blacklist the old refresh token
                # token.blacklist()
                
                return Response({
                    "success": True,
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "token_type": "electron_extended" if is_electron else "standard"
                })
                
            except Exception as token_error:
                return Response({'error': 'Invalid or expired refresh token'}, status=401)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
