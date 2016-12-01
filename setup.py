import codecs
import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

REQUIREMENTS = [
    'mohawk',
    'requests',
    'requests-hawk',
    'six',
]

setup(name='ipreputation',
      version='0.0.1',
      description='IP Reputation Python Client',
      long_description=README,
      license='MPL (2.0)',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
      ],
      keywords="web services",
      author='Mozilla Services',
      author_email='services-dev@mozilla.com',
      url='https://github.com/mozilla-services/ip-reputation-python-client',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS)
