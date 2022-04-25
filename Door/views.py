import os
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Door.models import *
from Door.serializers import *

from datetime import date
from django.shortcuts import render

from .form import ImageForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage


  
  
class Image_recognize_view(APIView):
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return JsonResponse({
                'message': 'Upload successful!'
            }, status=status.HTTP_201_CREATED)

class ListCreateDoorView(ListCreateAPIView):
    model = Door
    serializer_class = DoorSerializer

    def get_queryset(self):
        return Door.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DoorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Door successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Door unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteDoorView(RetrieveUpdateDestroyAPIView):
    model = Door
    serializer_class = DoorSerializer

    def put(self, request, *args, **kwargs):
        Door = get_object_or_404(Door, id=kwargs.get('pk'))
        serializer = DoorSerializer(Door, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Door successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Door unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Door = get_object_or_404(Door, id=kwargs.get('pk'))
        Door.delete()

        return JsonResponse({
            'message': 'Delete Door successful!'
        }, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)
# class RecognizeAPIView(generics.CreateAPIView):
#     class_id_param = openapi.Parameter(
#         'class_id', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
#     )

#     @swagger_auto_schema(manual_parameters=[class_id_param])
#     def get(self, request, *args, **kwargs):
#         class_id: int = int(request.query_params['class_id'])

#         today: date = date.today()
#         course: Classes = Classes.objects.get(pk=class_id)
#         date_class: Dates_Class = {}

#         try:
#             date_class = Dates_Class.objects.get(date=today, course=course)
#         except Dates_Class.DoesNotExist:
#             date_class = Dates_Class.objects.create(date=today, course=course)



#         for i in range(4):
#             # Get image from rasp
#             img_contain_dir = str(os.path.abspath(os.getcwd())) + '/img/'
#             img_path = get_image_from_rasp(img_contain_dir)

# #          current_path: str = str(os.path.abspath(os.getcwd()))  # .../pbl5-api
# #          img_path: str = current_path + '/dataset/test/HQT/9.jpg'

#             # Recognize and get ids
#             recognized_face_ids: [int] = recognize_students_in_image(img_path)
#             print(recognized_face_ids)

#             # Update to database
#             for user_id in recognized_face_ids:
#                 student: Users = Users.objects.get(pk=user_id)

#                 exist_attendances: StudentAttending = StudentAttending.objects.filter(
#                     student__pk=user_id, dateClass__pk=date_class.id
#                 ).count()

#                 if exist_attendances == 0:
#                     print(user_id, 'not exist')
#                     StudentAttending.objects.create(
#                         isAttending=True, dateClass=date_class, student=student
#                     )

# return Response()