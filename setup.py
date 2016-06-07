from setuptools import setup

setup(name='ugent-biblio',
      version='0.1.0',
      description='Connector to the API of Ghent University Academic Bibliography',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python',
      ],
      author='Stef Bastiaansen',
      author_email='stef.bastiaansen@ugent.be',
      url='https://github.com/megasnort/python-ugent-biblio',
      packages=['biblio'],
      keywords='UGent biblio library publications',
      install_requires=[
          'requests',
      ],
      setup_requires=['pytest-runner'],
      test_suite='pytest',
      include_package_data=True,
      zip_safe=False
      )
