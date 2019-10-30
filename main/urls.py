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

from apscheduler.schedulers.background import BackgroundScheduler
from routepang.controller import JobController

# scheduler = BackgroundScheduler()

# test용 time
# scheduler.add_job(JobController.urlTask, 'cron', hour=23, minute=5, id="job_url")
# scheduler.add_job(JobController.infoTask, 'cron', hour=23, minute=7, id="job_info")

# scheduler.start()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/', JobController.urlTask(), name='job1'),
    # path('test2/', JobController.infoTask(), name='job2'),
]




