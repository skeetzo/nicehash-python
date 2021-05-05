import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nicehash-python",
    version="0.0.1",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/nicehash-python',
    keywords = ['nicehash','api','python'],
    description="NiceHash API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']), # Include all the python modules except `tests`.
    include_package_data=True,
    install_requires=[
            "requests"
        ],
    extras_require={
        'dev': [
            'dotenv-python'
        ]
    },
    entry_points={
        'console_scripts' : [
            'nicehash = python.nicehash:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

    # entry_points={
    #     'pytest11': [
    #         'nicehash_python = nicehash_python.fixtures'
    #     ]
    # },
