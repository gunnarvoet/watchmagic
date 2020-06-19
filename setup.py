from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

setup(
    name="watchmagic",
    version="0.1.0",
    author="Gunnar Voet",
    author_email="gvoet@ucsd.edu",
    url="https://github.com/gunnarvoet/watchmagic",
    license="GNU GPL v3",
    # Description
    description="Add watchdog to IPython cells",
    long_description=f"{readme}\n\n{history}",
    long_description_content_type="text/x-rst",
    # Requirements
    python_requires=">=3.0",
    install_requires=[
        "watchdog",
        "IPython",
    ],
    # Packaging
    packages=find_packages(include=["watchdog"], exclude=["*.tests"]),
    zip_safe=False,
    platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
    # Metadata
    project_urls={"Documentation": "https://github.com/gunnarvoet/watchmagic"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
