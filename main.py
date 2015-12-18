from smbmodule.connector import smb_connector
import json
import config_file_parser
import os
import output
import i_tables
import timestamp
import run_selection
import sys

globals = {}
global_variables = ['audit_machine_ip',
					'audit_machine_shared_directory',
					'audit_machine_save_path',
					'audit_machine_username',
					'audit_machine_password']


def set_globals():
	for variable in global_variables:
		try:
			globals[variable] = os.environ[variable]
		except:
			raise Exception('Environment variable {!s} not defined'.format(variable))

def collect_audit_for_environment(environment, source_ip, source_shared_directory, source_path, source_username, source_password):
	print('{!s} at {!s}'.format(environment, source_path))
	run_time = timestamp.time_string()

	save_file_name = '{!s}_{!s}.json'.format(run_time, environment)
	save_file_path = os.path.join(globals['audit_machine_save_path'], save_file_name)
	overview = {'Environment':environment, 'Date':timestamp.current_date(), 'Time':timestamp.current_time()}
	comparison_object = {'overview':overview, 'config_files':[], 'database_tables':{}}

	with smb_connector(source_ip, source_shared_directory, source_username, source_password) as source_connection:
		for filepath in source_connection.all_files_recursively(source_path, config_file_parser.is_config_file, config_file_parser.is_not_excluded_directory):
			print(filepath)
			config_file = config_file_parser.create_dictionary_from_file_contents(source_connection.file_contents(filepath))
			config_file['file'] = filepath
			comparison_object['config_files'].append(config_file)

	i_tables.get_i_table_data(comparison_object)

	with smb_connector(globals['audit_machine_ip'], globals['audit_machine_shared_directory'], globals['audit_machine_username'], globals['audit_machine_password']) as save_connection:
		save_connection.write_file(save_file_path, json.dumps(comparison_object, sort_keys=True, indent=4, separators=(',', ': ')))

def collect_audit_for_all_environments(save_directory):
	configured_environments = run_selection.configured_environments()
	for environment in configured_environments:
		collect_audit_for_environment(environment, configured_environments[environment], save_directory)
		

if __name__ == "__main__":
	try:
		environment = sys.argv[1]
		source_ip = sys.argv[2]
		source_shared_directory = sys.argv[3]
		source_path = sys.argv[4]
		source_username = sys.argv[5]
		source_password = sys.argv[6]
	except:
		print('Bad parameters passed')
		sys.exit()
	else:
		collect_audit_for_environment(environment, source_ip, source_shared_directory, source_path, source_username, source_password)