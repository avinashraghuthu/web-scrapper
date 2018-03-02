from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


from views import WebScrapperView



urlpatterns = [
				url(r'^v1/webscrapper/$', csrf_exempt(WebScrapperView.as_view())),
			]