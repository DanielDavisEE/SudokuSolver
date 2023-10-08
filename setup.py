from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='sudoku-solver',
    version='1.0',
    author='Daniel Davis',
    description='',
    long_description=long_description,
    url='https://github.com/DanielDavisEE/SudokuSolver',
    python_requires='>=3.10, <4',
    package_dir={'': 'src'},
    packages=['sudoku_solver'],
    install_requires=[
        'pygame'
    ],
    package_data={
    },
    entry_points={
    }
)
