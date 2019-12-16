import setuptools


setuptools.setup(
    name="map_modifiers",
    version="0.1",
    packages=['map_modifiers'],

    package_data={
        'map_modifiers': ['*.json'],
    },
    description="Medical concept normalization with severity modifiers"
)
