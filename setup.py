import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nicehash-python",
    version="0.0.0",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/nicehash-python',
    keywords = ['nicehash','api','python'],
    description="NiceHash API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
            "python-dotenv>=0.17.0",
            "requests"
        ],
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