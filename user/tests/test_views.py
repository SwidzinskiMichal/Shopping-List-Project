from django.urls import reverse

def test_login_page(client):
    url = reverse('user:login')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in response.content.decode('UTF-8')


def test_register_page(client):
    url = reverse('user:registration')
    response = client.get(url)

    assert response.status_code == 200
    assert '<h1>Registration</h1>' in response.content.decode('UTF-8')


def test_register_user(client, django_user_model):
    url = reverse('user:registration')
    user_data = {
        'email': 'new@test.pl',
        'username': 'Test Registration',
        'password': 'secret123',
        'password_confirmation': 'secret123'
    }
    response = client.post(url, data=user_data)
    user_queryset = django_user_model.objects.filter(email='new@test.pl')

    assert response.status_code == 302
    assert len(user_queryset) == 1
    assert user_queryset.first().username == 'Test Registration'