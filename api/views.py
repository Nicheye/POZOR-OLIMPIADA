
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import Country_serializer,ChangePasswordSerializer,Publication_Serializer
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from authentification.serializers import UserSerializer,Friend_Link_Serializer
from authentification.models import User,Friend_Link
from django.utils import timezone

class Ping_View(APIView):
	def get(self,request):
		return Response({"message":"ok"}, status=status.HTTP_200_OK)
		
class Countries_View(APIView):
	def get(self,request,*args,**kwargs):
		try:
			alpha2 = kwargs.get("alpha2",None)
			if alpha2 is not None:
				try:
					qs= Country.objects.get(alpha2=alpha2)
					qs_ser = Country_serializer(qs)
					return Response({'country':qs_ser.data},status=status.HTTP_200_OK)
				except:
					return Response({'country':"not found"},status=status.HTTP_404_NOT_FOUND)
			region = kwargs.get("region",None)
			if region:
					qs = Country.objects.filter(region=region)
					qs_ser = Country_serializer(qs, many=True)
					return Response({'countries': qs_ser.data}, status=status.HTTP_200_OK)
			qs=Country.objects.all()
			qs_ser =Country_serializer(qs,many=True)
			return Response({"countries":qs_ser.data},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Profile_View(APIView):
	permission_classes = [IsAuthenticated,]
	def get(self,request):
		try:
			user = request.user
			user_ser = UserSerializer(user)
			return Response({"profile":user_ser.data},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	def patch(self,request):
		try:
			user = request.user
			data = request.data
			if 'name' in data and data['name'] !="":
				user.name = data['name']
				user.save()
			if 'last_name' in data and data['last_name'] !="":
				user.last_name = data['last_name']
				user.save()
			if 'age' in data and data['age'] !="":
				user.last_name = data['age']
				user.save()
			
			user_ser=  UserSerializer(user)
			return Response({"profile":user_ser.data})

		except Exception as e:
			return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Profiles_Viewer_View(APIView):
	def get(self,request,*args,**kwargs):
		try:
			login = kwargs.get('login',None)
			if login is not None:
				user_obj = User.objects.get(username=login,isPublic=True)
				user_ser = UserSerializer(user_obj)
				return Response({'user':user_ser.data},status=status.HTTP_302_FOUND)
		except Exception as e:
			return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            user = request.user
            user.last_friend_added_at = timezone.now()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
from rest_framework.pagination import LimitOffsetPagination

class FriendPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class Friend_View(APIView):
    pagination_class = FriendPagination
    permission_classes = [IsAuthenticated,]
	
    def get(self, request):
        try:
            user = request.user
            friends = Friend_Link.objects.filter(creator=user).order_by('-created_at')
            paginator = self.pagination_class()
            paginated_friends = paginator.paginate_queryset(friends, request)
            friends_ser = Friend_Link_Serializer(paginated_friends, many=True)
            return paginator.get_paginated_response({'friends': friends_ser.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            friend_id = kwargs.get("friend_id")
            user = request.user

            if friend_id is not None:

                friend_obj = User.objects.get(id=friend_id)

                if friend_obj != user:
                    if not Friend_Link.objects.filter(creator=user, receiver=friend_obj).exists():
                        friend_link_obj = Friend_Link.objects.create(creator=user, receiver=friend_obj)
                        ser = Friend_Link_Serializer(friend_link_obj)
                        return Response({"friend": ser.data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message': "Friend link already exists."}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'message': "Friend id is required."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': "User with the specified id does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            friend_id = kwargs.get("friend_id", None)
            user = request.user
            if friend_id is not None:
                friend_obj = User.objects.get(id=friend_id)
                link = Friend_Link.objects.get(creator=user, receiver=friend_obj)
                if link:
                    link.delete()
                return Response({'message': "successfully deleted"})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)


class Publication_View(APIView):
	permission_classes = [IsAuthenticated]
	def get(self,request,*args,**kwargs):
		try:
				user = request.user
				my_posts = Publication.objects.filter(created_by=user)
				public_posts = Publication.objects.filter(created_by__isPublic=True)
				friends = Friend_Link.objects.filter(receiver=user)
				
				# Using union() to combine QuerySets
				friends_posts = Publication.objects.none()  # Initialize an empty QuerySet
				for friend in friends:
					friend_post = Publication.objects.filter(created_by=friend.creator)
					friends_posts = friends_posts.union(friend_post)

				all_posts = my_posts.union(public_posts, friends_posts,my_posts)
				
				id = kwargs.get("postId",None)
				if id is not None:
					pub_obj = Publication.objects.get(id=id)
					if pub_obj in all_posts:
						pub_ser = Publication_Serializer(pub_obj)
						
						return Response({"posts":pub_ser.data},status=status.HTTP_202_ACCEPTED)
					else:
						return Response({"posts":"ur noot allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
		except Exception as e:
				return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)
	def post(self,request):
		try:
			data = request.data
			pub_ser = Publication_Serializer(data=data)
			if pub_ser.is_valid(raise_exception=True):
				pub_ser.save(created_by=request.user)
				return Response({"post":pub_ser.data})
		except Exception as e:
				return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)
	
class FeedPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class Feed_View(APIView):
	pagination_class = FeedPagination
	permission_classes = [IsAuthenticated,]
	def get(self,request,*args,**kwargs):
		try:
				login = kwargs.get("login",None)
				if login is not None:
					if login == "my":
						user = request.user
						my_posts = Publication.objects.filter(created_by=user)
						paginator = self.pagination_class()
						paginated_posts = paginator.paginate_queryset(my_posts, request)
						posts_ser = Publication_Serializer(paginated_posts, many=True)
						return paginator.get_paginated_response({'posts': posts_ser.data})
						
					else:
						creator = User.objects.get(username=login)
						my_posts = Publication.objects.filter(created_by=creator)
						paginator = self.pagination_class()
						paginated_posts = paginator.paginate_queryset(my_posts, request)
						posts_ser = Publication_Serializer(paginated_posts, many=True)
						return paginator.get_paginated_response({'posts': posts_ser.data})

		except Exception as e:
				return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)
	
class Like_View(APIView):
	permission_classes = [IsAuthenticated]
	def get(self,request,*args,**kwargs):
		try:
				user = request.user
				my_posts = Publication.objects.filter(created_by=user)
				public_posts = Publication.objects.filter(created_by__isPublic=True)
				friends = Friend_Link.objects.filter(receiver=user)
				
				# Using union() to combine QuerySets
				friends_posts = Publication.objects.none()  # Initialize an empty QuerySet
				for friend in friends:
					friend_post = Publication.objects.filter(created_by=friend.creator)
					friends_posts = friends_posts.union(friend_post)

				all_posts = my_posts.union(public_posts, friends_posts,my_posts)
				
				id = kwargs.get("post_id",None)
				if id is not None:
					pub_obj = Publication.objects.get(id=id)
					if pub_obj in all_posts:
						pub_ser = Publication_Serializer(pub_obj)
						likes = Like.objects.filter(pub=pub_obj,user=user)
						dislikes = DisLike.objects.filter(pub=pub_obj,user=user)
						for like in likes:
							like.delete()
							pub_obj.likesCount-=1
						for dislike in dislikes:
							dislike.delete()
							pub_obj.dislikesCount-=1	
						new_like_obj = Like.objects.create(pub=pub_obj,user=user)
						pub_obj.likesCount+=1
						pub_obj.save()
						return Response({"posts":pub_ser.data},status=status.HTTP_202_ACCEPTED)
					else:
						return Response({"posts":"ur noot allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
		except Exception as e:
				return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)


class DisLike_View(APIView):
	permission_classes = [IsAuthenticated]
	def get(self,request,*args,**kwargs):
		try:
				user = request.user
				my_posts = Publication.objects.filter(created_by=user)
				public_posts = Publication.objects.filter(created_by__isPublic=True)
				friends = Friend_Link.objects.filter(receiver=user)
				
				# Using union() to combine QuerySets
				friends_posts = Publication.objects.none()  # Initialize an empty QuerySet
				for friend in friends:
					friend_post = Publication.objects.filter(created_by=friend.creator)
					friends_posts = friends_posts.union(friend_post)

				all_posts = my_posts.union(public_posts, friends_posts,my_posts)
				
				id = kwargs.get("post_id",None)
				if id is not None:
					pub_obj = Publication.objects.get(id=id)
					if pub_obj in all_posts:
						pub_ser = Publication_Serializer(pub_obj)
						likes = Like.objects.filter(pub=pub_obj,user=user)
						dislikes = DisLike.objects.filter(pub=pub_obj,user=user)
						for like in likes:
							like.delete()
							pub_obj.likesCount-=1
						for dislike in dislikes:
							dislike.delete()
							pub_obj.dislikesCount-=1	
						new_dislike_obj = DisLike.objects.create(pub=pub_obj,user=user)
						pub_obj.dislikesCount+=1
						pub_obj.save()
						return Response({"posts":pub_ser.data},status=status.HTTP_202_ACCEPTED)
					else:
						return Response({"posts":"ur noot allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
		except Exception as e:
				return Response({'error': str(e)}, status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)