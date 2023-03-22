from django.db import models
from django.contrib.auth import get_user_model

# Model containing the ingredients
class Ingredients(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Model containing the units for the ingredients
class Units(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Model containing the created recipes
class Recipes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prep_method = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipe_author')
    created = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredients, through='RecipeIngredients')
    recipe_image = models.ImageField(upload_to='recipes/', default='recipes/placeholder.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)


# Relation model between ingredients, recipes and units
class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Units, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} {self.ingredient.name} for {self.recipe.name}'
