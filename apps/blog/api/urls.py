from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.blog.api.v1.urls'))
]