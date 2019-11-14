from django.db import models
from datetime import datetime

class Link(models.Model):
    class Meta:
        db_table = "link"

    id = models.BigAutoField(primary_key=True, blank=False, null=False)
    link_url = models.CharField(max_length=255, blank=False, null=False)
    favicon_url = models.CharField(max_length=1000, null=True, blank=False)
    image_url = models.CharField(max_length=1000, null=True, blank=False)
    summary = models.CharField(max_length=500, null=True, blank=False)
    reg_date = models.DateTimeField(null=True, blank=False, default=str(datetime.now())[:19])
    update_date = models.DateTimeField(null=True, blank=False, default=str(datetime.now())[:19])

    def __str__(self):
        return self.id