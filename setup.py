"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(

    name='powerjob',
    version='0.0.1',
    description='Enterprise job scheduling middleware with distributed computing ability.',
    url='https://github.com/PowerJob/powerjob-python',
    author='Teng Jiqi',
    author_email='tengjiqi@gmail.com',
    keywords='job-scheduler, task-scheduler, scheduler, workflow',
    python_requires='>=3.6, <4',

    # Setuptools 模块提供了一个 find_packages 函数,它默认在与 setup.py 文件同一目录下搜索各个含有 __init__.py 的目录做为要添加的包
    packages=find_packages(where='.'),
    # 依赖的其他包，比如 'requests', 'django>=1.11, !=1.11.1, <=2'
    install_requires=[],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/PowerJob/powerjob-python/issues',
        'Funding': 'https://opencollective.com/powerjob',
        'Say Thanks!': 'https://github.com/PowerJob/PowerJob/issues/6',
        'Source': 'https://github.com/PowerJob/powerjob-python',
    },
)