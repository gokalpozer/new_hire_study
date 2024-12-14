from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="my_project",
    version="1.0",
    packages=find_packages(include=["src", "resources", "config", "data"]),
    package_data={
        'src': ['*.sql'],
        'config': ['*.yaml'],
        'data': ['*.json'],
        # ... other package data ...
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "run-my-project=src.main:run",
        ],
    },
)
