from django.contrib import admin
from routepang.model.LocationModel import Location
from routepang.model.ArticleModel import Article

# Register your models here.
admin.site.register(Location)
admin.site.register(Article)