import setuptools

setuptools.setup(
    name="ditto",
    version="0.1.0",
    url="https://github.com/pokesource/ditto",

    author="Sargun Vohra",
    author_email="sargunvdev@gmail.com",

    description="Ditto is a server that serves a static copy of PokeAPI's data.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),
    scripts=['scripts/ditto'],

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
