from django.shortcuts import render
from .models import Task
from .serializers import *
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
import io
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView

class StudentList(ListAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer


# Create your views here.
#model object - single student data

# def student_details(request):
#     try:
#         task = Task.objects.get(id=1)
#     except Task.DoesNotExist:
#         return JsonResponse({'error': 'Task not found'}, status=404)
    
#     serializer = TaskSerializer(task)
#     json_data = JSONRenderer().render(serializer.data)  # Corrected to use JSONRenderer as an instance
#     return JsonResponse(json_data, content_type='application/json')

# def student_details(request):
#     try:
#         task = Task.objects.get(id=1)
#     except Task.DoesNotExist:
#         return JsonResponse({'error': 'Task not found'}, status=404)
    
#     serializer = TaskSerializer(task)
#     # Directly return the data serialized by DRF serializer
#     return JsonResponse(serializer.data)

# from django.http import JsonResponse

# def student_create(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         serializer = TaskSerializer(data=pythondata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data created successfully'}
#             return JsonResponse(res)  # Return JSON response directly
#         else:
#             # Return errors if the data is invalid
#             return JsonResponse(serializer.errors, status=400)
    
#     # Handle non-POST requests (optional, depending on your requirements)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



# def Class_Info(request):
#     tasks = Class.objects.all()
#     serializer = ClassSerializer(tasks, many=True)  # Use many=True for lists
#     return JsonResponse(serializer.data, safe=False)






