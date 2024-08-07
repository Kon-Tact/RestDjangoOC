from rest_framework import serializers

from shop.models import Category, Product, Article

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name']

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError('Le prix doit etre superieur a 1 euro')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Produit inactif')
        return value

class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles', 'ecoscore']

    def get_articles(self, instance):

        queryset = instance.articles.filter(active = True)
        serializer = ArticleDetailSerializer(queryset, many = True)
        return serializer.data
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'ecoscore']
    
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('La categorie existe deja')
        return value
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Le nom de la categorie doit apparaitre dans la description')
        return data

class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):

        queryset = instance.products.filter(active = True)
        serializer = ProductDetailSerializer(queryset, many = True)
        return serializer.data
