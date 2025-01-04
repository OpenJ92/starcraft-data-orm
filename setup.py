from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="starcraft-data-orm",  # Your package name
    version="0.1.1",  # Version number
    description="A Python package for StarCraft replay data ORM integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jacob Vartuli-Schonberg",
    author_email="jacob.vartuli.schonberg@gmail.com",
    url="https://github.com/OpenJ92/starcraft-data-orm",  # Your repository
    license="MIT",  # Replace with your license
    packages=find_packages(),  # Automatically find your package
    install_requires=requirements,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

