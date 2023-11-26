from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.blog.models import BlobCategory, Content
from .serializers import CategorySerializer, ContentSerializer


class CategoryListView(generics.ListAPIView):
    queryset = BlobCategory.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ContentListCreateView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class ContentListUpdateView(generics.UpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentListDestroyView(generics.DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer