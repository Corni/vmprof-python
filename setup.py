from setuptools import setup, find_packages, Extension
import os, sys

IS_PYPY = '__pypy__' in sys.builtin_module_names

if IS_PYPY:
    ext_modules = [] # built-in
else:
    extra_compile_args = []
    if sys.platform == 'win32':
        libraries = []
    elif sys.platform == 'darwin':
        libraries = []
        extra_compile_args = ['-Wno-unused']
    elif sys.platform.startswith('linux'):
        libraries = ['dl','unwind']
        extra_compile_args = ['-Wno-unused']
        if sys.maxsize == 2**63-1:
            libraries.append('unwind-x86_64')
        else:
            libraries.append('unwind-x86')
    else:
        raise NotImplementedError("platform '%s' is not supported!" % sys.platform)
    extra_compile_args.append('-I src/')
    ext_modules = [Extension('_vmprof',
                           sources=[
                               'src/libudis86/decode.c',
                               'src/libudis86/itab.c',
                               'src/libudis86/udis86.c',
                               'src/libudis86/syn.c',
                               'src/libudis86/syn-intel.c',
                               'src/libudis86/syn-att.c',
                               'src/_vmprof.c',
                               'src/stack.c',
                               'src/trampoline.c',
                               'src/machine.c',
                               'src/symboltable.c',
                               'src/compat.c',
                               ],
                           depends=[
                               'src/vmprof_main.h',
                               'src/vmprof_main_32.h',
                               'src/vmprof_mt.h',
                               'src/vmprof_common.h',
                           ],
                           extra_compile_args=extra_compile_args,
                           libraries=libraries)]

if sys.version_info[:2] >= (3, 3):
    extra_install_requires = []
else:
    extra_install_requires = ["backports.shutil_which"]

setup(
    name='vmprof',
    author='vmprof team',
    author_email='fijal@baroquesoftware.com',
    version="0.4.0.dev9",
    packages=find_packages(),
    description="Python's vmprof client",
    long_description='See https://vmprof.readthedocs.org/',
    url='https://github.com/vmprof/vmprof-python',
    install_requires=[
        'requests',
        'six',
        'pytz',
        'colorama',
    ] + extra_install_requires,
    tests_require=['pytest','cffi','hypothesis'],
    entry_points = {
        'console_scripts': [
            'vmprofshow = vmprof.show:main'
    ]},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=False,
    include_package_data=True,
    ext_modules=ext_modules,
)
