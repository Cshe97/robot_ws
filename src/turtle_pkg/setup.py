from setuptools import setup

package_name = 'turtle_pkg'

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
    maintainer='cshe97',
    maintainer_email='cshe97@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'remote_turtle = turtle_pkg.remote_turtle:main',
        'rotate_turtle = turtle_pkg.rotate_turtle:main',
        'rotate_turtle2 = turtle_pkg.pro_rotate_turtle:main',
        'circle = turtle_pkg.move_turtle:main',
        'sub_pose = turtle_pkg.sub_pose:main',
        ],
    },
)
