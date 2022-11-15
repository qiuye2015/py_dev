from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),  # 告诉 Python 要包含哪些包目录（以及它们包含的 Python 文件）; find_packages()自动找到这些目录，因此您不必输入它们
    include_package_data=True,  # 设置包含其他文件，例如静态和模板目录; 需要另一个名为的文件 MANIFEST.in来告诉这个其他数据是什么
    install_requires=[
        'flask',
    ],
)
