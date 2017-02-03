import tempfile
import os
import ftplib

class ftp_connector:
	def __init__(self, ip, username, password):
		self.ip = ip
		self.username = username
		self.password = password

	def __enter__(self):
		self.connection = ftplib.FTP(self.ip, timeout=100)
		self.connection.set_pasv(False)
		self.connection.login(self.username, self.password)
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	def close(self):
		self.connection.quit()

	def file_contents(self, path):
		with tempfile.NamedTemporaryFile() as file_obj:
			self.connection.retrbinary(
				"RETR {}".format(path),
				lambda bytes: file_obj.write(bytes)
			)
			file_obj.seek(2)
			contents = file_obj.read().decode('utf-8').translate({ord('\u0000'): None})
			return contents

	def all_files_recursively(self, full_path, file_filter, directory_filter, relative_path=''):
		whats_here = self.connection.nlst(full_path)
		for filename in whats_here:
			file_path = filename
			file_relative_path = os.path.join(relative_path, os.path.basename(filename))
			if self.is_library(file_path):
				if directory_filter(filename) and '.' not in filename:
					yield from self.all_files_recursively(file_path, file_filter, directory_filter, file_relative_path)
			elif file_filter(filename):
				yield os.path.normpath(file_relative_path)

	def is_library(self, path):
		try:
			self.connection.retrbinary("RETR {}".format(path), lambda bytes: bytes)
		except ftplib.error_perm:
			return True
		else:
			return False

	def write_file(self, path, contents):
		with tempfile.NamedTemporaryFile() as file_obj:
			bytes = file_obj.write(contents.encode('utf-8'))
			file_obj.seek(0)
			self.connection.storlines("STOR {}".format(path), file_obj)