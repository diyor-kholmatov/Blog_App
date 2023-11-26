from django.db import models
from apps.base.models import BaseModel
from apps.account.models import User

class BlobCategory(BaseModel):
    class Meta:
        verbose_name = "Blog Categories"
        verbose_name_plural = "Blog Category"

    title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title


class Content(BaseModel):
    class Meta:
        verbose_name = "Contents"
        verbose_name_plural = "Content"

    title = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(BlobCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Useer', on_delete=models.CASCADE)

    def __str__(self):
        return self.title