# This code is licensed under the New BSD License
# 2009, Alexander Artemenko <svetlyak.40wt@gmail.com>
# For other contacts, visit http://aartemenko.com

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name = 'gtdzen',
    version = __import__('gtdzen').__version__,
    description = 'Simple but flexible Getting Things Done task manager with tag-oriented workflow.',
    long_description = open('README.markdown').read(),
    author = 'Alexander Artemenko',
    author_email = 'svetlyak.40wt@gmail.com',
    license = 'New BSD License',
    keywords = 'GTD, TODO, time management',
    url = 'http://github.com/svetlyak40wt/gtdzen/',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'SQLAlchemy',
        'Elixir',
        'sqlalchemy-migrate',
    ],
    tests_require = ['nose >= 0.10'],
    entry_points = """
        [console_scripts]
        gtd = gtdzen.client:main
        """,
    test_suite = "nose.collector",
)

