"""Tests for the views of the ``download_stats`` app."""
import os
import shutil

from django.conf import settings
from django.test import TestCase

from django_libs.tests.mixins import ViewTestMixin

from download_stats.models import DownloadStatistic


class DownloadViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``DownloadView`` view class."""
    longMessage = True

    def get_data_payload(self):
        return self.get_data  # defined in setUp

    def get_view_name(self):
        return 'download_view'

    def setUp(self):
        # set up media folder and download temp folder. The test requirements
        # should serve as test file
        self.temp_folder = os.path.join(settings.MEDIA_ROOT, 'tmp')
        self.req_file = os.path.join(settings.APP_ROOT,
                                     '../test_requirements.txt')
        self.temp_file = os.path.join(settings.MEDIA_ROOT,
                                      'test_requirements.txt')
        try:
            os.makedirs(self.temp_folder)
        except OSError:
            pass
        shutil.copy(self.req_file, self.temp_folder)

        self.get_data = {'file': 'tmp/test_requirements.txt'}

    def tearDown(self):
        shutil.rmtree(self.temp_folder)

    def test_view(self):
        self.is_callable()
        self.assertEqual(DownloadStatistic.objects.count(), 1, msg=(
            'The view hasn\'t created the expected download statisics.'))
        stat = DownloadStatistic.objects.get()
        self.assertEqual(stat.count, 1, msg=(
            'The view set the wrong amount of downloads'))

        self.is_callable()
        self.assertEqual(DownloadStatistic.objects.count(), 1, msg=(
            'The view did not get the persistant stat properly.'))
        stat = DownloadStatistic.objects.get()
        self.assertEqual(stat.count, 2, msg=(
            'The view set the wrong amount of downloads'))

        self.get_data.update({'file': 'not_existing_file.xyz'})
        self.is_not_callable()

        self.get_data = {'file': '../../no_valid.file'}
        self.is_not_callable(message='This file should not be accessable.')
