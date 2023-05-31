# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .enums import ADMIN
from .models import UserProfile, Image
from .serializers import UserProfileSerializer, ImageSerializer, CustomTokenObtainPairSerializer, \
    UserProfileListSerializer
from .utils import add_watermark_to_image


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileListSerializer
        return UserProfileSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user_obj = None
        try:
            user_obj = User.objects.create(username=username, email=email, password=password)

            request_data = request.data
            request_data.pop("username")
            request_data.pop("email")
            request_data.pop("password")
            request_data.update({"user": user_obj.id})

            serialized_data = UserProfileSerializer(data=request_data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()

        except Exception as e:
            if user_obj:
                user_obj.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "user created"}, status=status.HTTP_201_CREATED)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        original_link = request.data.get('original_link')

        if not original_link:
            Response({"error": "please provide image link on which logo to be added"},
                     status=status.HTTP_400_BAD_REQUEST)

        edited_link = add_watermark_to_image(original_link)

        request.data['edited_link'] = edited_link

        return super().create(request, *args, **kwargs)

    @action(methods=["GET"], detail=False)
    def list_edited_image_of_a_user(self, request, *args, **kwargs):

        current_user_id = request.query_params.get('admin_user_id')

        try:
            admin_profile = UserProfile.objects.get(role=ADMIN, id=current_user_id)
        except Exception as e:
            return Response({"error": "current user does not exists or not a admin"},
                     status=status.HTTP_400_BAD_REQUEST)

        requested_user_id = request.query_params.get('requested_user_id')

        try:
            user_profile = UserProfile.objects.get(id=requested_user_id)
        except Exception as e:
            return Response({"error": "requested user does not exists"},
                     status=status.HTTP_400_BAD_REQUEST)

        user_image_qs = user_profile.image_set.all()

        serialized_data = ImageSerializer(user_image_qs, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer






