import base64

from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import serializers, status

from users.models import Follow


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def handle_request(action, user, recipe=None,
                   model_class=None, author=None):

    if action == 'add_recipe_favorite':
        if user.favorites.filter(recipe=recipe).exists():
            return Response({'detail': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model_class.objects.create(user=user, recipe=recipe)
        return Response({'detail': 'Рецепт успешно добавлен!'},
                        status=status.HTTP_201_CREATED)
    elif action == 'remove_recipe_favorite':
        queryset = user.favorites.filter(recipe=recipe)
        if queryset.exists():
            queryset.delete()
            return Response({'detail': 'Рецепт успешно удален!'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Рецепт не найден.'},
                        status=status.HTTP_404_NOT_FOUND)
    elif action == 'add_recipe_shoppingcart':
        if user.shopping_carts.filter(recipe=recipe).exists():
            return Response({'detail': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model_class.objects.create(user=user, recipe=recipe)
        return Response({'detail': 'Рецепт успешно добавлен!'},
                        status=status.HTTP_201_CREATED)
    elif action == 'remove_recipe_shoppingcart':
        queryset = user.shopping_carts.filter(recipe=recipe)
        if queryset.exists():
            queryset.delete()
            return Response({'detail': 'Рецепт успешно удален!'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Рецепт не найден.'},
                        status=status.HTTP_404_NOT_FOUND)
    elif action == 'create_subscription':
        if user == author:
            return Response({'detail': 'Нельзя подписаться на самого себя!'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription, created = Follow.objects.get_or_create(
            user=user, following=author)
        if created:
            return Response({'detail': 'Подписка успешно создана.'},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': 'Вы уже подписаны.'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif action == 'delete_subscription':
        subscription = user.followings.filter(following=author)
        if subscription.exists():
            subscription.delete()
            return Response({'detail': 'Подписка отменена.'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Подписка не найдена.'},
                        status=status.HTTP_404_NOT_FOUND)

# def handle_favorite_or_shopping_cart_request(user, recipe,
#                                              model_class, action):
#     if action == 'add':
#         if model_class.objects.filter(user=user, recipe=recipe).exists():
#             return Response({'detail': 'Рецепт уже добавлен!'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         model_class.objects.create(user=user, recipe=recipe)
#         return Response({'detail': 'Рецепт успешно добавлен!'},
#                         status=status.HTTP_201_CREATED)
#     elif action == 'remove':
#         queryset = model_class.objects.filter(user=user, recipe=recipe)
#         if queryset.exists():
#             queryset.delete()
#             return Response({'detail': 'Рецепт успешно удален!'},
#                             status=status.HTTP_204_NO_CONTENT)
#         return Response({'detail': 'Рецепт не найден.'},
#                         status=status.HTTP_404_NOT_FOUND)


# def handle_subscription_request(user, author, action):
#     if action == 'create':
#         if user == author:
#             return Response({'detail': 'Нельзя подписаться на самого себя!'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         subscription, created = Follow.objects.get_or_create(
#             user=user, following=author)
#         if created:
#             return Response({'detail': 'Подписка успешно создана.'},
#                             status=status.HTTP_201_CREATED)
#         return Response({'detail': 'Вы уже подписаны.'},
#                         status=status.HTTP_400_BAD_REQUEST)
#     elif action == 'delete':
#         subscription = Follow.objects.filter(user=user, following=author)
#         if subscription.exists():
#             subscription.delete()
#             return Response({'detail': 'Подписка отменена.'},
#                             status=status.HTTP_204_NO_CONTENT)
#         return Response({'detail': 'Подписка не найдена.'},
#                         status=status.HTTP_404_NOT_FOUND)
