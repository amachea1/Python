import os
import sys
import yaml

DEFAULT_REQUIRED = ['README.md', '.gitignore']
CONFIG_FILE = '.required-files.yml'

if os.path.exists(CONFIG_FILE):
    try:
        config_file = open(CONFIG_FILE)
        config = yaml.safe_load(config_file)
        config_file.close()
    except yaml.YAMLError:
        print('ERROR: .required-files.yml is malformed YAML')
        sys.exit(1)

    if not config or 'required_files' not in config:
        print("ERROR: .required-files.yml must contain a 'required_files' list")
        sys.exit(1)

    required_files = config['required_files']
else:
    required_files = DEFAULT_REQUIRED

present_files = []
missing_files = []
for file in required_files:
    if os.path.exists(file):
        present_files.append(file)
    else:
        missing_files.append(file)

output_file = os.environ.get('GITHUB_OUTPUT')
if output_file:
    out = open(output_file, 'a')
    out.write('required_files=' + ','.join(required_files) + '\n')
    out.write('present_files=' + ','.join(present_files) + '\n')
    out.write('missing_files=' + ','.join(missing_files) + '\n')
    out.close()

if missing_files:
    print('Missing required files:')
    for file in missing_files:
        print('  - ' + file)
    sys.exit(1)