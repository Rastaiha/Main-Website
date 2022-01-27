from django.shortcuts import render
from .models import Term

def get_members(request):
    terms = Term.objects.all().order_by('-end')
    context = {'terms':terms}
    return render(request, 'members/members.html', context)