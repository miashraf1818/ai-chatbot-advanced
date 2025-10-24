from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from apps.users.api.serializers import UserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import sys


class GoogleLoginView(APIView):
    """Google OAuth Login - Fixed Version"""
    permission_classes = [AllowAny]

    def post(self, request):
        # FIXED: Changed from 'access_token' to 'credential'
        credential = request.data.get('credential')

        # Debug logging
        print("=" * 80, file=sys.stderr)
        print("🔍 GOOGLE LOGIN ATTEMPT", file=sys.stderr)
        print(f"📦 Request data keys: {list(request.data.keys())}", file=sys.stderr)
        print(f"🎫 Credential present: {credential is not None}", file=sys.stderr)

        if not credential:
            print("❌ NO CREDENTIAL PROVIDED", file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            return Response({
                'success': False,
                'error': 'Credential required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("🔐 Verifying Google token...", file=sys.stderr)

            # FIXED: Updated to new Client ID
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                '89771009227-e4ca190m73gj3nkb4qboeqovauno5koi.apps.googleusercontent.com'

            )

            # Get user info from token
            email = idinfo.get('email')
            google_id = idinfo.get('sub')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            print(f"✅ Token verified! Email: {email}", file=sys.stderr)

            if not email or not google_id:
                print("❌ Invalid token data", file=sys.stderr)
                print("=" * 80, file=sys.stderr)
                return Response({
                    'success': False,
                    'error': 'Invalid token data'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Try to find existing user by email
            try:
                user = User.objects.get(email=email)
                print(f"👤 Found existing user: {user.username}", file=sys.stderr)
            except User.DoesNotExist:
                # Create new user
                print(f"🆕 Creating new user for {email}", file=sys.stderr)
                username = email.split('@')[0]
                base_username = username
                counter = 1

                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                print(f"✅ Created user: {user.username}", file=sys.stderr)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            print("🎉 Google login successful!", file=sys.stderr)
            print("=" * 80, file=sys.stderr)

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

        except ValueError as e:
            print(f"❌ VALUE ERROR: {str(e)}", file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            return Response({
                'success': False,
                'error': f'Invalid Google token: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            return Response({
                'success': False,
                'error': f'Google login failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
