import datetime

def current_date(sep='/'):
	now = datetime.datetime.now()
	return '{1:02d}{0!s}{2:02d}{0!s}{3:02d}'.format(sep, now.day, now.month, now.year)

def current_time(sep=':'):
	now = datetime.datetime.now()
	return '{1:02d}{0!s}{2:02d}{0!s}{3:02d}'.format(sep, now.hour, now.minute, now.second)

def time_string():
	now = datetime.datetime.now()
	return '{:02d}{:02d}{:02d}_{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)