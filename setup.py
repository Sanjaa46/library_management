from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

from library_management import __version__ as version

setup(
    name="library_management",
    version=version,
    description="Library Management System",
    author="Sanjaa",
    author_email="sanjaas880@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)