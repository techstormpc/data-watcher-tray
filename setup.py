from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

install_requires = [
    "PyQt6==6.3.1"
]

setup(
    name='data-watcher-tray',
    version='0.0.1',
    author='TechStorm PC',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Intended Audience :: Information Technology",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    author_email='nathan@techstormpc.com',
    description='System tray app and task runner used for watching files',
    packages=find_packages(include=['data_watcher*']),
    install_requires=install_requires,
    url='https://github.com/techstormpc/data-watcher-tray',
    long_description=long_description,
    long_description_content_type='text/markdown'
)