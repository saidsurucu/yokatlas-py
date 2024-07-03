from setuptools import setup, find_packages

setup(
    name="yokatlas-py",
    version="0.1.0",
    author="Said Sürücü",
    author_email="saidsrc@gmail.com",
    description="A python wrapper for YOKATLAS API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/saidsurucu/yokatlas-py",  # Update with your repository URL
    packages=find_packages(include=['yokatlas_py', 'yokatlas_py.*']),
    install_requires=[
        "fastapi",
        "pydantic",
        "requests",
        "uvicorn",
        "urllib3",
        "aiohttp"   
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
