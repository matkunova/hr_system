from django.db import models
from django.contrib.auth.models import User
from .constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, POSITION_MAX_LENGTH


class Worker(models.Model):
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    middle_name = models.CharField(
        max_length=NAME_MAX_LENGTH, blank=True, verbose_name='Отчество')
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Фамилия')
    email = models.EmailField(unique=True, max_length=EMAIL_MAX_LENGTH)
    position = models.CharField(
        max_length=POSITION_MAX_LENGTH, verbose_name='Должность')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    hired_date = models.DateField(auto_now_add=True, verbose_name='Дата приёма на работу')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_workers',
        verbose_name='Кем создан'
    )

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['position']),
        ]
        verbose_name = 'работник'
        verbose_name_plural = 'работники'
