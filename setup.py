from setuptools import setup

setup(name='epihan',
      version='0.0',
      description='Tools for transcribing Chinese into IPA.',
      url='http://github.com/dmort27/epihan',
      download_url='http://github.com/dmort27/epihan/tarball/0.0',
      author='David R. Mortensen',
      author_email='dmortens@cs.cmu.edu',
      license='MIT',
      install_requires=['setuptools',
                        'unicodecsv',
                        'regex',
                        'panphon>=0.3'],
      packages=['epihan'],
      package_dir={'epitran': 'epitran'},
      package_data={'epitran': ['data/*.csv']},
      zip_safe=True
      )
