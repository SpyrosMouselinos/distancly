from setuptools import setup, find_packages

setup(
    name='distancly',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A python package to implement all different distance/routing methods (Great Circle/Rhumbline/Haversine/Eucledian).',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/SpyrosMouselinos/distancly',
    author='Mouselinos Spyridon',
    author_email='mouselinos.spur.kw@gmail.com'
)
