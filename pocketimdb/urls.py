from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from pocketimdb.users.urls import userRouter
from pocketimdb.movies.urls import movie_router, watch_list_router, movie_watch_list_nested_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(userRouter.urls)),
    path('api/', include(movie_router.urls)),
    path('api/', include(watch_list_router.urls)),
    path('api/', include(movie_watch_list_nested_router.urls)),
]
