"""
Generate a random JWT secret key
"""

import os

print(os.urandom(24).hex())
