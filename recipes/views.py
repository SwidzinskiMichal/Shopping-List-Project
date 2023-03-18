from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RecipeForm, RecipeIngredientForm
from . import models
from django.views.generic import ListView, DetailView, DeleteView
from .models import Recipes, RecipeIngredients, Units
from django.contrib import messages

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

    def get_context_data(self, **kwargs):
        context = super(RecipesDetailView, self).get_context_data(**kwargs)
        context['recipe_ingredients'] = RecipeIngredients.objects.all()
        return context


class RecipeDeleteView(DeleteView):
    model = models.Recipes
    success_url = reverse_lazy('recipes:recipe_list')
    template_name = 'recipes/recipe_delete.html'
    context_object_name = 'recipe'


def add_ingredients(request, pk):
    recipe = Recipes.objects.get(id=pk)
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=pk)
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.cleaned_data['ingredients']
            quantity = form.cleaned_data['quantity']
            unit_id = form.cleaned_data['unit']
            unit = Units.objects.get(id=unit_id)
            recipe_ingredient = RecipeIngredients(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)
            recipe_ingredient.save()
            messages.success(request, 'Ingredient added successfully.')
            return redirect(f'/recipes/recipe/{pk}/add_ingredients', pk=recipe.id)
    else:
        form = RecipeIngredientForm()
    context = {'form': form, 'recipe': recipe, 'recipe_ingredients': recipe_ingredients}
    return render(request, 'recipes/add_ingredients.html', context)


def recipe_edit(request, pk):
    recipe = Recipes.objects.get(pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect(f'/recipes/recipe/{pk}/', pk=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_edit.html', {'form': form})