from setuptools import setup

setup(
    author="Kevin J. Delaney",
    author_email="kjdelaney@ucsd.edu",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    description="Creates synthetic REDCap-like records for software testing.",
    install_requires=[
        "Faker==15.0.0",
        "pandas==1.3.5",
        "typing>=3.7.4.3",
    ],
    license="",
    name="RecordSynthesizer",
    packages=[
        "dbmi_synthesizer",
        "dbmi_synthesizer.nickname_and_diminutive_names_lookup",
    ],
    url="https://github.com/DBMI/REDCapSynthesizer",
    version="0.0.1",
)
