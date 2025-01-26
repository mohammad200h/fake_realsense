from setuptools import find_packages, setup
import os
from glob import glob

from setuptools.command.build_py import build_py
import subprocess

import zipfile

package_name = 'fake_realsense'



def install_gdown():
    try:
      subprocess.check_call(['pip3','install','gdown'])
    except subprocess.CalledProcessError as e:
      print(f'Error installing gdown: {e}')
      raise

def download():

  print("\n\n")
  print("Runing BUild....bro!")
  print("\n\n")
   # Ensure the demo_data directory exists
  demo_data_dir = os.path.join(package_name, 'demo_data')
  os.makedirs(demo_data_dir, exist_ok=True)
  # Download the Google Drive folder using gdown
  google_drive_folder_url = 'https://drive.google.com/drive/folders/1pRyFmxYXmAnpku7nGRioZaKrVJtIsroP'
  try:
      print(f'Downloading Google Drive folder: {google_drive_folder_url}')
      subprocess.check_call([
          'gdown', '--folder', google_drive_folder_url, '-O', demo_data_dir
      ])
      print('Google Drive download complete.')
  except subprocess.CalledProcessError as e:
      print(f'Error downloading Google Drive folder: {e}')
      raise
  # Proceed with the rest of the build process

def extract_mustard0():

    demo_data_dir = os.path.join(package_name, 'demo_data')
    mustard_zip_path = os.path.join(demo_data_dir, 'mustard0.zip')  # Path to the mustard0.zip file

    if os.path.exists(mustard_zip_path):
        with zipfile.ZipFile(mustard_zip_path, 'r') as zip_ref:
            # Only extract the contents of mustard0.zip
            zip_ref.extractall(demo_data_dir)

    else:
        print(f"File {mustard_zip_path} not found. Skipping extraction.")


install_gdown()
download()
extract_mustard0()



setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # mustard0 rgb
        ('lib/python3.10/site-packages/' + package_name +'/demo_data/mustard0/rgb/',[
          package_name + f'/demo_data/mustard0/rgb/{filename}'for filename in
          os.listdir(package_name + f'/demo_data/mustard0/rgb/')
          if filename.endswith('.png')
        ]),
        # mustard0 mesh
        ('lib/python3.10/site-packages/' + package_name +'/demo_data/mustard0/mesh/',[
          package_name + '/demo_data/mustard0/mesh/textured_simple.obj']),
        # mustard0 depth
        ('lib/python3.10/site-packages/' + package_name +'/demo_data/mustard0/depth/',[
          package_name + f'/demo_data/mustard0/depth/{filename}'for filename in
          os.listdir(package_name + f'/demo_data/mustard0/depth/')
          if filename.endswith('.png')
        ]),
        # mustard0 masks
        ('lib/python3.10/site-packages/' + package_name +'/demo_data/mustard0/masks/',[
          package_name + f'/demo_data/mustard0/masks/{filename}'for filename in
          os.listdir(package_name + f'/demo_data/mustard0/masks/')
          if filename.endswith('.png')
        ]),
        # launch files
        (os.path.join('share', package_name, 'launch/'),
         glob('launch/*launch.[pxy][yma]*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mamad',
    maintainer_email='mamad@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        # used for testing
        'fake_realsense = fake_realsense.fake_realsense_node:main',
        ],
    },
)
