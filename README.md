# PyBitSet

PyBitSet is a very simple Python library to create and manage bitsets.

### Installation
```sh
$ git clone https://github.com/essessv/pybitset.git
$ cd pybitset
$ python setup.py install
```
### Running unit tests
The unit tests can be run using nosetests. There is a requirements.txt file included. To install the dependencies, run
```sh
$ pip install -r requirements.txt
```
to install nose in either a virtualenv or system as required.

To run the unit tests,
```sh
$ cd PyBitSet
$ nosetests -v
```
### Usage
Once installed,
```
Python 2.7.5 (default, Sep 12 2013, 21:33:34)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from pybitset.pybitset import BitSet
>>> b = BitSet(65535)
>>> b.size()
65535
>>> b.bitset_set(1000)
>>> b.bitset_is_set(999)
False
>>> b.bitset_is_set(1000)
True
>>> b.bitset_is_set(1001)
False
>>> b.bitset_set_range(start=65000, end=65100)
>>> b.bitset_count_set_bits()
102
>>> b.bitset_count_unset_bits()
65433
```

License
----

MIT

**Free Software, Hell Yeah!**
