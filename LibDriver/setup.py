from setuptools import setup, find_packages

setup(
    name='ThalamusEngine',
    version='0.1.0',
    description='ThalamusEngine for Recognition of 3D',
    author='Thomas A. Anderson',
    author_email='pjtthalamus@gmail.com',
    #url='https://blog.d4v1d.com/setup-py',
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.0',
        'opencv-contrib-python>=4.0'
    ],
    package_data={'ThalamusPjt': ['Lib/freeglut.dll', 'Lib/opencv_world450d.dll.dll', 'Lib/Simul3DDLL.dll']}
)