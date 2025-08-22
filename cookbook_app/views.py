from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout

from rest_framework import generics,filters,status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken




from .models import Recipe,UserProfile
from .serializers import RecipeSerializer,UserSerializer,UserLoginSerializer
from cookbook_app.pagination import RecipePagination




# Create your views here.
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset=Recipe.objects.all()
    serializer_class =RecipeSerializer
    pagination_class=RecipePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields=['title']
    order_fields=['-create_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(
                {"error": "No recipes found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().list(request, *args, **kwargs)
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Recipe.objects.all()
    serializer_class =RecipeSerializer

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
    
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Recipe deleted Successfully"})
    


class UserListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    pagination_class=RecipePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields=['title']


    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
   
    

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"User deleted Successfully"})


class UserLoginView(generics.GenericAPIView):
    serializer_class=UserLoginSerializer
    permission_classes=[AllowAny]

    def post(self,request,*args, **kwargs):

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "username":user.username,
                    
                }

            },status=status.HTTP_200_OK
        )
    
class SessionLogoutView(APIView):
    permission_class =permissions.IsAuthenticated

    def post(self,request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
        


        
            