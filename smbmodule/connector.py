import tempfile
import os
from smb.SMBConnection import SMBConnection

class smb_connector:
	def __init__(self, ip, shared_directory, username, password):
		self.connection = SMBConnection(username, password, "this_machine", "remote_machine", use_ntlm_v2=True, is_direct_tcp=True)
		self.connection.connect(ip, 445)
		self.shared_directory = shared_directory

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	def close(self):
		self.connection.close()

	def file_contents(self, path):
		with tempfile.NamedTemporaryFile() as file_obj:
			self.connection.retrieveFile(self.shared_directory, path, file_obj)
			file_obj.seek(0)
			content = file_obj.read().decode('utf-8')
		return content

	def all_files_recursively(self, path, file_filter, directory_filter):
		whats_here = self.connection.listPath(self.shared_directory, path)
		for file in whats_here:
			file_path = os.path.join(path, file.filename)
			if file.isDirectory:
				if directory_filter(file.filename) and '.' not in file.filename:
					for child_file_path in self.all_files_recursively(file_path, file_filter, directory_filter):
						yield child_file_path
			elif file_filter(file.filename):
				yield file_path

	def write_file(self, path, contents):
		with tempfile.NamedTemporaryFile() as file_obj:
			bytes = file_obj.write(contents.encode('utf-8'))
			file_obj.seek(0)
			bytes = self.connection.storeFile(self.shared_directory, path, file_obj)