from rest_framework import serializers
from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework.authtoken.models import Token
from product.models import Category, Image, Product, ProductAttribute, Comment, Attribute, AttributeValue, MyModel
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class CategoryModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'image']


class CommentModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    # product_name = serializers.CharField(source='product.product_name')
    class Meta:
        model = Comment
        fields = ['username', 'positive_message', 'negative_message', 'file']


class ProductModelSerializer(serializers.ModelSerializer):
    comments = CommentModelSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter(product=instance).values_list('attribute_id',
                                                                                   'attribute__attribute_name',
                                                                                   'attribute_value_id',
                                                                                   'attribute_value__attribute_value')
        characters = [
            {'attrbute_id': key_id,
             'attribute_name': key_name,
             'attribute_value_id': value_id,
             'attribute_value': value_name

             }
            for key_id, key_name, value_id, value_name in attributes

        ]
        return characters

    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        else:
            return False

    def get_avg_rating(self, obj):
        avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0

    def get_comment_count(self, instance):
        count = Comment.objects.filter(product=instance).count()
        return count

    def get_primary_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None

    def get_all_images(self, instance):
        images = Image.objects.filter(product=instance).all()
        request = self.context.get('request')
        all_images = []
        if images:
            for image in images:
                all_images.append(request.build_absolute_uri(image.image.url))

            return all_images

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['primary_image', 'comments', 'is_liked', 'attributes']


class CategoryDetailModelSerializer(serializers.ModelSerializer):
    products = ProductModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        extra_fields = ['products']


# Register, login
class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserModelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# Attributelar
class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'attribute_name']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute_value']


class ProductAttributesSerializer(serializers.ModelSerializer):
    attribute_key = serializers.CharField(source='attribute.attribute_name')
    attribute_value = serializers.CharField(source='attribute_value.attribute_value')

    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute_key', 'attribute_value']