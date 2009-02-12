from distutils.core import setup

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
    packages = ['gtdzen'],
    scripts = ['gtd'],
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
    requires = [
        'SQLAlchemy',
        'Elixir',
    ],
)

