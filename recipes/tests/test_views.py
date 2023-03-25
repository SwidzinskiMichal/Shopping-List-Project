from django.urls import reverse
import pytest
from ..models import Recipes, RecipePlan


@pytest.mark.django_db
def test_add_recipe_page(client, user):
    url = reverse('recipes:recipe_add')

    client.login(email=user.email, password='testPass123')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Add Recipe</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_recipe_list_page(client):
    url = reverse('recipes:recipe_list')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Recipe List</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_recipe_details_page(client, user):
    client.login(email=user.email, password='testPass123')
    recipe = Recipes(name='test recipe', description='test desc', prep_method='test method', owner_id=2)
    recipe.save()
    url = reverse('recipes:recipe_details', kwargs={'pk': recipe.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Recipe Details</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_add_ingredients_page(client, user):
    client.login(email=user.email, password='testPass123')
    recipe = Recipes(name='test recipe', description='test desc', prep_method='test method', owner_id=3)
    recipe.save()
    url = reverse('recipes:add_ingredients', kwargs={'pk': recipe.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Add Ingredients</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_delete_ingredients_page(client, user):
    client.login(email=user.email, password='testPass123')
    recipe = Recipes(name='test recipe', description='test desc', prep_method='test method', owner_id=4)
    recipe.save()
    url = reverse('recipes:delete_ingredients', kwargs={'pk': recipe.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Remove Ingredients</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_recipe_edit_page(client, user):
    client.login(email=user.email, password='testPass123')
    recipe = Recipes(name='test recipe', description='test desc', prep_method='test method', owner_id=5)
    recipe.save()
    url = reverse('recipes:recipe_edit', kwargs={'pk': recipe.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Modify Recipe</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_recipe_delete_page(client, user):
    client.login(email=user.email, password='testPass123')
    recipe = Recipes(name='test recipe', description='test desc', prep_method='test method', owner_id=6)
    recipe.save()
    url = reverse('recipes:recipe_delete', kwargs={'pk': recipe.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>You are going to delete your recipe!</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_add_plan_page(client, user):
    url = reverse('recipes:add_plan')
    client.login(email=user.email, password='testPass123')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Create plan</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_plan_list_page(client):
    url = reverse('recipes:plan_list')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Plan List</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_plan_details_page(client, user):
    client.login(email=user.email, password='testPass123')
    plan = RecipePlan(name='test plan', description='test desc', owner_id=8)
    plan.save()
    url = reverse('recipes:plan_details', kwargs={'pk': plan.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Plan Details</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_plan_delete_page(client, user):
    client.login(email=user.email, password='testPass123')
    plan = RecipePlan(name='test plan', description='test desc', owner_id=9)
    plan.save()
    url = reverse('recipes:plan_delete', kwargs={'pk': plan.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>You are going to delete your plan!</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_plan_edit_page(client, user):
    client.login(email=user.email, password='testPass123')
    plan = RecipePlan(name='test plan', description='test desc', owner_id=10)
    plan.save()
    url = reverse('recipes:plan_edit', kwargs={'pk': plan.id})
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Modify Plan</h1>' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_recipe_edit_by_not_logged_user(client):
    url = reverse('recipes:recipe_edit', kwargs={'pk': 1})
    response = client.get(url)

    assert response.status_code == 302

    next_response = client.get(response.url)

    assert next_response.status_code == 200
    assert '<h1>Login</h1>' in next_response.content.decode('UTF-8')
