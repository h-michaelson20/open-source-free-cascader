
from setuptools import setup, find_packages

setup(
    name="free_apis_llm_cascade",
    version="0.1.0",
    packages=find_packages(where='free_apis_llm_cascade'),  # Specify the source directory
    package_dir={'': 'free_apis_llm_cascade'},  # Tell setuptools to look for packages in src
    install_requires=[
        "requests",
    ],
    author="Henry Michaelson and Yash Agrawal",
    description="A library for free cascading LLM API calls.",
    url="https://github.com/h-michaelson20/open-source-free-cascader",  # Update with your repository URL
)