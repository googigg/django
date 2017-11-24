from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

import json


class HttpUtil(object):
	def getRequestData(self,request):
		is_chunked = request.META.get("HTTP_TRANSFER_ENCODING")
		if(is_chunked == "chunked"):
			input_data_tmp = request.stream.read().decode("utf-8")
			input_data = json.loads(input_data_tmp)
		else:
			input_data = request.data
		return input_data

class HeaderUtil(APIView):
	def setUser(self, request):
		if 'HTTP_APP_META' in request.META:
			header_meta = request.META['HTTP_APP_META']
			request_header = json.loads(header_meta)
			log_session_id = request_header['log_session_id']
			user_id = request_header['user_id']
			user_name = request_header['user_name']

		user = dict()
		user['user_id'] = user_id
		user['log_session_id'] = log_session_id
		user['user_name'] = user_name
		return user

class authorizeUsers(APIView):
	def delete(self, request, user_id):
		return Response("")

	def put(self, request, user_id):
		return Response("")

	def get(self, request, user_id):
		return Response("")

	def post(self, request, user_id):
		# user = HeaderUtil().setUser(request)
		print('test')
		print(user_id)

		# httpUtil = HttpUtil()
		# request_data = httpUtil.getRequestData(request)

		# authorize_service_func = AuthorizeService()
		# response_return = authorize_service_func.check_authorize_by_user(request_data, user, user_id)

		response_return = dict()

		# response_return['meta']['response_ref'] = user['log_session_id']
		# response_return['meta']['response_datetime'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

		# log.debug("")
		return Response(response_return)
