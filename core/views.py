from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


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
        serializer = KeyboardMappingSerializer(mapping)
        return Response(serializer.data)
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

# Community
@api_view(['GET'])
@authentication_classes([])
def get_all_community_mappings(request):
    try:
        # TODO: Change this to true
        mappings = KeyboardMapping.objects.filter(is_public=False)
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
            
            res = Response()
            
            res.data = {
                "success": True,
                "user": {
                    "username": user.username,
                    "email": user.email,
                }
            }

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            return res
        except Exception as e:
            print(f"Login error: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
        

class CustomTokenRefreshView(TokenRefreshView):
    def post (self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

        
            res = Response()

            res.data = {
            "success": True,
            }

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            return res
        except:
            return Response({'success':False})
