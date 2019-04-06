from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .views import Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id','first_name','last_name','date_of_birth','date_of_death')
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','email','groups')
        
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')