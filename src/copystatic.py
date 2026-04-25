import os
import shutil


def copy_files_recursive(source, dest):
	if os.path.exists(dest):
		shutil.rmtree(dest)
	os.mkdir(dest)
	dir_list = os.listdir(source)
	for item in dir_list:
		from_path = os.path.join(source, item)
		to_path = os.path.join(dest, item)
		if os.path.isfile(from_path):
			shutil.copy(from_path, to_path)
		else:
			copy_files_recursive(from_path, to_path)
    
