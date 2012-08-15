from distutils.core import setup

setup(
    name='asciidoc-aafigure-filter',
    version='0.1.0-SNAPSHOT',
    author='Jeremy Hughes',
    author_email='jed@jedatwork.com',
    packages=['asciidoc_aafigure_filter'],
    url='https://github.com/jedahu/asciidoc-aafigure-filter',
    license='GPL2',
    description='aafigure filter for AsciiDoc.',
    long_description=open('README').read(),
    include_package_data=True,
    install_requires=[
      'PIL==1.1.7',
      'aafigure==0.5',
      ]
    )
