import setuptools

import pinboard

setuptools.setup(
    name="pinboard",
    version=pinboard.__version__,
    description="A collection of useful Pinboard commands",
    license="MIT",
    url="https://github.com/keith/pinboard",
    author="Keith Smiley",
    author_email="keithbsmiley@gmail.com",
    install_requires=[
        "requests==2.31.0",
    ],
    packages=["pinboard", "pinboard.helpers"],
    entry_points={"console_scripts": ["pinboard=pinboard.__main__:main"]},
)
