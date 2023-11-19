from setuptools import find_packages
from setuptools import setup

package_name = 'nav_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gnd0',
    maintainer_email='greattoe@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'follow1 = nav_pkg.follow_waypoints1:main',
                'follow2 = nav_pkg.follow_waypoints2:main',
                'pub_nav_msg = nav_pkg.pub_nav_msg:main',
                'follow3 = nav_pkg.follow_waypoints:main',
                'follow_ji = nav_pkg.follow_waypoints_ji:main',
                
                
                
        ],
    },
)
