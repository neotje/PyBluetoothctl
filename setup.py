from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bluetoothctl",
    version="0.0.1",
    author="Neo Hop",
    author_email="neote111@gmail.com",
    description="A wrapper for the bluetoothctl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neotje/PyBluetoothctl",
    project_urls={
        "Bug Tracker": "https://github.com/neotje/PyBluetoothctl/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "pexpect==4.8.0",
        "PyBluez==0.23"
    ],
)