from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return (self.name + ', ' + self.unit)

    class Meta:
        unique_together = ['name', 'unit']


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='Composition',
        blank=True
    )
    tag = models.ManyToManyField(Tag, blank=True)
    cooking_time = models.PositiveIntegerField()
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class Composition(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    number = models.PositiveIntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return ''


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        unique_together = ['user', 'author']


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reader'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='reading'
    )

    class Meta:
        unique_together = ['user', 'recipe']


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer'
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'recipe']
