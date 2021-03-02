from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from content.models import Title, Genre, Category, Review, Comment
from users.models import User


class UserEmailRegistration(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserConfirmation(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if len(obj.reviews.all()) > 0:
            summa = 0
            for review in obj.reviews.all():
                summa += review.score
            count = obj.reviews.count()
            rating = int(summa/count)
            return rating
        return None

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'description', 'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',)


class ReviewReadSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        title = (self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Вы уже поставили оценку')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
