from django.db import models


class Email(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = 'e-mail'
        verbose_name_plural = 'e-mails'

    def __str__(self):
        return self.email
