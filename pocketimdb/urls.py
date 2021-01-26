from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from pocketimdb.users.urls import userRouter
from pocketimdb.movies.urls import movieRouter, popular_movie_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(userRouter.urls)),
    path('api/', include(movieRouter.urls)),
    path('api/', include(popular_movie_router.urls)),
]
