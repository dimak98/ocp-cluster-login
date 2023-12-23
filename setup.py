from setuptools import setup, find_packages

setup(
    name='ocp-cluster-login',
    version='v1.0.0',
    packages=find_packages(),
    include_package_data=True,
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
        'Tracker': 'https://github.com/dimak98/ocp-cluster-login/',
    },
)