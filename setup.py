from setuptools import setup,find_namespace_packages
setup(
        name='financialworks',
        version='0.0.1',
        description='Time Series Analysis',
        #long_description=long_description,
        author='ansev',
        author_email='asevis0705@gmail.com',
        url='https://github.com/ansev-0',
        packages=find_namespace_packages(include=["src.*"]),
        include_package_data=True,
        #test_require = ['unittest']
            

    )