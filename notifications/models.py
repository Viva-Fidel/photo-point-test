from django.db import models

from users.models import CustomUser

# Create your models here.


class Notification(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        TELEGRAM = "telegram", "Telegram"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        CustomUser,
        related_name="notification",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус оповещения",
    )
    sent_channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        null=True,
        blank=True,
        verbose_name="Канал отправки оповещения",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    error_log = models.TextField(blank=True, null=True, verbose_name="Журнал ошибок")

    def __str__(self):
        return f"Оповещение номер {self.id} для {self.user.email} - {self.status}"

    class Meta:
        verbose_name = "Оповещение"
        verbose_name_plural = "Оповещения"
        ordering = ["-created_at"]
