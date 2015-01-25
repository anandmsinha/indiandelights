from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class HomeImages(models.Model):

    """
        This class is for uploading images for slider.
    """

    image = ProcessedImageField(upload_to='config', processors=[ResizeToFill(1140, 340)], format='JPEG', options={'quality': 80})