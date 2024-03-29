from setuptools import setup

setup(name='YourAppName',
      version='1.0',
      description='OpenShift App',
      author='Your Name',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.7.2',
                        'MarkupSafe',
                        'mongoengine>=0.14.0',
                        'flask-mongoengine>=0.9.3'],
      )
