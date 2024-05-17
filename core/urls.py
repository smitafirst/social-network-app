from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .views import (
    UserSignupView,
    MyTokenObtainPairView,
    UserSearchView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    ListFriendsView,
    ListPendingFriendRequestsView,
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/accept/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friend-request/reject/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='friend_list'),
    path('friend-request/pending/', ListPendingFriendRequestsView.as_view(), name='pending_friend_requests'),
]

