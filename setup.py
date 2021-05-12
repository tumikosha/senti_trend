import setuptools
from glob import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="senti_trend_tumikosha", # Replace with your own username
    version="1.0.0",
    author="Veaceslav Kunitki",
    author_email="tumikosha@gmail.com",
    description="Sentiment and Trend extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={
        'PKL': ['src/PKL/en_trend.pkl'],
    },
    data_files=[
        ('PKL', glob('src/PKL/*.pkl')),
    ],

    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)