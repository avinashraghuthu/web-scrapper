from django.shortcuts import render

from django.views.generic import View
from responses import init_response, send_200, send_400 ,send_201
from exception import NoWebUrlProvided, InvalidWebUrl
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from constants import (STR_INVALID_URL,
					   STR_NO_URL_PROVIDED,
					   STR_WEB_SCRAPE_SUCCESS,
						STR_WEB_URL_INFO_RETRIEVED,
					   STR_LIMIT_OFFSET_INVALID)
from models import ScrapperInformation
# Create your views here.


class WebScrapperView(View):

	def __init__(self):
		self.response = init_response()

	def _validate(self, web_url):
		if not web_url:
			raise NoWebUrlProvided('No url provided')
		val = URLValidator()
		try:
			val(web_url)
		except ValidationError, e:
			raise InvalidWebUrl('Invalid Url')

	# @decorator_4xx([]) # to authenticate the user for api
	def post(self, request, *args, **kwargs):
		req_data = request.POST
		web_url = req_data.get('web_url')
		try:
			self._validate(web_url)
			tag_information = ScrapperInformation.objects.scrape_url(web_url)
			self.response['res_data']['tags'] = tag_information
			self.response['res_str'] = STR_WEB_SCRAPE_SUCCESS
			return send_201(self.response)
		except NoWebUrlProvided, e:
			self.response['res_str'] = STR_NO_URL_PROVIDED
		except InvalidWebUrl, e:
			self.response['res_str'] = STR_INVALID_URL
		return send_400(self.response)


	#@decorator_4xx([]) # to authenticate the user for api
	def get(self, request, *args, **kwargs):
		"""
		:param offset:  Gives the starting of list
		:param limit:  Gives the ending of list
		offset. limit = 0,10 - Gives the first 10 entries
					= 10, 20 - Gives the next 10 entries
		:return:
		"""
		req_data = request.GET
		try:
			limit = int(req_data['limit']) # Used for pagination fo request
			offset = int(req_data['offset'])
			web_urls_info, count = ScrapperInformation.objects.get_all_urls_hitted(limit, offset)
			self.response['res_data']['url_info'] = web_urls_info
			self.response['res_data']['count'] = count # specifies total url requests in db
			self.response['res_str'] = STR_WEB_URL_INFO_RETRIEVED
			return send_200(self.response)
		except KeyError, e:
			self.response['res_str'] = STR_LIMIT_OFFSET_INVALID
		except ValueError, e:
			self.response['res_str'] = STR_LIMIT_OFFSET_INVALID
		return send_400(self.response)



