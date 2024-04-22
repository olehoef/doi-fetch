from setuptools import setup, find_packages

setup(
    name='doi-fetch',
    version='2.0',
    # py_modules=['cli', 'crossrefRequests', 'sjr', 'rest'],
    packages=['doi_fetch.datamodel', 'doi_fetch.scripts', 'doi_fetch.utils'],
    include_package_data=True,
    install_requires=[
        'click',
        'Flask',
        'Requests',
        'inquirer',
        'trogon'
    ],
    package_data={'doi-fetch/persistence': ['works.json', 'config.json'],'sjr-data': ['*.csv'], '': ['config.json']},
    entry_points={
        'console_scripts': [
            'doi-fetch = doi_fetch.scripts.doi_fetch:doi_fetch',
        ],
    },
)