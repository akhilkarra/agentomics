from setuptools import find_packages, setup

setup(
    name="agentomics",  # Name of your package
    version="0.1.0",  # Version of your package
    author="Akhil Karra",  # Your name
    author_email="akarra@andrew.cmu.edu",  # Your email
    description="A package for agent-based economic simulations.",  # Short description
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/akhilkarra/agentomics",  # URL to your project
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
    install_requires=[
        # List your package dependencies here
        "langroid"
    ],
)
