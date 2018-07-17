from setuptools import setup

setup(name='windi',
      version='0.1',
      description='Wrapper for pyindi',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Natural Language :: English',
            'Operating System :: OS Independent',
      ],
      keywords='pyindi pyindi-client camera',
      url='https://gitlab.com/parsaalian0/windi',
      authors='Parsa Alian & Emad Salehi',
      author_email='emad.s1178@yahoo.com',
      license='MIT',
      packages=['windi'],
      install_requires=[
            'subprocess',
      ],
      zip_safe=False)
