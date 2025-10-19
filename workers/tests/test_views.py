import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from workers.models import Worker

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com"
    )

@pytest.fixture
def regular_user():
    return User.objects.create_user(username="user", password="userpass")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_admin_can_create_worker(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post('/api/workers/', {
        'first_name': 'Анна',
        'last_name': 'Сидорова',
        'email': 'anna@example.com',
        'position': 'HR'
    })
    assert response.status_code == 201
    assert Worker.objects.count() == 1
    assert Worker.objects.first().created_by == admin_user

@pytest.mark.django_db
def test_regular_user_cannot_create_worker(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    response = api_client.post('/api/workers/', {
        'first_name': 'Борис',
        'last_name': 'Кузнецов',
        'email': 'boris@example.com',
        'position': 'Аналитик'
    })
    assert response.status_code == 403
    assert Worker.objects.count() == 0
