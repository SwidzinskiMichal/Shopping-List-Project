from django.db import models
from django.contrib.auth import get_user_model


class Ingredients(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prep_method = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipe_author')
    created = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredients, through='RecipeIngredients')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Units, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} {self.ingredient.name} for {self.recipe.name}'
