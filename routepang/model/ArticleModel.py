from django.db import models

class Article(models.Model):
    id = models.BigIntegerField(blank=False, primary_key=True)
    location_id = models.BigIntegerField(blank=False)
    link_id = models.BigIntegerField(null=True, blank=False)
    image = models.CharField(max_length=255, null=True, blank=False, default="no image")
    summary = models.CharField(max_length=255, null=True, blank=False)
    reg_date = models.DateTimeField(null=True, blank=False)
    user_id = models.IntegerField(blank=False)