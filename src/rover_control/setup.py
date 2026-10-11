from setuptools import find_packages, setup

package_name = 'rover_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abhinav',
    maintainer_email='abhinavbhandari905@gmail.com',
    description='Control nodes for the rover',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drive_forward = rover_control.drive_forward:main',
            'scan_reader = rover_control.scan_reader:main',
            'obstacle_avoider = rover_control.obstacle_avoider:main',
        ],
    },
)
