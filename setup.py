from setuptools import setup
import sys

required = ['requests', 'markdownify', 'bs4', 'unidecode', 'fake_useragent', 'lxml']
long_description = ""
with open('README.md') as f:
    long_description += f.read()

setup(
    name='eksipy',
    version='1.0.2',
    description='Unofficial API for Eksi Sozluk.',
    long_description=long_description,
    author='Yusuf Usta',
    author_email='yusuf@fusuf.codes',
    maintainer='Yusuf Usta',
    maintainer_email='yusuf@fusuf.codes',
    url='https://github.com/quiec/EksiPy',
    license='GPL3',
    packages=['eksipy'],
    install_requires=required,
    keywords=['eksi', 'eksisozluk', 'api', 'eksi-sozluk'],
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)