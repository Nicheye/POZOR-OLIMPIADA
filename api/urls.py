
from django.urls import path, include,re_path

from .views import *
urlpatterns = [
      path('ping',Ping_View.as_view()),
	path('countries',Countries_View.as_view()),
	path('countries/<slug:alpha2>',Countries_View.as_view()),
	re_path('countries/(?P<region>.+)/$',Countries_View.as_view()),
	path('me/profile',Profile_View.as_view()),
	path('profiles/<slug:login>',Profiles_Viewer_View.as_view()),
	path('me/updatePassword',ChangePasswordView.as_view()),
	path('friends',Friend_View.as_view()),
	path('friends/<int:friend_id>',Friend_View.as_view()),
	path('posts/new',Publication_View.as_view()),
	path('posts/<int:postId>',Publication_View.as_view()),
	path('posts/feed/<slug:login>',Feed_View.as_view()),
	path('post/like/<int:post_id>',Like_View.as_view()),
	path('post/dislike/<int:post_id>',DisLike_View.as_view()),
	
      
]