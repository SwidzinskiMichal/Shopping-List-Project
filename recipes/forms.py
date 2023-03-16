from django import forms
from .models import Recipes


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
            self.save_m2m()
        return recipe
