from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='pyri-device-manager',
    version='0.1.0',
    description='PyRI Teach Pendant Device Manager',
    author='John Wason',
    author_email='wason@wasontech.com',
    url='http://pyri.tech',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    package_data = {
        'pyri.device_manager': ['*.robdef','*.yml']
    },
    zip_safe=False,
    install_requires=[
        'pyri-common',
        'robotraconteur'
    ],
    tests_require=['pytest','pytest-asyncio'],
    extras_require={
        'test': ['pytest','pytest-asyncio']
    },
    entry_points = {
        'pyri.plugins.robdef': ['pyri-device-manager-robdef=pyri.device_manager.robdef:get_robdef_factory'],
        'console_scripts': ['pyri-device-manager-service = pyri.device_manager.__main__:main']
    }
)