"""Setup module for AdaM."""

from setuptools import setup, find_packages

setup(
        name='adam-dui',
        version='0.1',
        description='Automatic adaptation of GUIs to multiple devices and '
                    'users in real-time.',

        author='Seonwook Park',
        author_email='spark@inf.ethz.ch',

        packages=find_packages(exclude=[]),
        python_requires='>=2.7',
        install_requires=[
            'matplotlib',
            'numpy',
            'websocket-server',
        ],
)
