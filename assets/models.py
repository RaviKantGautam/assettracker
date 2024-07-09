import uuid
from django.db import models
from asset_tracker.db import AbstractBaseModel
from django.urls import reverse


class AssetType(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Asset Type'
        verbose_name_plural = 'Asset Types'
        ordering = ['-created_at']
    
    def get_absolute_url(self):
        return reverse("asset_type_detail", kwargs={"pk": self.pk})


class AssetImage(AbstractBaseModel):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.asset.name

    class Meta:
        verbose_name = 'Asset Image'
        verbose_name_plural = 'Asset Images'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("asset_image_detail", kwargs={"pk": self.pk})


class Asset(AbstractBaseModel):
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['-created_at']

    @property
    def is_active(self):
        return self.status
    
    def get_absolute_url(self):
        return reverse("asset_detail", kwargs={"pk": self.pk})
