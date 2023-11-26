from django.urls import path
from .views import CategoryListView, ContentListCreateView,\
    ContentListUpdateView, ContentListDestroyView

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('content/', ContentListCreateView.as_view()),
    path('content/u/<int:pk>/', ContentListUpdateView.as_view()),
    path('content/d/<int:pk>/', ContentListDestroyView.as_view()),


]