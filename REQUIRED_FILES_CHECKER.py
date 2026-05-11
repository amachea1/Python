import os
import sys

required_files = ['README.md','.gitignore']
missing_files = []

for file in required_files:
    if not os.path.exists(file):
       missing_files.append(file)

if missing_files:
    print('Missing required files:')
    for file in missing_files:
        print(file)
    sys.exit(1)