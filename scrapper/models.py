from __future__ import unicode_literals

from django.db import models

import requests
from bs4 import BeautifulSoup
import json
from django.db import IntegrityError
# Create your models here.


class ScrapperInformationManager(models.Manager):

	def scrape_url(self, web_url):
		r = requests.get(web_url)
		status_code = r.status_code
		data = r.text
		soup = BeautifulSoup(data, 'html.parser')
		h1_tag_info = [i.encode() for i in soup.find_all('h1')]
		h2_tag_info = [i.encode() for i in soup.find_all('h2')]
		tag_information = {
			'h1': h1_tag_info,
			'h2': h2_tag_info
		}
		tag_information_json = json.dumps(tag_information)
		if status_code == 200:
			status = self.model.SUCCESS
		else:
			status = self.model.FAILURE
		try:
			self.create_scrape_information(web_url, data, tag_information_json, status_code, status)
		except IntegrityError, e:
			scrapper_obj = self.get(web_url=web_url)
			scrapper_obj.update_scrapper(data, tag_information_json, status_code, status)
		return tag_information

	def create_scrape_information(self, web_url, site_information, tag_information,status_code, status):
		obj = self.model(web_url=web_url, site_information=site_information, tag_information=tag_information,
						 status_code=status_code,status=status)
		obj.save()
		return obj

	def get_all_urls_hitted(self, limit, offset):
		web_urls_info = []
		count = self.all().count()
		scrapper_list = self.all()[offset:limit]
		for scrapper in scrapper_list:
			web_urls_info.append(scrapper.serializer())
		return web_urls_info, count


class ScrapperInformation(models.Model):

	SUCCESS = 0
	FAILURE = 1
	status_choices = ((SUCCESS, 'Success'),
					  (FAILURE, 'Failure'),
						)

	web_url = models.URLField(primary_key=True,max_length=1000)
	site_information = models.TextField(null=True, blank=True)  # stores entire html of url
	tag_information = models.TextField(null=True, blank=True)  # stores information wrt tags.Here h1 and h2 as of now
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
	status_code = models.IntegerField(null=True, blank=True)  # stores http status code of response
	status = models.PositiveSmallIntegerField(choices=status_choices)

	objects = ScrapperInformationManager()

	def __unicode__(self):
		return str(self.web_url) + ' ' + str(self.status_code)

	def serializer(self):
		data = dict()
		data['web_url'] = self.web_url
		data['tag_information'] = json.loads(self.tag_information)
		data['status_code'] = self.status_code
		data['status'] = dict(self.status_choices).get(self.status)
		data['created_on'] = self.created_on.strftime('%Y-%m-%d')
		data['updated_on'] = self.created_on.strftime('%Y-%m-%d') if self.updated_on else None
		return data

	def update_scrapper(self, site_information, tag_information, status_code, status):
		self.site_information = site_information
		self.tag_information = tag_information
		self.status_code = status_code
		self.status = status
		self.save()

