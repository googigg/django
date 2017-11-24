from django.conf import settings

# access django setting from Py
# it is able to sent to Angular framework by calling


class PageUtil(object):

	@staticmethod
	def get_hello(self):
		print('final')
		data = dict()
		data['menu'] = getattr(settings, "HELLO")
		return data
