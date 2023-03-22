from django import forms
from .models import Recipes, Ingredients, Units, RecipeIngredients


# Form for recipe creation
class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    prep_method = forms.CharField(widget=forms.Textarea)
    recipe_image = forms.ImageField()

    # class that defines metadata for the form
    class Meta:
        model = Recipes
        fields = ('name', 'description', 'prep_method', 'recipe_image')

    # method used to initialize the form object when it is created
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # function used to save the object to table
    def save(self, commit=True):
        recipe = super().save(commit=False)
        if self.request:
            recipe.owner = self.request.user
        if commit:
            recipe.save()
        return recipe


# Form for adding ingredients to recipe and creating recipe ingredient relations
class RecipeIngredientForm(forms.Form):
    ingredients = forms.ModelChoiceField(queryset=Ingredients.objects.all())
    quantity = forms.DecimalField()
    unit = forms.ChoiceField(choices=[(unit.id, unit.name) for unit in Units.objects.all()])


# Form for removing ingredients from recipe
class RemoveIngredientForm(forms.Form):
    def __init__(self, pk, *args, **kwargs):
        super(RemoveIngredientForm, self).__init__(*args, **kwargs)
        queryset = RecipeIngredients.objects.filter(recipe_id=pk)
        self.fields['ingredients'] = forms.ModelMultipleChoiceField(queryset)





