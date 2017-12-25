"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

if __name__ == '__main__':
    here = path.abspath(path.dirname(__file__))

    # Get the long description from the README file
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    requirements = ['peppercorn']
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        requirements.append(f.read().splitlines())

    setup(
        name='vision',

        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        version='0.1.0',

        description='A framework for Date Presentation.',
        long_description=long_description,
        url='https://github.com/GuangTianLi/vision',

        # Author details
        author='GuangTian Li',
        # author_email='pypa-dev@googlegroups.com',

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        packages=find_packages(exclude=('tests', 'tests.*')),

        # List run-time dependencies here.  These will be installed by pip when
        # your project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        # package_data={
        # },

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        include_package_data=True,

        install_requires=requirements,

        # Although 'package_data' is the preferred approach, in some case you may
        # need to place data files outside of your packages. See:
        # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
        # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
        # data_files=[('my_data', ['data/data_file'])],

        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        entry_points={
            'console_scripts': [
                'vision = vision.cmdline:execute',
            ],
        },
    )
