from django.urls import path
from .views import RecipeListCreateView,RecipeRetrieveUpdateDestroyView,SessionLogoutView,UserLoginView
from .views import UserListCreateView, UserRetrieveUpdateDestroyView

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(),name='List-Create'),
    path('recipes/<int:pk>/',RecipeRetrieveUpdateDestroyView.as_view(),name='retrieve-update-delete'),
    

    path("user/login/", UserLoginView.as_view(), name="token_obtain_pair"),
    path("logout/",SessionLogoutView.as_view(),name='logout'),
   
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
]
