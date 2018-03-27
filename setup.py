#                             MAB-VLSI 
#
#                                   Copyright 2018 
#     Regents of the University of California 
#                         All Rights Reserved
#
#                         
#  MAB-VLSI was developed by Shriram Kumar and Tushar Shah ai at
#  University of California, San Diego.
#
#  If your use of this software contributes to a published paper, we
#  request that you cite our paper that appears on our website 
#  http://vlsicad.ucsd.edu/MAB/MAB_v7.pdf
#
#  Permission to use, copy, and modify this software and its documentation is
#  granted only under the following terms and conditions.  Both the
#  above copyright notice and this permission notice must appear in all copies
#  of the software, derivative works or modified versions, and any portions
#  thereof, and both notices must appear in supporting documentation.
#
#  This software may be distributed (but not offered for sale or transferred
#  for compensation) to third parties, provided such third parties agree to
#  abide by the terms and conditions of this notice.
#
#  This software is distributed in the hope that it will be useful to the
#  community, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

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