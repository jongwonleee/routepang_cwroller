from django.db import models

class Article(models.Model):
    class Meta:
        db_table = "article"

    id = models.BigAutoField(primary_key=True, blank=False, null=False)
    location_id = models.BigIntegerField(blank=False, null=False)
    # default = admin_id : 1
    customer_id = models.IntegerField(blank=False, null=False, default=1)
    link_id = models.BigIntegerField(null=True, blank=False)
    image = models.CharField(max_length=1000, null=True, blank=False, default="no image")
    summary = models.CharField(max_length=500, null=True, blank=False)
    reg_date = models.DateTimeField(null=True, blank=False)
    update_date = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        return self.id