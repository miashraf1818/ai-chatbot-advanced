"""
User Authentication Views
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserSerializer


class RegisterView(APIView):
    """
    User Registration with proper validation and error handling
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Create user
                user = serializer.save()

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                return Response({
                    'success': True,
                    'message': 'Registration successful! Welcome aboard! 🎉',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Handle any unexpected errors during user creation
                return Response({
                    'success': False,
                    'error': 'Registration failed. Please try again.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return validation errors with proper format
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    User Login with proper error handling
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Get username and password from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate input
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Username and password required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginView(APIView):
    """Google OAuth Login with detailed error logging"""
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get('credential')

        # Debug logging
        print(f"🔍 Received credential: {credential[:50]}..." if credential else "❌ No credential received")

        if not credential:
            return Response({
                'success': False,
                'message': 'Credential required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Import here to catch import errors
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests

            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                '329644175819-3f0cqiaqq4vnrrtuhcv7n2beh40t9t5v.apps.googleusercontent.com'
            )

            print(f"✅ Token verified! Email: {idinfo.get('email')}")

            # Get user info from Google
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # Check if user exists
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            print(f"{'🆕 Created' if created else '👤 Found'} user: {user.username}")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'success': True,
                'message': 'Google login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        except ImportError as e:
            print(f"❌ IMPORT ERROR: {str(e)}")
            print("⚠️ Run: pip install google-auth google-auth-oauthlib google-auth-httplib2")
            return Response({
                'success': False,
                'message': 'Google auth library not installed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError as e:
            print(f"❌ VALUE ERROR: {str(e)}")
            return Response({
                'success': False,
                'message': 'Invalid Google token'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {str(e)}")
            return Response({
                'success': False,
                'message': f'Google login failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get Current User Profile"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """User Logout (Blacklist Token)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'success': False,
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
