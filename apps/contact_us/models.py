from django.db import models


class UserFeedback(models.Model):
    type_choices = (('student', 'دانش آموز'),
                    ('teacher', 'آموزگار'),
                    ('parent', 'پدر یا مادر'),
                    ('other', 'دیگر'))
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    type = models.CharField(max_length=200, null=False,
                            blank=False, choices=type_choices)
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.submit_time) + ' - ' + self.type
