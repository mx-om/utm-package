"""Setup for EmbedUrlXBlock."""

import os
from setuptools import setup,find_packages

def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='django-utm-tracker',
    version='0.1',
    packages=find_packages(include=['utm_tracker']),
    description='This utm-tracker provides a way to track utm source urls',
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'lms.djangoapp': [
            'utm_tracker = utm_tracker.apps:UtmTrackerConfig',
        ]
    },
    package_data=package_data("utm_tracker", "static"),
)
