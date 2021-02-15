from setuptools import setup

readme=""
with open('README.md') as f:
    readme = f.read()

setup(
    name="speedrun.py",
    packages=["speedrunpy"],
    version="0.0.10",
    license="MIT",
    description="Async API Wrapper for speedrun.com",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="null2264",
    author_email="palembani@gmail.com",
    url="https://github.com/null2264/speedrun.py",
    install_requires=[
        "aiohttp"
    ],
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
