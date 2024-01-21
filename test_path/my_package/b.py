import os
import sys

print("I'm b")
print(os.path.basename(__file__), "*" * 10, sys.path)
# import a
from my_package import a
# from . import a
# from . import a 与 from my_package import a 等价

