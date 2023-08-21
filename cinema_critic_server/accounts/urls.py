from django.urls import path

from cinema_critic_server.accounts import views_admin
from cinema_critic_server.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, DetailsUserView, \
    EditUserProfileView, CheckUserIsAuthenticatedView, AllUsersListView, DeleteUserView

urlpatterns = [
    path('allUsers/', AllUsersListView.as_view(), name='get_all_users'),
    path('register/', RegisterUserView.as_view(), name='user_register'),
    path('login/', LoginUserView.as_view(), name='user_login'),
    path('logout/', LogoutUserView.as_view(), name='current_user_logout'),
    path('details/', DetailsUserView.as_view(), name='current_user_details'),
    path('details/<int:pk>/', DetailsUserView.as_view(), name='user_details'),
    path('edit/<int:pk>/', EditUserProfileView.as_view(), name='user_edit_info'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='user_edit_info'),
    path('authenticated/', CheckUserIsAuthenticatedView.as_view(), name='check_if_user_authenticated'),


    # Admin views
    path('api/get-users/', views_admin.AdminUsersListView.as_view(), name='get_users'),
]
