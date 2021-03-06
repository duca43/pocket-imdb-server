from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from pocketimdb.users.urls import user_router, user_router_nested
from pocketimdb.movies.urls import movie_router, movie_nested_router, popular_movie_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(user_router.urls)),
    path('api/', include(user_router_nested.urls)),
    path('api/', include(movie_router.urls)),
    path('api/', include(movie_nested_router.urls)),
    path('api/', include(popular_movie_router.urls)),
]
