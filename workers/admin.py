from django.contrib import admin
from django.contrib.auth.models import User
from .models import Worker
import logging

logger = logging.getLogger(__name__)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email',
                    'position', 'is_active', 'created_by')
    list_filter = ('is_active', 'position', 'hired_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_editable = ('is_active',)
    readonly_fields = ('hired_date', 'created_by', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:  # Создание нового объекта
            obj.created_by = request.user
            logger.info(
                f"Worker created via admin: {obj.email} by {request.user.username}")
        super().save_model(request, obj, form, change)
