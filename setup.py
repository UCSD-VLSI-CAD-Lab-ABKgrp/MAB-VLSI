from setuptools import setup

setup(name='mab',
      version='1.0',
      description='Module that provides components for the MAB-VLSI project',
      url='https://github.com/ShriramKumar/mab_vlsi',
      author='Shriram Kumar, Tushar Shah',
      author_email='shriramck@gmail.com',
      packages=['mab'],
      install_requires=[
      'pytest-cov',
      'numpy',
      'scipy',
      'uuid',
      'pymc3',
      ],
      zip_safe=False)