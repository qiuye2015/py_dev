import os
import sys

"""
python -m site
"""
print(os.path.basename(__file__), "*" * 10, sys.executable)
print(os.path.basename(__file__), "*" * 10, sys.path)
print(os.path.basename(__file__), "*" * 10, sys.prefix)

import my_package.b


# py3 main.py
# py3 -m my_package.b