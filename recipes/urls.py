from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('recipe/add/', views.recipe_add, name='recipe_add'),
    path('recipe/list/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipesDetailView.as_view(), name='recipe_details'),
    # path('recipe/modify/<int:pk>/', views.recipe_edit, name='recipe_edit'),
]
