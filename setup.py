import setuptools

with open("requirements.txt", "r") as fh:
    requirements = [x[:-1] for x in fh.readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Aeros",
    version="1.0.3",
    author="TheClockTwister",
    description="High-performance ASGI framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheClockTwister/Aeros",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
