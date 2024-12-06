from rest_framework import serializers
from .models import Product, Review, Tags

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    
    class Meta:
        model = Review
        fields = ('rating', 'comment', 'reviewer_name', 'reviewer_email', 'product')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'category', 'price', 'discount_percentage', 
            'rating', 'stock', 'tags', 'brand', 'sku', 'weight', 'warranty_information', 
            'shipping_information', 'availability_status', 'return_policy', 
            'minimum_order_quantity', 'images', 'thumbnail', 'width', 'height', 'depth', 'barcode', 'qr_code', 'reviews'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'rating': {'required': False}
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        product = Product.objects.create(**validated_data)

        for tag_data in tags_data:
            if 'id' in tag_data:  
                tag = Tags.objects.get(id=tag_data['id'])
            else:  
                tag, created = Tags.objects.get_or_create(**tag_data)
            product.tags.add(tag)
        
        return product
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.discount_percentage = validated_data.get('discount_percentage', instance.discount_percentage)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.depth = validated_data.get('depth', instance.depth)
        instance.warranty_information = validated_data.get('warranty_information', instance.warranty_information)
        instance.shipping_information = validated_data.get('shipping_information', instance.shipping_information)
        instance.availability_status = validated_data.get('availability_status', instance.availability_status)
        instance.return_policy = validated_data.get('return_policy', instance.return_policy)
        instance.minimum_order_quantity = validated_data.get('minimum_order_quantity', instance.minimum_order_quantity)
        instance.images = validated_data.get('images', instance.images)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.barcode = validated_data.get('barcode', instance.barcode)
        instance.qr_code = validated_data.get('qr_code', instance.qr_code)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            if 'id' in tag_data:
                tag = Tags.objects.get(id=tag_data['id'])
            else:
                tag, created = Tags.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation
