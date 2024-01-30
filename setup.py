from setuptools import setup

setup(
  name="tljh-neurodesk",
  author="SteffenBollmann",
  version="0.1",
  license="MIT",
  url="https://github.com/NeuroDesk/tljh-neurodesk",
  entry_points = {"tljh": ["neurodesk = tljh_neurodesk"]},
  py_modules=["tljh_neurodesk"]
)
