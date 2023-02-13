#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup,find_packages,find_namespace_packages
from mb_milvus.src.version import version

setup(
    name="mb_milvus",
    version=version,
    description="Basic milvus package",
    author=["Malav Bateriwala"],
    packages=find_namespace_packages(include=["mb_milvus.*"]),
    #packages=find_packages(),
    scripts=['scripts/df_profile','scripts/df_view'],
    install_requires=[
        "numpy",
        "pandas",
        "colorama",],
    python_requires='>=3.8',)
