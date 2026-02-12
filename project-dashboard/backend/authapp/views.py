from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authapp.models import User
from authapp.serializers import UserSerializer

def validate_keys(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return Response(
            {
                'message': 'missing required fields',
                'missing_fields': missing_keys
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return None

class RegisterView(APIView):
    def post(self, request):
        data=request.data or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        required_keys = ['username', 'email', 'password', 'confirm_password']

        # Validate required fields
        validation_response = validate_keys(data, required_keys)
        if validation_response:
            return validation_response
        if password != confirm_password:
            return Response({'message': 'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects(email=email).first():
            return Response({'message': 'email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects(username=username).first():
            return Response({'message': 'username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        user = User()

        try:
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
        except Exception as e:
            return Response({'message': 'registration failed', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'registration successful'}, status=status.HTTP_201_CREATED)
    


class LoginView(APIView):
    def post(self, request):
        data=request.data or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Must have either username or email, and password
        if not password:
            return Response({'message': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not username and not email:
            return Response({'message': 'username or email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to find user by username or email
        user = None
        if username:
            user = User.objects(username=username).first()
        elif email:
            user = User.objects(email=email).first()
            
        if not user or not user.check_password(password):
            return Response({'message': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user)
        return Response({'message': 'login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
        