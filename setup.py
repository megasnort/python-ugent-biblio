from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ugentbiblio',
      version='0.2.0',
      description='Connector to the API of Ghent University Academic Bibliography',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python',
      ],
      author='Stef Bastiaansen',
      author_email='stef.bastiaansen@ugent.be',
      url='https://github.com/megasnort/python-ugent-biblio',
      packages=['biblio'],
      keywords='ugent biblio library publications',
      license='Apache',
      install_requires=[
          'requests',
      ],
      setup_requires=['pytest-runner'],
      test_suite='pytest',
      include_package_data=True,
      zip_safe=False
      )
