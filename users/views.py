from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    }


class LoginView(APIView):
    permission_classes = [AllowAny]  # no auth needed to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response(
                {
                    "message": "Login successful",
                    "role":    data["role"],
                    "tokens":  {
                        "access": data["access"],
                        "refresh": data["refresh"],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]  # no auth needed to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response(
                {
                    "message": "Registration successful",
                    "role":    user.role,
                    "tokens":  tokens,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            # This will show you exactly what failed
            print(serializer.errors)  # Check your terminal/console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        