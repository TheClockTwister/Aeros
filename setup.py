import setuptools

with open("requirements.txt", "r") as fh:
    requirements = [x.strip("\n") for x in fh.readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Aeros",
    version="2.0.0b3",
    author="TheClockTwister",
    description="High-performance ASGI framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheClockTwister/Aeros",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # required for f"" string format notation
)
