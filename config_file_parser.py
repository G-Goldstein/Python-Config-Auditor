import unittest
import os
from unittest.mock import MagicMock

class config_file_parser_test(unittest.TestCase):

	def setUp(self):
		pass

	def test_create_dictionary_from_configuration_contents(self):
		file_contents = "colour=red|shape=rectangle|size=large".replace('|', os.linesep)
		expected_dictionary = {
			'dictionary':{
				'colour':'red',
				'shape':'rectangle',
				'size':'large'
			}
		}
		file_content_lines = split_text_lines(file_contents)
		self.assertEqual(create_dictionary_from_configuration_lines(file_content_lines),expected_dictionary)

	def test_create_dictionary_from_configuration_contents_with_profiles(self):
		self.maxDiff = None
		file_contents = "[Default]|colour=red|shape=rectangle|size=large|[Special User]|colour=blue".replace('|', os.linesep)
		expected_dictionary = {
			'profiles':[
				{
					'profile':'[Default]',
					'dictionary':{
						'colour':'red',
						'shape':'rectangle',
						'size':'large'
					}
				},
				{
					'profile':'[Special User]',
					'dictionary':{
						'colour':'blue'
					}
				}
			]
		}
		file_content_lines = split_text_lines(file_contents)
		self.assertEqual(create_dictionary_from_configuration_lines(file_content_lines),expected_dictionary)

	def test_create_dictionary_from_configuration_contents_with_mix_of_profiles_and_default(self):
		self.maxDiff = None
		file_contents = "colour=red|shape=rectangle|size=large|[Special User]|colour=blue".replace('|', os.linesep)
		expected_dictionary = {
			'dictionary':{
				'colour':'red',
				'shape':'rectangle',
				'size':'large'
			},
			'profiles':[
				{
					'profile':'[Special User]',
					'dictionary':{
						'colour':'blue'
					}
				}
			]
		}
		file_content_lines = split_text_lines(file_contents)
		self.assertEqual(create_dictionary_from_configuration_lines(file_content_lines),expected_dictionary)	

	def test_line_is_profile(self):
		self.assertTrue(line_is_profile('[Default]'))
		self.assertFalse(line_is_profile('path=fhsh/[fhshs]'))
		self.assertFalse(line_is_profile('[hello'))
		self.assertFalse(line_is_profile('hello]'))

	def test_is_config_file(self):
		self.assertTrue(is_config_file('config.ini'))
		self.assertTrue(is_config_file('config.properties'))
		self.assertTrue(is_config_file('config.pref'))
		self.assertFalse(is_config_file('config.xlsx'))
		self.assertFalse(is_config_file('config'))
		self.assertFalse(is_config_file('configini'))

def split_text_lines(text):
	lines = text.split(sep='\n')
	return map(strip,lines)

def strip(string):
	return string.strip()

def create_dictionary_from_configuration_lines(lines):
	config_dictionary = {}
	dictionary = {}
	profile = ''
	def add_profile_to_config_dictionary():
		#if dictionary == {}:
		#	return
		if profile == '':
			config_dictionary['dictionary'] = dictionary
		else:
			if 'profiles' not in config_dictionary:
				config_dictionary['profiles'] = []
			config_dictionary['profiles'].append({'profile':profile, 'dictionary': dictionary})

	for dirty_line in lines:
		line = dirty_line.strip()
		if line_is_comment(line):
			continue
		if line_is_profile(line):
			add_profile_to_config_dictionary()
			dictionary = {}
			profile = line
		elif '=' in line:
			(key, equals, value) = line.partition('=')
			dictionary[key] = value
	add_profile_to_config_dictionary()
	return config_dictionary

def create_dictionary_from_file(file):
	return create_dictionary_from_configuration_lines(split_text_lines(file_contents(file)))

def file_contents(filepath):
	with open(filepath, 'r') as file:
		return file.read()

def line_is_comment(line):
	return line.startswith('#')

def line_is_profile(line):
	return line.startswith('[') and line.endswith(']')

def is_config_file(file):
	config_file_extensions = ['.ini', '.pref', '.properties']
	for ext in config_file_extensions:
		if file.endswith(ext):
			return True
	return False

def is_not_excluded_directory(file):
	excluded_directories = ['Archive']
	return not file in excluded_directories

if __name__ == '__main__':
	unittest.main()

