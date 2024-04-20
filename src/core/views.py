from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework

from .serializers import PostSerializer, ContactsSerializer, AboutUsSerializer, DeliverySerializer, SlideSerializer, BannerSerializer
from .models import Post, Slide
from rest_framework.response import Response
from taggit.models import Tag
from .serializers import TagSerializer, ContactSerailizer
from taggit.models import Tag
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import RegisterSerializer, UserSerializer, CommentSerializer
from .models import Comment, Contacts, AboutUs, Banner, Delivery
from django_filters import FilterSet, CharFilter


class BannerFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='exact', required=False)

    class Meta:
        model = Banner
        fields = ['id', 'name']


class AboutFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='exact', required=False)

    class Meta:
        model = AboutUs
        fields = ['id', 'name']


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
            return Response({"success": "Sent"})


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)


class BannerView(ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BannerFilter


class ContactsView(ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class AboutUsView(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = AboutFilter


class DeliveryView(ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class SlideView(ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
