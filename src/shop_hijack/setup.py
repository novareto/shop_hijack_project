from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='shop_hijack',
      version=version,
      description="",
      long_description=""" """,
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'uvc.layout',
          'dolmen.content',
          'dolmen.message',
          'dolmen.menu',
      ],
      entry_points={
         'fanstatic.libraries': [
            'shop_hijack = shop_hijack.resources:library',
         ],
         'paste.app_factory': [
             'app = shop_hijack.app:app_factory',
         ],
      }
      )
