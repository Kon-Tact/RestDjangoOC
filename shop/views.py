from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer,\
    CategoryListSerializer, ProductDetailSerializer, ProductListSerializer, ArticleListSerializer, ArticleDetailSerializer

class MultipleSerializerMixin:
    detail_serializer_class = None
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class AdminCategoryViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Category.objects.all()

class CategoryViewSet(ReadOnlyModelViewSet, MultipleSerializerMixin):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ProductViewSet(ReadOnlyModelViewSet, MultipleSerializerMixin):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id = category_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ArticleViewSet(ReadOnlyModelViewSet, MultipleSerializerMixin):
    serializer_class = ArticleListSerializer
    detail_serializer_class = ArticleDetailSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
    
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id = product_id)
        return queryset
    
class AdminArticleViewset(ModelViewSet, MultipleSerializerMixin):
    serializer_class = ArticleListSerializer
    detail_serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()