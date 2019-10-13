"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from routepang.controller import JobController


scheduler = BackgroundScheduler()

# scheduler.add_job(JobController.locationTask(), 'interval', seconds=3, id="job_location")
# scheduler.add_job(JobController.urlTask(), 'interval', seconds=3, id="job_url")
# scheduler.add_job(JobController.infoTask(), 'interval', seconds=3, id="job_info")

scheduler.start()

urlpatterns = [
    path('admin/', admin.site.urls),
]




