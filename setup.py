from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ocp-cluster-login',
    version='v0.1.0',
    packages=find_packages(),
    include_package_data=True,
    author='dimak98',
    author_email='kazindevops@gmail.com',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=[
        'selenium>=3.141.0',
    ],
    entry_points={
        'console_scripts': [
            'ocp-cluster-login=ocp_cluster_login.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/dimak98/ocp-cluster-login',
        'Tracker': 'https://github.com/dimak98/ocp-cluster-login/issues',
    },
)