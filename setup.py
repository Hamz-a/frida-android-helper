from distutils.core import setup


with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="fridaandroidhelper",
    description="Handy Android frida helping tools at the tip of your terminal",
    version="0.1",
    packages=["fah"],
    requires=requirements,
    install_requires=requirements,
    license="MIT",
    keywords="frida android helper",
    entry_points={
        'console_scripts': [
            'fah.fah:main'
        ]
    },
)
