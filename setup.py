import setuptools
from distutils.core import setup

with open("requirements.txt") as f:
    requirements = f.readlines()


setup(
    name="frida-android-helper",
    description="Handy Android frida helping tools at the tip of your terminal",
    version="0.6.3",
    packages=["frida_android_helper"],
    package_data={"frida_android_helper": ["frida_hooks/*.js"]},
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
