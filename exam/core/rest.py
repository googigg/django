from rest_framework.response import Response
#from rest_framework.views import APIView
from exam.core.my_api_view import MyApiView

from exam.core.util.http import HttpUtil


# To use APIView, 'rest_framework' add to INSTALLED_APPS in settings.py
class Operation(MyApiView):
    def get(self, request: object) -> object:
        param = request.GET.get('param', None)

        if 'param' in request.GET and request.GET['param'] != "":
            print('there is something.')

        # bad way to declare dict variable like this
        result = {}
        result['meta'] = {}
        result['meta']['status'] = '00'
        result['meta']['message'] = 'Completed'
        result['meta']['param'] = param

        # parent function which extends from ApiView
        self.globol_function()

        return Response(result)

    def post(self, request):
        #print('[Operation][post]')
        return Response('post')

    def put(self, request: object) -> object:
        # good practise to declare dict variable below
        data = {
            "hello": "WORLD",
        }

        response_return = {
            "response_code": 20000,
            "response_desc": data
        }
        return Response(response_return)


class ExtractHeader(MyApiView):

    def get(self, request: object) -> object:
        http = HttpUtil()
        http.get_header_data(request)
        return Response(http.get_header_data(request))
