from django.shortcuts import render
from django.views import View
import logging

logger = logging.getLogger(__name__)


class EnvView(View):

    def get(self, request):
        data = {}
        return render(request, 'env/index.html', data)

    def post(self, request):
        data = {}
        return render(request, 'env/index.html', data)
