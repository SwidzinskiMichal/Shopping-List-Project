from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RecipeForm, RecipeIngredientForm, RemoveIngredientForm
from . import models
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import Recipes, RecipeIngredients, Units
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import OwnerRequiredMixin


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


class RecipeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = models.Recipes
    success_url = reverse_lazy('recipes:recipe_list')
    login_url = reverse_lazy('user:login')
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


def delete_ingredients(request, pk):
    recipe = Recipes.objects.get(id=pk)
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=pk)
    if request.method == 'POST':
        form = RemoveIngredientForm(pk, request.POST)
        selected_ingredients = request.POST.getlist('ingredients')
        print(selected_ingredients)
        if form.is_valid():
            selected_ingredients = request.POST.getlist('ingredients')
            RecipeIngredients.objects.filter(pk__in=selected_ingredients).delete()
            messages.success(request, 'Ingredient removed successfully.')
            return redirect(f'/recipes/recipe/{pk}/delete_ingredients', pk=recipe.id)
    else:
        form = RemoveIngredientForm(pk)
    context = {'form': form, 'recipe': recipe, 'recipe_ingredients': recipe_ingredients}
    return render(request, 'recipes/delete_ingredients.html', context)


class RecipeUpdateView(LoginRequiredMixin,OwnerRequiredMixin, UpdateView):
    model = models.Recipes
    fields = ('name', 'description', 'prep_method')
    template_name = 'recipes/recipe_edit.html'
    login_url = reverse_lazy('user:login')
    context_object_name = 'recipe'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('recipes:recipe_details', kwargs={'pk': pk})