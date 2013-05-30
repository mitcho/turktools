# coding: utf-8
from unittest import TestCase
import decoder
import sys

class Silence:
	def __init__(self):
		self.__log = []
		return
	def __call__(self):
		return self.__log
	def write(self, x):
		self.__log.append(x)
		return

class TestDecoder(TestCase):
	def test_decoder(self):
		pass
		