from distutils.core import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
    name="speedrun.py",
    packages=["speedrunpy"],
    version="0.0.1",
    license="MIT",
    description="Async speedrun.com API wrapper",
    author="null2264",
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
