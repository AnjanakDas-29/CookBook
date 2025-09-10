from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import RecipeListCreateView,RecipeRetrieveUpdateDestroyView,SessionLogoutView,UserLoginView
from .views import UserRegisterView, UserRetrieveUpdateDestroyView,UserListCreate

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(),name='List-Create'),
    path('recipes/<int:pk>/',RecipeRetrieveUpdateDestroyView.as_view(),name='retrieve-update-delete'),
    

    path("user/login/", UserLoginView.as_view(), name="token_obtain_pair"),
    path("logout/",SessionLogoutView.as_view(),name='logout'),
   
    path("users/", UserRegisterView.as_view(), name="user-register"),
    path("users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),

    path("userlist/",UserListCreate.as_view(),name="user-list-create"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
