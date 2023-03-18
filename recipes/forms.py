from django import forms
from .models import Recipes, Ingredients, Units


class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    prep_method = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Recipes
        fields = ('name', 'description', 'prep_method')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if self.request:
            recipe.owner = self.request.user
        if commit:
            recipe.save()
        return recipe


class RecipeIngredientForm(forms.Form):
    ingredients = forms.ModelChoiceField(queryset=Ingredients.objects.all())
    quantity = forms.DecimalField()
    unit = forms.ChoiceField(choices=[(unit.id, unit.name) for unit in Units.objects.all()])


