
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [
     
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register',RegisterView.as_view()),
      path('sign-in', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('sign-in/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
]