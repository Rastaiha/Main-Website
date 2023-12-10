from django.test import TestCase
from django.core.files import File
from PIL import Image
from io import BytesIO
from apps.contact_us.forms import ContactUsForm


class ContactUsFormTest(TestCase):

    def test_valid_form(self):
        form = ContactUsForm(data={'name': 'Shadi',
                                   'text': 'Form Test',
                                   'email': 'valid.email@gmail.com',
                                   'type': 'student'})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = ContactUsForm(data={'name': 'Shadi',
                                   'text': 'Form Test',
                                   'email': 'Invalid Email',
                                   'type': 'student'})
        self.assertFalse(form.is_valid())

    def test_invalid_type(self):
        form = ContactUsForm(data={'name': 'Shadi',
                                   'text': 'Form Test',
                                   'email': 'valid.email@gmail.com',
                                   'type': ''})
        self.assertFalse(form.is_valid())


class ContactUsViewTest(TestCase):
    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(255, 0, 0)):
        file_obj = BytesIO()
        image = Image.new('RGBA', size=size, color=color)
        image.save(file_obj, format=ext, quality=100)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_view_url_exists(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/contact_us.html')

    def test_form_exists(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

    def test_invalid_form_submission(self):
        response = self.client.post('/contact_us/', data={'name': 'Shadi',
                                                          'text': 'Form Test',
                                                          'email': 'valid.email@gmail.com',
                                                          'type': 'student',
                                                          'bibot-response': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/contact_us.html')
