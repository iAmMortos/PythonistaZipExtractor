
import sys
import appex
import os
import shutil
from zipfile import ZipFile
from confirm_view import ConfirmView

import sharedlibs
sharedlibs.add_path_for('config_file')
from config_file import ConfigFile

config_path = 'app.config'
		
def first_run(config):
	config.set('FIRST_RUN', 'True')
	path = os.getcwd()
	tag = '/Pythonista3/Documents/'
	parts = path.split(tag)
	root = parts[0] + tag
	local = tag.join(parts[1:]) + os.sep + 'out'
	config.set('ROOT', root)
	config.set('DEST', local)
	config.save()
		
def main():
	if not appex.is_running_extension():
		print('Running in Pythonista app. Use via sharing extension with a .zip file instead.')
		exit(1)
	
	config = ConfigFile(config_path)
	if not config.key_exists('FIRST_RUN'):
		first_run(config)
		
	root = config.get('ROOT')
	dest = config.get('DEST')
	zip_src = appex.get_file_path()
	zip_name = zip_src.split(os.sep)[-1]
	
	cv = ConfirmView.load_view(dest, zip_name)
	cv.present()
	cv.wait_modal()
	
	if cv.proceed:
		new_dest = cv.path
		clear_first = cv.clearfirst
		if dest != new_dest:
			config.set('DEST', new_dest)
			dest = new_dest
			config.save()
		os.chdir(root)
		if clear_first and os.path.exists(dest):
			shutil.rmtree(dest)
		if not os.path.exists(dest):
			os.makedirs(dest)
		with ZipFile(zip_src, 'r') as zipo:
			zipo.extractall(dest)
		print('Done.')
	else:
		print('Cancelled by user.')
	
if __name__ == '__main__':
	main()
