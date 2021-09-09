from setuptools import setup, find_namespace_packages

setup(
    name='vsdkx-addon-depth',
    url='https://github.com/natix-io/vsdkx-addon-depth',
    author='Guja',
    author_email='g.mekokishvili@omedia.ge',
    namespace_packages=['vsdkx', 'vsdkx.addon'],
    packages=find_namespace_packages(include=['vsdkx*']),
    dependency_links=[
        'https://github.com/natix-io/vsdkx-core.git#egg=vsdkx-core'
    ],
    install_requires=[
        'vsdkx-core',
        'opencv-contrib-python==4.4.0.46',
        'timm==0.4.12',
        'torch==1.9.0',
        'torchvision==0.10.0',
        'pandas==1.3.0',
        'requests==2.26.0',
        'tqdm==4.62.0',
        'matplotlib==3.4.2',
        'seaborn==0.11.1',
        'pillow==8.2.0',
        'numpy==1.20.2',
        'pyyaml==5.3.1'
    ],
    version='1.0',
)
