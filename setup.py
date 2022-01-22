from setuptools import setup

setup(
    name='pybuy',
    version='0.3.1',    
    description='A library for accessing Ebay REST API',
    url='https://github.com/APDevice/pyBuy',
    author='Dylan Luttrell',
    author_email='aplot_dev@icloud.com',
    license='MIT License',
    packages=['pybuy'],
    install_requires=['requests>=2.27.1',                    
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
    ],
)