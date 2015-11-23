import filepathops
import json
import config_file_parser
import os
import output
import i_tables
import timestamp
import run_selection
import sys

def collect_audit_for_environment(environment, source_path, save_directory):
	print('{!s} at {!s}'.format(environment, source_path))
	run_time = timestamp.time_string()

	save_file = '{!s}/{!s}_{!s}.json'.format(save_directory, run_time, environment)
	overview = {'Environment':environment, 'Date':timestamp.current_date(), 'Time':timestamp.current_time()}
	comparison_object = {'overview':overview, 'config_files':[], 'database_tables':{}}

	for filepath in filepathops.each_object_in_directory_recursively(source_path, config_file_parser.is_config_file, config_file_parser.is_not_excluded_directory):
		relativepath = os.path.relpath(filepath, source_path)
		print(relativepath)
		config_file = config_file_parser.create_dictionary_from_file(filepath)
		config_file['file'] = relativepath
		comparison_object['config_files'].append(config_file)

	i_tables.get_i_table_data(comparison_object)

	output.write_out_json(comparison_object, save_file, save_directory)

def collect_audit_for_all_environments(save_directory):
	configured_environments = run_selection.configured_environments()
	for environment in configured_environments:
		collect_audit_for_environment(environment, configured_environments[environment], save_directory)
		

if __name__ == "__main__":
	try:
		environment = sys.argv[1]
		source_path = sys.argv[2]
		save_directory = sys.argv[3]
	except:
		print('Bad parameters passed')
		sys.exit()
	else:
		collect_audit_for_environment(environment, source_path, save_directory)