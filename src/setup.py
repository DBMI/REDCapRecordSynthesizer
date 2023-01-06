from setuptools import setup

setup(
    author="Kevin J. Delaney",
    author_email="kjdelaney@ucsd.edu",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    description="Creates synthetic REDCap-like records for software testing.",
    include_package_data=True,
    install_requires=[
        "Faker==15.0.0",
        "pandas==1.3.5",
        "typing==3.7.4.3",
    ],
    license="",
    name="REDCapRecordSynthesizer",
    package_dir={"": "src"},
    packages=[
        "redcap_record_synthesizer",
        "redcap_record_synthesizer.nickname_lookup",
    ],
    url="https://github.com/DBMI/REDCapRecordSynthesizer",
    version="0.3.0",
)