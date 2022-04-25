from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Door import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register',views.UserRegisterView.as_view(), name='register'),
    path('Doors', views.ListCreateDoorView.as_view()),
    path('Doors/<int:pk>', views.UpdateDeleteDoorView.as_view()),
    path('image_upload', views.Image_recognize_view.as_view()),

    # path('recognizes', views.RecognizeAPIView.as_view()),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)