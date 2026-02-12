from authapp.models import User
from rest_framework_mongoengine.serializers import DocumentSerializer

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields =('id', 'email', 'username','created_at')