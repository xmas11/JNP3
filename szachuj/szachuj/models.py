from django.db import models


class Szach(models.Model):
    """
        Main model for storing dips in database
    """

    content = models.TextField(max_length=1024, blank=False)
    signature = models.TextField(max_length=128, blank=False)
    stamp = models.DateTimeField(auto_now=True)