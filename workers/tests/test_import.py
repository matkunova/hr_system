import pytest
from io import BytesIO
from openpyxl import Workbook
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from workers.models import Worker


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username="admin", password="adminpass"
    )


@pytest.fixture
def api_client():
    return APIClient()


def create_excel_file(data):
    wb = Workbook()
    ws = wb.active
    ws.append(["first_name", "last_name", "email", "position"])
    for row in data:
        ws.append(row)
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return SimpleUploadedFile(
        name="test_import.xlsx",
        content=buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@pytest.mark.django_db
def test_import_valid_excel(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    data = [
        ["Анна", "Сидорова", "anna@test.com", "HR"],
        ["Борис", "Кузнецов", "boris@test.com", "Аналитик"]
    ]
    excel_file = create_excel_file(data)

    response = api_client.post(
        '/api/workers/import/',
        {'file': excel_file},
        format='multipart'
    )

    assert response.status_code == 201
    assert response.data['success_count'] == 2
    assert Worker.objects.count() == 2
    assert Worker.objects.get(email="anna@test.com").created_by == admin_user


@pytest.mark.django_db
def test_import_duplicate_email_in_file(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    data = [
        ["Анна", "Сидорова", "anna@test.com", "HR"],
        ["Анна2", "Сидорова2", "anna@test.com", "HR"]
    ]
    excel_file = create_excel_file(data)

    response = api_client.post(
        '/api/workers/import/',
        {'file': excel_file},
        format='multipart'
    )

    assert response.status_code == 400
    assert response.data['success_count'] == 0
    assert len(response.data['errors']) == 1
    assert "Дубликат email в файле" in response.data['errors'][0]['error']
    assert Worker.objects.count() == 0  # ничего не сохранено
