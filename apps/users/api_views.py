from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farms.models import CropHistory, Farm, Field
from apps.recommendations.models import Recommendation

from .models import UserProfile
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class CsrfTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        preferred_language = data.get('preferred_language', 'en')
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')

        errors = {}
        if not username:
            errors['username'] = ['This field is required.']
        elif User.objects.filter(username=username).exists():
            errors['username'] = ['A user with that username already exists.']

        if not email:
            errors['email'] = ['This field is required.']
        elif User.objects.filter(email=email).exists():
            errors['email'] = ['A user with that email already exists.']

        if not password:
            errors['password'] = ['This field is required.']
        elif len(password) < 8:
            errors['password'] = ['Password must be at least 8 characters.']

        if password and password != confirm_password:
            errors['confirm_password'] = ['Passwords do not match.']

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        UserProfile.objects.create(
            user=user,
            phone=phone,
            preferred_language=preferred_language,
        )
        login(request, user)
        return Response({'detail': 'Account created successfully.'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        UserProfile.objects.get_or_create(user=user)
        return Response({'detail': 'Login successful.'})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
        )

        UserProfile.objects.create(
            user=user,
            phone=serializer.validated_data.get('phone', ''),
            preferred_language=serializer.validated_data.get('preferred_language', 'en'),
        )

        return Response({'detail': 'Account created successfully.'}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful.'})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        farms = Farm.objects.filter(user=request.user)
        fields = Field.objects.filter(farm__user=request.user)
        recommendations = Recommendation.objects.filter(user=request.user)
        crop_history = CropHistory.objects.filter(field__farm__user=request.user)
        recent = recommendations.order_by('-created_at')[:5]

        recent_items = [
            {
                'id': item.id,
                'fieldName': item.field.name,
                'cropName': item.crop_name,
                'confidenceScore': float(item.confidence_score),
                'createdAt': item.created_at,
            }
            for item in recent
        ]

        return Response(
            {
                'totalFarms': farms.count(),
                'totalFields': fields.count(),
                'totalRecommendations': recommendations.count(),
                'totalCropHistory': crop_history.count(),
                'recentRecommendations': recent_items,
            }
        )
