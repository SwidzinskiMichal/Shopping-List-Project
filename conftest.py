import pytest


@pytest.fixture
def user(db, django_user_model):
    """User instance from default django user model"""
    return django_user_model.objects.create_user(
        email='test@user.pl',
        username='Test User',
        password='testPass123'
        )


