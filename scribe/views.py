from django.views.generic.base import TemplateView
from django.shortcuts import render


def index(request):
    return render(request, 'scribe/index.html')


class ProfileView(TemplateView):
    template_name = "profile.html"
