from routepang.model.Url import Url
from routepang.model.Link import Link

class UrlController():

    def insertUrl(self, request, location_id):
        if not Link.objects.filter(link_url=request).exists():
            Url(url=request, location_id=location_id).save()

        return