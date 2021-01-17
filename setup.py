from setuptools import setup, find_packages

setup(
    name='Py2048',
    url='https://github.com/andnp/Py2048.git',
    author='Andy Patterson',
    author_email='andnpatterson@gmail.com',
    packages=find_packages(exclude=['tests*', 'scripts*']),
    install_requires=[
        "numpy>=1.19.5",
        "numba>=0.52.0",
    ],
    version=0.0,
    license='MIT',
    description='A quick implementation of the popular 2048 game',
    long_description='todo',
)
