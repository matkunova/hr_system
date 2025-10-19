import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from workers.models import Worker

@pytest.mark.django_db
def test_worker_creation():
    user = User.objects.create_user(username="testuser")
    worker = Worker.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="ivan@example.com",
        position="Разработчик",
        created_by=user
    )
    assert worker.first_name == "Иван"
    assert worker.is_active is True
    assert worker.created_by == user

@pytest.mark.django_db
def test_worker_email_unique():
    user = User.objects.create_user(username="testuser")
    Worker.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="ivan@example.com",
        position="Разработчик",
        created_by=user
    )
    with pytest.raises(IntegrityError):
        Worker.objects.create(
            first_name="Мария",
            last_name="Петрова",
            email="ivan@example.com",
            position="Дизайнер",
            created_by=user
        )