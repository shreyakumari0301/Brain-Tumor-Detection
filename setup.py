from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brain-tumor-detection",
    version="1.0.0",
    author="Shreya Kumari",
    description="Brain Tumor Detection using CNN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shreyakumari0301/Brain-Tumor-Detection",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "python-multipart>=0.0.6",
        "streamlit>=1.28.1",
        "torch>=2.1.0",
        "torchvision>=0.16.0",
        "opencv-python>=4.8.1",
        "pillow>=10.1.0",
        "numpy>=1.24.3,<2.0.0",
        "requests>=2.31.0",
        "scikit-learn>=1.3.2",
        "seaborn>=0.13.0",
        "matplotlib>=3.8.2",
    ],
)

