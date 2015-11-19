import filepathops
import json
import config_file_parser
import os
import output
import i_tables
import timestamp
import run_selection

run_time = timestamp.time_string()
configured_environments = run_selection.configured_environments()

for environment in configured_environments:

	print('{!s} at {!s}'.format(environment, configured_environments[environment]))

	source_path = configured_environments[environment]
	save_file = '../data/{!s}_{!s}.json'.format(run_time, environment)
	overview = {'Environment':environment, 'Date':timestamp.current_date(), 'Time':timestamp.current_time()}
	comparison_object = {'overview':overview, 'config_files':[], 'database_tables':{}}

	for filepath in filepathops.each_object_in_directory_recursively(source_path, config_file_parser.is_config_file, config_file_parser.is_not_excluded_directory):
		relativepath = os.path.relpath(filepath, source_path)
		print(relativepath)
		config_file = config_file_parser.create_dictionary_from_file(filepath)
		config_file['file'] = relativepath
		comparison_object['config_files'].append(config_file)

	i_tables.get_i_table_data(comparison_object)

	output.write_out_json(comparison_object, save_file)