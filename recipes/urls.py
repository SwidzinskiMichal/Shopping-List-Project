from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('recipe/add/', views.recipe_add, name='recipe_add'),
    path('recipe/list/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipesDetailView.as_view(), name='recipe_details'),
    path('recipe/<int:pk>/add_ingredients/', views.add_ingredients, name='add_ingredients'),
    path('recipe/<int:pk>/delete_ingredients/', views.delete_ingredients, name='delete_ingredients'),
    path('recipe/modify/<int:pk>/', views.RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/delete/<int:pk>/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]
