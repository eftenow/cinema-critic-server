from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cinema_critic_server.common.urls')),
    path('account/', include('cinema_critic_server.accounts.urls')),
    path('dashboard/', include('cinema_critic_server.content.urls')),
    path('reviews/', include('cinema_critic_server.reviews.urls')),

]
