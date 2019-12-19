"""
Grades API URLs.
"""

from __future__ import absolute_import

from django.conf.urls import include, url

app_name = 'lms.djangoapps.grades'

urlpatterns = [
    url(r'^v1/', include('grades.rest_api.v1.urls', namespace='v1'))
]
