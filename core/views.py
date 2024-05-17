from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import User, FriendRequest, Friendship, RateLimit
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(name__icontains=query)

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        rate_limit, created = RateLimit.objects.get_or_create(user=user)
        if (now() - rate_limit.last_request_time).seconds < 60 and rate_limit.request_count >= 3:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        friend_request, created = FriendRequest.objects.get_or_create(sender=user, receiver=receiver)
        if created:
            rate_limit.request_count += 1
            rate_limit.last_request_time = now()
            rate_limit.save()
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        friend_request_id = request.data.get('request_id')
        friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=user)
        friend_request.status = 'accepted'
        friend_request.save()
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        return Response(FriendRequestSerializer(friend_request).data)

class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        friend_request_id = request.data.get('request_id')
        friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=user)
        friend_request.status = 'rejected'
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data)

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status='')

class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        friends = Friendship.objects.filter(user1=user).values_list('user2', flat=True)
        friend_users = User.objects.filter(id__in=friends)
        serializer = UserSerializer(friend_users, many=True)
        return Response(serializer.data)
