from django.urls import path
from .views import RegistrationView, MyObtainTokenPairView, CategoryListView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-registration'),
    path('login/', MyObtainTokenPairView.as_view(), name='user-login'),
    path('test/', CategoryListView.as_view(), name='test'),
]