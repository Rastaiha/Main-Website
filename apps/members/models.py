from operator import mod
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Term(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

class RastaMember(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    education = models.CharField(max_length=200, blank=False, null=False)
    role = models.CharField(max_length=100, blank=True, null=True)
    photo_visible = models.ImageField(null=False, blank=False)
    photo_hidden = models.ImageField(null=True, blank=True)
    term = models.ForeignKey(Term,on_delete=models.CASCADE,related_name='members')
    def save(self, *args, **kwargs):
        im1 = Image.open(self.photo_visible)
        output1 = BytesIO()
        im1 = im1.resize((150, 150))
        im1.save(output1, format='png', quality=100)
        output1.seek(0)
        self.photo_visible = InMemoryUploadedFile(output1, 'ImageField',
                                                  "%s.jpg" % self.photo_visible.name.split('.')[
                                                      0], 'image/jpeg',
                                                  sys.getsizeof(output1), None)
        if self.photo_hidden:
            im2 = Image.open(self.photo_hidden)
            im2 = im2.resize((150, 150))
            output2 = BytesIO()
            im2.save(output2, format='png', quality=100)
            output2.seek(0)
            self.photo_hidden = InMemoryUploadedFile(output2, 'ImageField',
                                                     "%s.jpg" % self.photo_hidden.name.split('.')[
                                                         0],
                                                     'image/jpeg',
                                                     sys.getsizeof(output2), None)

        super(RastaMember, self).save()

    def __str__(self):
        if self.role:
            return self.name + ' - ' + self.role
        return self.name

