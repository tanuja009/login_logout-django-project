from rest_framework import serializers
from rest_framework.views import APIView
from .models import *
# class TaskSerializer(serializers.Serializer):
#     name=serializers.CharField(max_length=100)
#     roll=serializers.IntegerField()
#     city=serializers.CharField(max_length=100)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['name','roll','city']



    

# class ClassSerializer(serializers.Serializer):
#     class_name=serializers.CharField(max_length=50)
#     section=serializers.CharField(max_length=50)
#     url=serializers.URLField(allow_blank=True,required=False)

     