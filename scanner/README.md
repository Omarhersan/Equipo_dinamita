# Scanner

This is a simple python application that facilitates scanning the filesystem content.

## Context

Before working in the infrastructure, be sure to have implemented the following functions:
* `list_files`
* `scan_path`

### Function: List Files

Create a python function called `list_files` that receives a `target_path` as an input and returns a generator where each item is a string containing all the files in the target directory. If the `include_nested` boolean argument is set to true, the result should contain all the nested files as well.

```python=
from typing import Generator


def list_files(target_path: str, include_nested: bool = False) -> Generator:
    pass

```

### Function: Scan Path


Create a function called `scan_path` that returns a list of dictionaries that represent the filename and external metadata. The function should have the following inputs:
* `target_path` & `include_nested` have the same argument definition as with the `list_file` function. 
* `include_created_at`: boolean value (should default to `False`) adds the `created_at` key to the dictionary with the creation timestamp of the file.
* `include_file_size`: boolean value (should default to `False`) that adds the `file_size` metadata into the dictionary.


```python=
from typing import Dict, Generator, List


def list_files(target_path: str, include_nested: bool = False) -> Generator:
    pass


def scan_path(
    target_path: str,
    include_nested: bool = False,
    include_created_at: bool = False,
    include_file_size: bool = False,
) -> List[Dict]:
    pass
```

Complete output:

```json 
{
    "file_path": "xxxx",
    "file_name": "xxxx"
    "file_created_at": "xxxx",
    "file_size": "xxxx",
}
```
* The `file_created_at` key should not be included when the `include_created_at` argument is set to `False` (default).
* The `file_size` key should not be included when the `include_file_size` argument is set to `False` (default).

Considerations:
* Use the `list_files` function in the `scan_path` implementation.
* **Hint 1**: Consider the following standard library functions to get the results of listing the target directory:
    * [os.walk](https://docs.python.org/3/library/os.html#os.walk)
    * [os.listdir](https://docs.python.org/3/library/os.html#os.listdir)
* **Hint 2**: Consider the following standard library function to get the creation timestamp of a file [os.path.getctime](https://docs.python.org/3/library/os.path.html#os.path.getctime).
* **Hint 3**: Consider the following standard library function to get the file size [os.path.getsize](https://docs.python.org/3/library/os.path.html#os.path.getsize).

## Python Application (0.1.0)

Create an executable python application capable of scanning a given `target_path` in the filesystem
and saving the results in a csv file.

Execution example:

```commandline
python -m scanner run --target_path <path> --output scan.csv
```

Optional arguments (default value should be `False`):
* `exclude_nested`
* `include_file_created_at`
* `include_file_size`

Your implementation must place the `list_files` and `scan_path` functions in a `utils` module. Moreover,
you should also implement the `cli.py` and all the required infrastructure to
make your executable python application.
