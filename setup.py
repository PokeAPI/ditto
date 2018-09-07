import setuptools

setuptools.setup(
    name="ditto",
    version="0.1.0",
    url="https://github.com/PokeAPI/ditto",

    author="Sargun Vohra",
    author_email="sargun.vohra@gmail.com",

    description="Ditto is a server that serves a static copy of PokeAPI's data.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),
    scripts=['scripts/ditto'],

    install_requires=open('requirements.txt').read().splitlines(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
