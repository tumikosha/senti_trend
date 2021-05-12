import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="senti_trend_tumikosha", # Replace with your own username
    version="1.0.0",
    author="Veaceslav Kunitki",
    author_email="tumikosha@gmail.com",
    description="Sentiment and Trend extractor for En, Ro , RU, Es, Vi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tumikosha/senti_trend",
    project_urls={
        "Bug Tracker": "https://github.com/tumikosha/senti_trend/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)