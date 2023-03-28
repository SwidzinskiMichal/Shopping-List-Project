from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RecipeForm, RecipeIngredientForm, RemoveIngredientForm, RecipePlanForm
from . import models
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Recipes, RecipeIngredients, Units, RecipePlan
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import OwnerRequiredMixin
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# view function for saving shopping list as pdf file
def shopping_list_pdf(request, pk, is_plan="False"):
    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    text_object =canv.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 12)

    lines = []
    if is_plan == "True":
        recipe_list = RecipePlan.objects.get(pk=pk).recipes.all()
        ingredients_list = RecipeIngredients.objects.filter(recipe_id__in=recipe_list)
        for recipe_id in recipe_list:
            recipe = Recipes.objects.get(pk=recipe_id.id)
            line = f"Shopping list for {recipe.name}"
            lines.append(line)
            for ingredient in (recipe_ingredient for recipe_ingredient in ingredients_list if recipe_ingredient.recipe_id == recipe_id.id):
                line = f"- {ingredient.quantity} {ingredient.unit.name} {ingredient.ingredient.name}"
                lines.append(line)
    else:
        ingredients_list = RecipeIngredients.objects.filter(recipe_id=pk)
        recipe = Recipes.objects.get(pk=pk)
        line = f"Shopping list for {recipe.name}"
        lines.append(line)

        for ingredient in ingredients_list:
            line = f"- {ingredient.quantity} {ingredient.unit.name} {ingredient.ingredient.name}"
            lines.append(line)

    for line in lines:
        text_object.textLine(line)

    canv.drawText(text_object)
    canv.showPage()
    canv.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='ShoppingList.pdf')


# View with form to add new recipes
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES,request=request)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect(reverse('recipes:recipe_details', args=[recipe.pk]))
    else:
        form = RecipeForm(request=request)
    return render(request, 'recipes/add_recipe.html', {'form': form})


# class view for list of all recipes inheriting after ListView
class RecipeListView(ListView):
    model = models.Recipes
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'


# class view for details of each recipe, inheriting after DetailView
class RecipesDetailView(DetailView):
    model = models.Recipes
    template_name = 'recipes/recipe_details.html'
    context_object_name = 'recipes'

    # Function to get additional context object of RecipeIngredients
    def get_context_data(self, **kwargs):
        context = super(RecipesDetailView, self).get_context_data(**kwargs)
        context['recipe_ingredients'] = RecipeIngredients.objects.all()
        return context


# class view to delete a recipe with additional permissions
class RecipeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = models.Recipes
    success_url = reverse_lazy('recipes:recipe_list')
    login_url = reverse_lazy('user:login')
    template_name = 'recipes/recipe_delete.html'
    context_object_name = 'recipe'


# function view to add ingredients to recipes
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


# function view to delete ingredients using multi select
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


# class view to update the recipes with additional permissions
class RecipeUpdateView(LoginRequiredMixin,OwnerRequiredMixin, UpdateView):
    model = models.Recipes
    fields = ('name', 'description', 'prep_method')
    template_name = 'recipes/recipe_edit.html'
    login_url = reverse_lazy('user:login')
    context_object_name = 'recipe'

    # function to redirect on successful update to corrected recipe
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('recipes:recipe_details', kwargs={'pk': pk})


# class view for plan creation
class AddPlanView(LoginRequiredMixin, CreateView):
    model = models.RecipePlan
    form_class = RecipePlanForm
    template_name = 'recipes/add_plan.html'
    login_url = reverse_lazy('user:login')
    success_url = reverse_lazy('recipes:plan_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# class view for plan list
class PlanListView(ListView):
    model = models.RecipePlan
    template_name = 'recipes/plan_list.html'
    context_object_name = 'plans'


# class view for plan details
class PlanDetailView(DetailView):
    model = models.RecipePlan
    template_name = 'recipes/plan_details.html'
    context_object_name = 'plans'

    # Function to get additional context object of RecipeIngredients
    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        context['recipe_ingredients'] = RecipeIngredients.objects.all()
        plan = RecipePlan.objects.get(pk=self.kwargs['pk'])
        context['plan_recipes'] = plan.recipes.all()
        return context


# class view to delete a plan with additional permissions
class PlanDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = models.RecipePlan
    success_url = reverse_lazy('recipes:plan_list')
    login_url = reverse_lazy('user:login')
    template_name = 'recipes/plan_delete.html'
    context_object_name = 'plan'


# class view to update the recipes with additional permissions
class PlanUpdateView(LoginRequiredMixin,OwnerRequiredMixin, UpdateView):
    model = models.RecipePlan
    fields = ('name', 'description', 'recipes')
    template_name = 'recipes/plan_edit.html'
    login_url = reverse_lazy('user:login')
    context_object_name = 'plan'

    # function to redirect on successful update to corrected recipe
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('recipes:plan_details', kwargs={'pk': pk})