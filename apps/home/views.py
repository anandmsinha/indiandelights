from django.shortcuts import render
from django.core.paginator import Paginator

from .models import HomePage, Vendors
from apps.product.models import HomeImages


def home_page(request):
    """
        Fetch the home page.
    """
    template_name = 'home/index.html'
    home_components = HomePage.objects.select_related('category').all()
    feed_components = [home_page for home_page in home_components if home_page.is_config is False]
    for page in feed_components:
        page.decode_json()
        page.fetch_items()
    slider_images = HomeImages.objects.all()
    return render(request, template_name, {'home_components': feed_components, 'slider_images': slider_images, 'loop_range': range(len(slider_images))})


def vendor_view(request):
    """
        This view represents list of all vendors along with profile pic and little description.
    """
    template_name = 'home/vendor.html'
    vendors_list = Vendors.objects.select_related('city').all()
    page = request.GET.get('page', 1)
    vendors = Paginator(vendors_list, 20).page(page)
    return render(request, template_name, {'vendors': vendors})


def error_page(request, code, message):
    template_name = 'home/error.html'
    return render(request, template_name, {'code': code, 'message': message})


def not_found(request):
    return error_page(request, '404 Not Found', 'Sorry, an error has occured, Requested page not found!')


def internal_server_error(request):
    return error_page(request, '500 Error', 'Sorry, Internal server error')