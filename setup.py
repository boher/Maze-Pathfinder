from setuptools import setup, find_packages

setup(name="maze-pathfinder",
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      py_modules=["colour"]
      )
