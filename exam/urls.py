from django.conf.urls import url
from . import views

urlpatterns = [

    # http://127.0.0.1:8000/exam/angular/?id=1
    url(r'^angular/$', views.MyAngularTutorial.as_view()),

    url(r'^angular/hello/$', views.easyfunction),

    # url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^angular/<filepath>/?$', views.MyRouting.as_view()),

    url(r'^angular/([\w\-]+)/$', views.MyAngularHTMLPath.as_view()),
    # or
    # url(r'^angular/([\w\-]+)/$', views.myAngularHTMLPath),

]
