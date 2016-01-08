import odbc_connection
from odbc_connection import odbc_connect

tables_to_retrieve = ['ORDERCFG', 'MODALLOW', 'MODESTS', 'ACCESS', 'EARNER', 'BGGROP', 'ORDERMSG']

def _find_library_for_table(odbc, table):
	def _table_is_in_library(odbc, table, library):
		for row in odbc.connection.cursor().execute("SELECT * FROM qsys2.systables WHERE sys_dname = '{!s}' AND sys_tname = '{!s}'".format(library, table)):
			return True
		return False
	for lib in odbc.libarray:
		if _table_is_in_library(odbc, table, lib):
			return lib
	return None

def _header_descriptions(odbc, table, library):
	for row in odbc.connection.cursor().execute("SELECT CAST(labeltext AS CHAR(100)) FROM qsys2.syscolumns WHERE sys_dname = '{!s}' AND sys_tname = '{!s}' ORDER BY colno".format(library, table)):
		for column in row:
			yield column

def _table_information(odbc, table, lib):
	def numbers_with_commas(n):
		arr = []
		for m in range(1, n):
			arr.append(str(m))
		return ', '.join(arr)

	info = {}
	info['headers'] = []
	info['rows'] = []
	info['title'] = table

	for header in _header_descriptions(odbc, table, lib):
		try:
			header = header.strip()
		except:
			header = ''
		info['headers'].append(header)

	info['rows'] = []
	sqlstring = "SELECT * from {!s} order by {!s}".format(table, numbers_with_commas(len(info['headers'])))
	for row in odbc.connection.cursor().execute(sqlstring):
		row_builder = []
		for column in row:
			try:
				column = column.strip()
			except:
				pass
			try:
				column = '{0:f}'.format(column)
			except:
				pass
			row_builder.append(column)
		info['rows'].append(row_builder)

	return info


def get_i_table_data(comparison_object):

	i_connection_settings = {}

	for config_file in comparison_object['config_files']:
		if config_file['file'].endswith('.properties'):
			for property in odbc_connection.i_connection_properties_required:
				if property in config_file['dictionary']:
					i_connection_settings[property] = config_file['dictionary'][property]
				else:
					break

	with odbc_connect(i_connection_settings) as odbc:
		for table in tables_to_retrieve:
			lib = _find_library_for_table(odbc, table)
			print('{!s}.{!s}'.format(lib, table))
			comparison_object['database_tables'][table] = _table_information(odbc, table, lib)