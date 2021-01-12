import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-ngrok",
    version="0.0.26",
    author="",
    description="A simple way to demo Flask apps from your machine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='flask ngrok',
    install_requires=['Flask>=0.8', 'requests'],
    py_modules=['flask_ngrok']
)
