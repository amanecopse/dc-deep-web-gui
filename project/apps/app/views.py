from django.shortcuts import render
from django.views import View
import logging

logger = logging.getLogger(__name__)


class IndexView(View):

    def get(self, request):
        data = {}
        return render(request, 'app/index.html', data)

    def post(self, request):
        data = {}
        return render(request, 'app/index.html', data)
