from django.apps import AppConfig
import logging
import django
import imp

logger = logging.getLogger('django')


class MyhackerrankConfig(AppConfig):
	name = 'myhackerrank'

	def ready(self):
		logger.info(imp.find_module('requests'))

