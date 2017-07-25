from rest_framework.response import Response

from django.views.generic.base import TemplateView
from rest_framework.views import APIView

#To use APIView, 'rest_framework' add to INSTALLED_APPS in settings.py
class Operation(APIView):
    def post(self, request):
        #print('[Operation][post]')
        return Response('post')

    def get(self, request):
        param = request.GET.get('param', None)

        result = {}
        result['meta'] = {}
        result['meta']['status'] = '00'
        result['meta']['message'] = 'Completed'
        result['meta']['param'] = param

        return Response(result)
