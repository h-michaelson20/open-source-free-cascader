
from setuptools import setup, find_packages

setup(
    name="my_cascade_library",
    version="0.1.0",
    packages=find_packages(where='src'),  # Specify the source directory
    package_dir={'': 'src'},  # Tell setuptools to look for packages in src
    install_requires=[
        "requests",
    ],
    author="Henry Michaelson and Yash Agrawal",
    description="A library for free cascading LLM API calls.",
    url="https://github.com/yourusername/my_cascade_library",  # Update with your repository URL
    entry_points={
        'console_scripts': [
            'llm-cascade=src.cascade:main',  # Create a command line entry point
        ],
    },
)