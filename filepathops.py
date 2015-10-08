import os

def each_object_in_directory_recursively(path, file_filter, directory_filter):
	for file_or_dir in os.listdir(path):
		newpath = path + '/' + file_or_dir
		if os.path.isdir(newpath) and directory_filter(file_or_dir):
			for thing in each_object_in_directory_recursively(newpath, file_filter, directory_filter):
				yield thing
		elif file_filter(file_or_dir):
			yield newpath