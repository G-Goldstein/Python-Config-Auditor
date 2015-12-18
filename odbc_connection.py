import pyodbc

i_connection_properties_required = ['iseries.username', 'iseries.password', 'iseries.connection', 'iseries.librarylist']

def _trim_ip(ip):
	clean_ip = ip.strip('#')
	ip_part, port_part = clean_ip.split(':')
	return ip_part

class odbc_connect:
	def __init__(self, args):
		for required_property in i_connection_properties_required:
			if required_property not in args:
				raise AttributeError('required property {!s} not provided to odbc connection'.format(required_property))
		self.ip = _trim_ip(args['iseries.connection'])
		self.user = args['iseries.username']
		self.libl = args['iseries.librarylist']
		self.libarray = self.libl.split(',')
		self.connection_string="DSN=DB2DSN;ssl=1;System={!s};Uid={!s};Pwd={!s};DefaultLibraries={!s};ConnectionType=2".format(self.ip, self.user, args['iseries.password'], self.libl)

	def __enter__(self):
		self.connection = pyodbc.connect(self.connection_string, autocommit=True)
		print('Connected to the i at {!s} as {!s}'.format(self.ip, self.user))
		print('Using library list: {!s}'.format(self.libl))
		return self

	def __exit__(self, type, value, traceback):
		self.connection.close()