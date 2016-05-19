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
                        'panphon>=0.3',
                        'marisa_trie'],
      scripts=['epihan/bin/zh2ipaspace.py'],
      packages=['epihan'],
      package_dir={'epihan': 'epihan'},
      package_data={'epihan': ['data/*.csv', 'data/*.txt']},
      zip_safe=True
      )
