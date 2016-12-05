from setuptools import setup

setup(name='smart_car',
	    version='0.1',
	    description='Smart car',
	    url='https://github.com/bezirganyan/mechanics_smart_car',
	    author='Grigor Bezirganyan',
	    author_email='grigor.bezirganyan98@gmail.com',
	    license='GPL-3.0',
	    packages=['smart_car'],
	    zip_safe=False,
	    install_requires=[
		  'pyqtgraph',
		  'numpy'
		  ],
	    )
