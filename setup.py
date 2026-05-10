from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wallpaper-engine",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An interactive particle system wallpaper with flowing connections and hue shifting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wallpaper-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "wallpaper-engine=wallpaper_engine.app:main",
        ],
    },
)
