from django.contrib import admin
from routepang.model.Location import Location
from routepang.model.Article import Article
from routepang.model.Url import Url
from routepang.model.Link import Link

# Register your models here.
admin.site.register(Location)
admin.site.register(Article)
admin.site.register(Url)
admin.site.register(Link)