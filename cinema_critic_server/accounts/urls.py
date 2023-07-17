from django.urls import path


from cinema_critic_server.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, DetailsUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUserView.as_view()),
    path('details/', DetailsUserView.as_view()),


]