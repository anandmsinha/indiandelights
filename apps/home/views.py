from django.shortcuts import render
from .models import HomePage


def home_page(request):
    template_name = 'home/index.html'
    # Get all home page components
    home_components = HomePage.objects.select_related('category').all().prefetch_related('category__categories')
    for page in home_components:
        page.decode_json()
        page.fetch_items()
    return render(request, template_name, {'home_components': home_components})
