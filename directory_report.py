import sys
import os
import argparse
from tabulate import tabulate
from hurry.filesize import size

def get_script_path():
	return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_folder_size(folder):
	total_size = os.path.getsize(folder)
	for item in os.listdir(folder):
		itempath = os.path.join(folder, item)
		if os.path.isfile(itempath):
			total_size += os.path.getsize(itempath)
		elif os.path.isdir(itempath):
			total_size += get_folder_size(itempath)
	return total_size

def list_subfolders(rootdir):
	folders = []
	for item in os.listdir(rootdir):
		itempath = os.path.join(rootdir, item)
		if os.path.isdir(itempath):
			folders.append(itempath)
	return folders

def list_files(rootdir):
	files = []
	for item in os.listdir(rootdir):
		itempath = os.path.join(rootdir, item)
		if os.path.isfile(itempath):
			files.append(itempath)
	return files

parser = argparse.ArgumentParser(description='A tool for reporting on the largest user directories.')
parser.add_argument('--directory', help='Specified directory to report on.', type=str)

args = parser.parse_args()

home_directory = get_script_path()

if(args.directory is not None):
	if(os.path.isdir(args.directory)):
		print("Supplied directory is valid.")
		home_directory=args.directory
	else:
		print("Argument supplied to directory is invalid. Using script current directory.")
else:
	print("No directory argument defined. Using script root directory.")

tabulated_folder_data = []

print(list_subfolders(home_directory))

for items in list_subfolders(home_directory):
	tabulated_folder_data.append([items, 'Folder',size(get_folder_size(items))])

for item in list_files(home_directory):
	tabulated_folder_data.append([item, 'File',size(os.path.getsize(item))])

print(tabulate(tabulated_folder_data, headers=['Item','File Type','Size']))
