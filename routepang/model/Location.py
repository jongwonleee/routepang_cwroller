from django.db import models
from django.contrib.gis.db import models as models_gis

class Location(models.Model):
    class Meta:
        db_table = "location"

    id = models.BigAutoField(primary_key=True, blank=False, null=False)
    place_id = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255 ,blank=False, null=False)
    coordinates = models_gis.GeometryField(blank=False, null=False)
    category = models.IntegerField(blank=False, null=False, default=0)
    # rating = models.FloatField(default=0, blank=False)
    # api에서 제공 X
    # used_time = models.FloatField(default=0, blank=False) # doulbe??
    image = models.CharField(max_length=1000, null=True, blank=False, default="no image")
    reg_date = models.DateTimeField(null=True, blank=False)
    update_date = models.DateTimeField(null=True, blank=False)

    # 튜플의 대표값
    def __str__(self):
        return self.name