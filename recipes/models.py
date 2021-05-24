from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=100, unique=True,
        verbose_name='название тега'
    )
    slug = models.CharField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Теги для рецепта'
        verbose_name_plural = 'Теги для рецепта'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='название ингредиента'
    )
    unit = models.CharField(
        max_length=100,
        verbose_name='единица измерения'
    )

    def __str__(self):
        return (self.name + ', ' + self.unit)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'unit'],
                name='unique pair of ingredients'
            )
        ]
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='автор'
    )
    title = models.CharField(
        max_length=100, verbose_name='название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/', blank=True, null=True,
        verbose_name='изображение рецепта'
    )
    description = models.TextField(verbose_name='описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes', through='Composition',
        blank=True, verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, blank=True, verbose_name='теги для рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления'
    )
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True,
        verbose_name='уникальное имя рецепта'
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Composition(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='ингрединт для композиции'
    )
    number = models.PositiveIntegerField(verbose_name='количество')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='рецепт для композиции'
    )

    class Meta:
        verbose_name = 'Композиции ингредиентов'
        verbose_name_plural = 'Композиции ингредиентов'

    def __str__(self):
        return ''


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='подписавшийся пользователь'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Пользователь, на которого подписаны'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique pair of subscribers'
            ),
            models.CheckConstraint(
                name="prevent self follow",
                check=~models.Q(user=models.F("author")),
            ),
        ]
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reader',
        verbose_name='пользователь, добавивший в избранное'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='reading',
        verbose_name='рецепт, добавленный в избранное'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique pair of favorites'
            )
        ]
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer',
        verbose_name='пользователь, добавивший в покупки'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='рецепт, добавленный в покупки'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique pair of purchases'
            )
        ]
        verbose_name = 'Рецепты в покупках'
        verbose_name_plural = 'Рецепты в покупках'
