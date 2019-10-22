from distutils.core import setup
import setuptools

with open("requirements.txt") as f:
    requirements = f.readlines()


setup(
    name="frida-android-helper",
    description="Handy Android frida helping tools at the tip of your terminal",
    version="0.2",
    packages=["frida_android_helper"],
    install_requires=requirements,
    zip_safe=True,
    license="MIT",
    keywords="frida android helper",
    entry_points={
        'console_scripts': [
            'fah = frida_android_helper.fah:main'
        ]
    },
)
