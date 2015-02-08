from django.shortcuts import render
from django.core.paginator import Paginator

from .models import HomePage, Vendor
from apps.product.models import HomeImages, MenuItems
from .utilities import processMenuItems
import logging

logger = logging.getLogger(__name__)


def home_page(request):
    """
        Fetch the home page.
    """
    logger.debug('home_page fetch method called')
    template_name = 'home/index.html'
    home_components = HomePage.objects.select_related('category').all()
    for page in home_components:
        page.decode_json()
        page.fetch_items()
    slider_images = HomeImages.objects.all()
    menu_items = processMenuItems(MenuItems.objects.filter(leftMenu__exact=True))
    output = render(request, template_name, {'home_components': home_components, 'slider_images': slider_images, 'loop_range': range(len(slider_images)), 'left_menu_items': menu_items})
    logger.debug('home_page method finished')
    return output


def vendor_view(request):
    """
        This view represents list of all vendors along with profile pic and little description.
    """
    template_name = 'home/vendor.html'
    vendors_list = Vendor.objects.select_related('city').all()
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