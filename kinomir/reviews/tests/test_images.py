# reviews/tests/test_images.py
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from reviews.models import Review

class ImageTests(TestCase):
    def test_image_upload(self):
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00...')
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        # тест загрузки картинки