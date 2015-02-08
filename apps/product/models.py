from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from jsonfield import JSONField
from apps.home.models import Category


class HomeImages(models.Model):

    """
        This class is for uploading images for slider.
    """

    image = ProcessedImageField(upload_to='config', processors=[
                                ResizeToFill(1140, 340)], format='JPEG',
                                options={'quality': 80})


class MenuItems(models.Model):

    """
        This class defines items in menus.
    """

    leftMenu = models.BooleanField(
        default=True, help_text='True if item appears in left menu, in case of top menu set false.',
        verbose_name='Is left item')
    label = models.CharField(max_length=100)
    parent = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.label
