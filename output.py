import json

def write_out_json(comparison_object, save_path):
	with open(save_path, 'w') as file:
		file.write(json.dumps(comparison_object, sort_keys=True, indent=4, separators=(',', ': ')))
	print('Done! Audit output to ' + save_path)