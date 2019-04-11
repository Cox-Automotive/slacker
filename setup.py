from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


setup(
    name='slackest',
    version='0.13.2',
    packages=['slackest'],
    description='Slack API client',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Cox Automotive Cloud Team',
    author_email='andrew.sledge@coxautoinc.com',
    url='http://github.com/Cox-Automotive/slackest/',
    install_requires=['requests >= 2.2.1'],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='slack api'
)
