# File, containing urls of input videos, one per line
INPUT_LINKS = './input_links.txt'

# Output settings
# You can specify any storage type here.
# Supported protocols are: ftp, sftp, ftps, s3, b2, aspera
DESTINATION_ENDPOINT = 's3://your-storage-provider.com/bucket'
DESTINATION_BASE_FOLDER = '/some/folder/'
DESTINATION_KEY = 'your-key' #replace this with your key or username
DESTINATION_SECRET = 'your-secret' #replace this with your secret or password

# qencode
QENCODE_API_KEY = 'your-qencode-api-key' #place your project API Key here
QENCODE_API_SERVER = 'https://api.qencode.com/'

#file with API query
QUERY = 'query.json'

DEBUG = True
