from django.db import models
from datetime import datetime

class Article(models.Model):
    class Meta:
        db_table = "article"

    id = models.BigAutoField(primary_key=True, blank=False, null=False)
    location_id = models.BigIntegerField(blank=False, null=False)
    customer_id = models.IntegerField(blank=False, null=False, default=0)
    link_id = models.BigIntegerField(null=True, blank=False)
    image = models.CharField(max_length=1000, null=True, blank=False, default="no image")
    summary = models.CharField(max_length=500, null=True, blank=False)
    reg_date = models.DateTimeField(null=True, blank=False, default=str(datetime.now())[:19])
    update_date = models.DateTimeField(null=True, blank=False, default=str(datetime.now())[:19])

    def __str__(self):
        return self.id