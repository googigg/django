from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from engine.core.dataObjects.Car import Car
from engine.core.dataObjects.Cat import Cat

from django.views.generic.base import TemplateView


def easyfunction(request,):
    c = Car('Mazda')
    c.run()
    c.debug()
    current_fuel = c.get_fuel()

    print(c)
    print(c.__dict__)

    cat = Cat('Kitty')
    cat.info()

    return HttpResponse("Current Fuel: " + str(c) + " " + c.brand + " " + str(current_fuel))




class HomePageView(TemplateView):

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = 'hello'
        return context