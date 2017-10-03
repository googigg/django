from rest_framework.views import APIView

class MyApiView(APIView):
	def global_function(self):
		print('globol')
