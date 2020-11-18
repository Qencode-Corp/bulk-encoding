# bulk-encoding
Use this script to launch transcoding jobs for a set of files

## pre-requisites
Install qencode python API client.
See installation instructions
 - for python2: https://github.com/qencode-dev/qencode-api-python-client
 - for python3: https://github.com/qencode-dev/qencode-api-python3-client

## configuration
See descriptions in conf.py

You can change API request JSON to reflect your needs in query.json

## usage
python encode.py

## using different output file naming conventions
Modify code in encode.py - get_file_name()
To use original file names you can use the following code:

def get_file_name(self, url):
    file_name = url[url.rfind("/") + 1:]
    self.original_filename = file_name
    eol = file_name.split('.')
    if len(eol) == 1:
        eol.append('')
    return '.'.join(eol[:-1])


