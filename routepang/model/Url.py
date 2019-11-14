from django.db import models

class Url(models.Model):
    class Meta:
        db_table = "crawlingUrl"

    id = models.BigAutoField(blank=False, null=False, primary_key=True)
    location_id = models.BigIntegerField(blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.url_id