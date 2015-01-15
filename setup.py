from setuptools import setup, find_packages

setup(name='dkt',
      version='0.0.1',
      description='Docker tool',
      packages=find_packages(),
      install_requires=[
          'requests',
          'ConfigArgParse'
      ],
      entry_points={'console_scripts': ['dkt=dkt.cli:main']},
      url='http://github.com/residentsummer/dkt',
      author='Anton S',
      author_email='residentsummer+dkt@gmail.com',
      license='MIT',
      zip_safe=False)

