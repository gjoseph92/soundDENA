from setuptools import setup, find_packages
import os

setup(
    name= "soundDB",
    version= "0.0.1",
    description= "A tool for accessing the NSNSD hierarchical file structure like a queryable database",
    url= "https://github.com/gjoseph92/soundDB",
    author= "Gabe Joseph",
    author_email= "gjoseph92@gmail.com",

    packages= find_packages(exclude= ["doc"]),
    install_requires= ['numpy', 'pandas']

    )
