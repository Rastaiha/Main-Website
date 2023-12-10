from Rasta_Web.settings.base import bibot_SiteKey
from Rasta_Web.utils import check_bibot_response
from apps.contact_us.models import *
from apps.contact_us.forms import ContactUsForm
from django.shortcuts import render


def get_contact_us(request):
    form = ContactUsForm()
    context = {'form': form,
               'bibot': bibot_SiteKey}
    if request.method == 'GET':
        return render(request, 'contact_us/contact_us.html', context)
    else:
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact_us/successful.html')
