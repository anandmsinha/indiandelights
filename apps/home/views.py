from django.shortcuts import render


def home_page(request):
    template_name = 'home/index.jinja'
    return render(request, template_name)
