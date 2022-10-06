from setuptools import setup

setup(name='us treas',
      version='0.0',
      url='http://github.com/lathaniel/us-treas',
      author='Adam Lathan',
      license='MIT',
      packages=['src/ustreas'],
      install_requires=[
          'pandas==1.3.4',
      ],
      zip_safe=False)
