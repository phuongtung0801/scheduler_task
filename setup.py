from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in scheduler_task/__init__.py
from scheduler_task import __version__ as version

setup(
	name="scheduler_task",
	version=version,
	description="send email pdf report scheduled",
	author="Tung",
	author_email="phuongtung0801@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
