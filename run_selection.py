import tkinter as tk
import os
from tkinter import filedialog
from tkinter import simpledialog
import unittest
from unittest.mock import MagicMock

class run_selection_test(unittest.TestCase):

	def setUp(self):
		self.normalpath = '/folder/parent/child'
		self.normalpath2 = self.normalpath + '/childer'
		self.slashpath = self.normalpath + '/'
		self.slashpath2 = self.normalpath2 + '/'
		self.filepath = self.slashpath + 'file.ini'

	def test_chosen_directory_can_be_called(self):
		_chosen_directory = MagicMock(return_value='child')
		self.assertEqual(_chosen_directory(self.normalpath),'child')
		_chosen_directory.assert_called_once_with(self.normalpath)

	def test_chosen_directory_in_normal_case_returns_directory(self):
		self.assertEqual(_chosen_directory(self.normalpath),'child')
		self.assertEqual(_chosen_directory(self.normalpath2),'childer')

	def test_chosen_directory_with_final_slash_returns_directory(self):
		self.assertEqual(_chosen_directory(self.slashpath),'child')
		self.assertEqual(_chosen_directory(self.slashpath2),'childer')

	def test_parent_directory_can_be_called(self):
		_parent_directory = MagicMock(return_value='parent')
		self.assertEqual(_parent_directory(self.normalpath),'parent')
		_parent_directory.assert_called_once_with(self.normalpath)

	def test_parent_directory_in_normal_case_returns_parent(self):
		self.assertEqual(_parent_directory(self.normalpath),'parent')
		self.assertEqual(_parent_directory(self.normalpath2),'child')

	def test_parent_directory_with_final_slash_returns_parent(self):
		self.assertEqual(_parent_directory(self.slashpath),'parent')
		self.assertEqual(_parent_directory(self.slashpath2),'child')

	def test_error_returned_when_a_file_is_passed_to_chosen_directory(self):
		with self.assertRaises(ValueError):
			_chosen_directory(self.filepath)
		try:
			_chosen_directory(self.filepath)
		except ValueError as e:
			self.assertEqual(e.args[0],'Directory expected but file file.ini received')

	def test_error_returned_when_a_file_is_passed_to_parent_directory(self):
		with self.assertRaises(ValueError):
			_parent_directory(self.filepath)
		try:
			_parent_directory(self.filepath)
		except ValueError as e:
			self.assertEqual(e.args[0],'Directory expected but file file.ini received')

def _chosen_directory(path):
	normpath = os.path.normpath(path)
	(head, tail) = os.path.split(normpath)
	if '.' in tail:
		raise(ValueError('Directory expected but file {!s} received'.format(tail)))
	else:
		return tail

def _parent_directory(path):
	normpath = os.path.normpath(path)
	(head, tail) = os.path.split(normpath)
	if '.' in tail:
		raise(ValueError('Directory expected but file {!s} received'.format(tail)))
	else:
		return os.path.basename(head)

def get_selections():
	root = tk.Tk()
	root.withdraw()
	config_directory_path = filedialog.askdirectory(mustexist=True, title="Choose a source Config directory")
	if not config_directory_path:
		raise(RuntimeError('Selection cancelled'))
	root_directory = _chosen_directory(config_directory_path)
	parent_directory = _parent_directory(config_directory_path)
	if root_directory != 'Config':
		raise(RuntimeError('Selected directory is not a Config directory'))

	save_file = filedialog.asksaveasfilename(filetypes=[('json file', '.json')], initialfile=parent_directory + '.json', title="Save As")
	if not config_directory_path:
		raise(RuntimeError('Selection cancelled'))
	selections = {
		'source_path': config_directory_path,
		'root_directory': root_directory,
		'save_file': save_file
	}
	return selections

if __name__ == '__main__':
	unittest.main()