from rest_framework.response import Response
from rest_framework.views import APIView

from engine.core.util.http import HttpUtil


# To use APIView, 'rest_framework' add to INSTALLED_APPS in settings.py

class Operation(APIView):

    def get(self, request):
        param = request.GET.get('param', None)

        result = {}
        result['meta'] = {}
        result['meta']['status'] = '00'
        result['meta']['message'] = 'Completed'
        result['meta']['param'] = param

        return Response(result)

    def post(self, request):
        #print('[Operation][post]')
        return Response('post')


class ExtractHeader(APIView):

    def get(self, request):
        http = HttpUtil()
        http.get_header_data(request)
        return Response(http.get_header_data(request))
