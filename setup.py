import json
from setuptools import setup


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name="lexibank_crossandean",
    description=metadata["title"],
    license=metadata.get("license", ""),
    url=metadata.get("url", ""),
    py_modules=["lexibank_crossandean"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "lexibank.dataset": ["blumquechua=lexibank_crossandean:Dataset"],
        "cldfbench.commands": ["crossandean=crossandeancommands"],
    },
    install_requires=["pylexibank>=3.0"],
    extras_require={
        "test": ["pytest-cldf"],
        # 'commands': []
        },
)
