import filepathops
import json
import config_file_parser
import run_selection
import os
import output

selections = run_selection.get_selections()

save_file_name = os.path.basename(selections['save_file'])
(environment, _) = os.path.splitext(save_file_name)

comparison_object = {'environment':environment, 'config_files':[], 'database_files':[]}

for filepath in filepathops.each_object_in_directory_recursively(selections['source_path'], config_file_parser.is_config_file, config_file_parser.is_not_excluded_directory):
	relativepath = os.path.relpath(filepath, selections['source_path'])
	print(relativepath)
	config_file = config_file_parser.create_dictionary_from_file(filepath)
	if 'dictionary' in config_file or 'profiles' in config_file:
		config_file['file'] = relativepath
		comparison_object['config_files'].append(config_file)

for config_file in comparison_object['config_files']:
	if config_file['file'] == 'Envs\site.properties':
		print('Got a site.properties file!')

output.write_out_json(comparison_object, selections['save_file'])