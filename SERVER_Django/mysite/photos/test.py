import os
import sys

print(os.path.realpath(__file__))
print(os.path.dirname(os.path.dirname(__file__)))
print(os.getcwd())
print(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))