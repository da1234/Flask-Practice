from setuptools import find_packages, setup

setup(
      name='flaskr',
      version='1.0.0',
      packages=find_packages(), #packages/dirs that contain relevant python files
      include_package_data=True, #To include other files, such as the static and templates directories, include_package_data is set.
      zip_safe=False,
      install_requires=[
              'flask',
              ],
)

[tool:pytest]
testpaths = tests

[coverage:run]
branch = True
source =
    flaskr
