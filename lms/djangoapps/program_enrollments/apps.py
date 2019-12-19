# -*- coding: utf-8 -*-
"""
ProgramEnrollments Application Configuration
"""
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import PluginURLs, ProjectType


class ProgramEnrollmentsConfig(AppConfig):
    """
    Application configuration for ProgramEnrollment
    """
    name = 'lms.djangoapps.program_enrollments'

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: 'programs_api',
                PluginURLs.REGEX: 'api/program_enrollments/',
                PluginURLs.RELATIVE_PATH: 'rest_api.urls',
            }
        },
    }

    def ready(self):
        """
        Connect handlers to signals.
        """
        from . import signals  # pylint: disable=unused-variable
        from . import tasks    # pylint: disable=unused-variable
