from django.shortcuts import render
from .models import Task
from .serializers import *
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

class students_deatils(APIView):
    def get(self,request):
        queryset=Task.objects.all() .order_by('-pk')
        serializer=TaskSerializer(queryset,many=True)
        return Response({
            'data':serializer.data
        })

    def post(self,request):
        data=request.data
        serializer=TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data saved','data':serializer.data})
        else:
            return Response({
                'msg':'data not saved',
                'errors':serializer.errors,
            })
       
    def put(self,request):
        data=request.data
        if not data.get('id'):
           return Response({
               'message':'data is not update',
               'errors':'id is required'
           })
        details=Task.objects.get(id=data.get('id'))
        serializer=TaskSerializer(details,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg':'data upadate',
                'data':serializer.data
            })
        else:
            return Response({
                'msg':'data not update',
                'errors':'validation failed'

            })
       
    
    def patch(self,request):
        data=request.data
        if not data.get('id'):
            return Response({
                'message':'data not updated',
                'errors':'id is required'
            })
        details=Task.objects.get(id=data.get('id'))
        serializer=TaskSerializer(details,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg':'data updated',
                'data':serializer.data
            })
        else:
            return Response({
                'msg':'data is not valid',
                'errors':'data validation failed'
            })
        
    
    def delete(self,request):
        data=request.data
        if not data.get('id'):
            return Response({
                'msg':'data is not deleted',
                'errors':'id is needed'
            })
        details=Task.objects.get(id=data.get('id')).delete()
        return Response({'msg':'data id deleted','data':{}})








