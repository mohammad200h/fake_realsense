from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'fake_realsense'

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
        ('lib/python3.10/site-packages/' + package_name +'/demo_data/mustard0/',[
          package_name + '/demo_data/mustard0/mustard0.obj']),
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
