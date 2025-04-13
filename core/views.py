from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MyUser, KeyboardMapping
from .serializers import MyUserProfileSeralizer, KeyboardMappingSerializer

@api_view(['GET'])
def get_user_profile_data(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error':'user does not exist'})
        seralizer = MyUserProfileSeralizer(user, many=False)
        return Response(seralizer.data)
    except:
        return Response({'error':'error getting user data'})


@api_view(['GET'])
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
    

@api_view(['POST'])
def create_mapping(request, pk):
    try:
        try:
            user = MyUser.objects.get(username=pk)
        except MyUser.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=404)
        
        # Create new mapping
        mapping_data = {
            'user': user,
            'mappings': request.data.get('mappings', {}),
            'is_active': request.data.get('is_active', False)
        }
        
        mapping = KeyboardMapping.objects.create(**mapping_data)
        serializer = KeyboardMappingSerializer(mapping)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'error': f'error creating mapping: {str(e)}'}, status=400)