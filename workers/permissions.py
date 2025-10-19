from rest_framework import permissions


class WorkerPermission(permissions.BasePermission):
    """
    Разрешение для WorkerViewSet:
    - Любой авторизованный пользователь может читать (GET)
    - Только администраторы (is_staff) могут изменять (POST, PUT, PATCH, DELETE)
    """

    def has_permission(self, request, view):
        # Только авторизованные пользователи
        if not request.user.is_authenticated:
            return False

        # Разрешить чтение всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для изменения — только администраторы
        return request.user.is_staff
