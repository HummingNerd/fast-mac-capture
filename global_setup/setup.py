from setuptools import setup, find_packages

setup(
    name='fast_mac_capture',
    version='1.0.0',
    packages=find_packages(),
    # This ensures the .dylib file is included in the installation
    package_data={'fast_mac_capture': ['*.dylib']},
    install_requires=[
        'numpy'
    ],
)