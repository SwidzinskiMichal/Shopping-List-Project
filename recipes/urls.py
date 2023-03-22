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
    path('recipe/download/<str:is_plan>/<int:pk>/', views.shopping_list_pdf, name='shopping_list_pdf'),
    path('recipe/add_plan/', views.AddPlanView.as_view(), name='add_plan'),
    path('recipe/plan_list/', views.PlanListView.as_view(), name='plan_list'),
    path('recipe/plan/<int:pk>/', views.PlanDetailView.as_view(), name='plan_details'),
    path('recipe/plan/delete/<int:pk>/', views.PlanDeleteView.as_view(), name='plan_delete'),
    path('recipe/plan/edit/<int:pk>/', views.PlanUpdateView.as_view(), name='plan_edit'),
]
