from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RecipeForm
from . import models
from django.views.generic import ListView, DetailView


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request=request)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect(reverse_lazy('recipes:recipe_add'))
    else:
        form = RecipeForm(request=request)
    return render(request, 'recipes/add_recipe.html', {'form': form})


class RecipeListView(ListView):
    model = models.Recipes
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'


class RecipesDetailView(DetailView):
    model = models.Recipes
    template_name = 'recipes/recipe_details.html'
    context_object_name = 'recipes'

