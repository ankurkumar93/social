from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserLoginSerializer 
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, UserFollower, Post, LikePost, CommentPost
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import TokenAuthentication
from django.db.models import F, Q


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        accessToken = AccessToken.for_user(request.user)
        accessToken['id'] = user.id
        return Response({"Message": "Success", 'token':str(accessToken)}, status=status.HTTP_200_OK)
        

class FollowUserView(APIView):

    def post(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        if str(tokeUserId) == str(id):
            return Response({'message':'You can not follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=str(id))
        except Exception as e:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        allValues = UserFollower.objects.filter(followee=id).values_list('follower', flat=True)
        if tokeUserId in allValues:
            return Response({'message':'You are already following the user'}, status=status.HTTP_400_BAD_REQUEST)
        follwerIns = User.objects.get(id=tokeUserId)
        follweeIns = User.objects.get(id=id)
        UserFollower.objects.create(follower=follwerIns, followee=follweeIns)
        return Response({"Message":"Successfully followed"}, status=status.HTTP_200_OK)


class UnFollowUserView(APIView):

    def post(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        if str(tokeUserId) == str(id):
            return Response({'message':'You can not unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=str(id))
        except:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        followInst = UserFollower.objects.filter(Q(follower_id=tokeUserId) and Q(followee_id=id)).delete()
        return Response({"Message":"Successfully unfollowed"}, status=status.HTTP_200_OK)

    
class GetUserView(APIView):

    def get(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        try:
            user = User.objects.get(id=str(id))
        except:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        userData = {}
        followers = UserFollower.objects.filter(followee_id=id).count()
        followings = UserFollower.objects.filter(follower_id=id).count()
        userData['name'] = user.name
        userData['followers'] = followers
        userData['followings'] = followings
        return Response({"data":userData}, status=status.HTTP_200_OK)


class PostView(APIView):

    def post(self, request):
        title = request.data['title']
        desc = request.data['desc']
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        userInst = User.objects.get(id=tokeUserId)
        postIns = Post.objects.create(user=userInst, title=title, desc=desc, date=datetime.now())
        data = {
            'id': postIns.id,
            'title':title,
            'description':desc,
            'created time': datetime.now()
        }
        return Response({"Message": "Success", 'data':data}, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        try:
            postIns = Post.objects.get(id=id)
        except:
            return Response({"Message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        if str(postIns.user.id) != str(tokeUserId):
            return Response({"Message":"You can not delete posts by others"}, status=status.HTTP_403_FORBIDDEN)
        postIns.delete()
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)


class LikePostView(APIView):
    
    def post(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"}, status=status.HTTP_403_FORBIDDEN)
        tokeUserId = accessTokenData['id']
        try:
            postIns = Post.objects.get(id=id)
        except:
            return Response({"Message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        allValues = LikePost.objects.filter(post_id=id).values_list('user_id', flat=True)
        if tokeUserId in allValues:
            return Response({'message':'You have liked the post already'}, status=status.HTTP_400_BAD_REQUEST)
        userInst = User.objects.get(id=tokeUserId)
        LikePost.objects.create(post_id=postIns, user_id=userInst)
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)


class UnLikePostView(APIView):

    def post(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"})
        tokeUserId = accessTokenData['id']
        try:
            post = Post.objects.get(id=str(id))
        except:
            return Response({'message':'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        followInst = LikePost.objects.filter(Q(post_id=id) and Q(user_id=tokeUserId)).delete()
        return Response({"Message":"Successfully unliked post"}, status=status.HTTP_200_OK)


class CommentPostView(APIView):

    def post(self, request, id):
        comment = request.data['comment']
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"})
        tokeUserId = accessTokenData['id']
        try:
            postIns = Post.objects.get(id=str(id))
        except:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        userIns = User.objects.get(id=tokeUserId)
        comment = CommentPost.objects.create(comment_text=comment, post_id=postIns,user_id=userIns)
        return Response({"comment Id":comment.id}, status=status.HTTP_201_CREATED)


class GetPostView(APIView):

    def get(self, request, id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"})
        tokeUserId = accessTokenData['id']
        try:
            postIns = Post.objects.get(id=str(id))
        except:
            return Response({'message':'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        likes = LikePost.objects.filter(post_id=postIns.id).count()
        comments = CommentPost.objects.filter(post_id=postIns.id).count()
        data = {
            'id':postIns.id,
            'likes': likes,
            'comment': comments
        }
        return Response({"Data":data}, status=status.HTTP_200_OK)

    
class AllPostView(APIView):

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            accessTokenData = AccessToken(token[7:])
        except:
            return Response({"Message":"Authentication credentials weren't provided"})
        tokeUserId = accessTokenData['id']
        userIns = User.objects.get(id=tokeUserId)
        allPosts = Post.objects.filter(user=userIns)
        dataPosts = []
        for post in allPosts:
            data = {}
            data = {
                'id': post.id,
                'title': post.title,
                'desc': post.desc,
                'date': post.date,
            }
            comments = CommentPost.objects.filter(post_id=post.id).count()
            likes = LikePost.objects.filter(post_id=post.id).count()
            data['comments'] = comments
            data['likes'] = likes
            dataPosts.append(data)
        return Response({"Data":dataPosts}, status=status.HTTP_200_OK)
