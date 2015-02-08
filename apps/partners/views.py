from django.shortcuts import render, redirect
from .forms import ApplicantsForm
import logging


logger = logging.getLogger(__name__)


def register(request):
    logger.debug('register vendor called')
    template_name = 'partners/register.html'

    if request.method == 'GET':
        form = ApplicantsForm()
    else:
        form = ApplicantsForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('partners:thanks')
    return render(request, template_name, {'form': form})
