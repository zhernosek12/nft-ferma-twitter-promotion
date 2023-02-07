import setuptools
from setuptools import setup

setup(
    include_package_data=True,
    name='zhnftfermatwitter',
    version='0.0.9',
    packages=setuptools.find_packages(),
    install_requires=["requests", "selenium"],
    url='http://ferma.zhernosek.xyz/',
    license='',
    author='Zhernosek Andrei',
    author_email='zhernosek12@gmail.com',
    description=''
)
