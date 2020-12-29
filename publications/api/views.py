from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from profiles.models import User
from publications.models import Post
from .serializers import PostSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_post_view(request, slug):
    try:
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_post_view(request, slug):
    try:
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = PostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_post_view(request, slug):
    try:
        blog_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_post_view(request):

    profiles = User.objects.get(pk=1)

    blog_post = Post(author=request.profiles)

    if request.method == 'POST':
        serializer = PostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body', 'author__username')