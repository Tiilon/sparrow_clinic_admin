from django.db import models
from django.utils import timezone


class Branch(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, related_name='branches', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
