from setuptools import setup  # type: ignore[import]  # noqa: F401

setup(
    author="Kevin J. Delaney",
    author_email="kjdelaney@ucsd.edu",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    description="Creates synthetic REDCap-like records for software testing.",
    include_package_data=True,
    install_requires=[
        "Faker>=15.3.4",
        "pandas==1.3.5",
        "typing==3.7.4.3",
    ],
    license="",
    name="REDCapRecordSynthesizer",
    package_dir={"": "src"},
    packages=[
        "redcaprecordsynthesizer",
    ],
    url="https://github.com/DBMI/REDCapRecordSynthesizer",
    version="0.5.8",
)
