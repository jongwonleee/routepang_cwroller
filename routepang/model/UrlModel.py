from django.db import models

class Url(models.Model):
    class Meta:
        db_table = "crawling_url"

    url_id = models.BigAutoField(blank=False, primary_key=True)
    location_id = models.BigIntegerField(blank=False)
    url = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.url_id