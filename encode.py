import sys
if sys.version_info[0] == 2:
  import qencode
else:
  import qencode3 as qencode
import conf
import time
import threading
import random
from datetime import datetime


ITERATIONS = 300
SLEEP = 20 #sec
FAILED_JOBS = 'failed.txt'
MAX_PARALLEL_JOBS = 50

class Job(threading.Thread):
    def __init__(self, task, url):
        threading.Thread.__init__(self)
        self.url = url
        self.task = task
        self.original_filename = None
        self.filename = self.get_file_name(url)

    def run(self):
        query = self.get_query(conf.QUERY, source_url)

        self.task.custom_start(query)
        if self.task.error:
            print(self.task.message)
            return
        print("Launched task: " + self.task.task_token)
        self.check_status()

    def get_query(self, query_file_path, source_url):
        try:
            file = open(query_file_path, "r")
            query_json = file.read()
            query_json = self.prepare_query(query_json, source_url=source_url)
        except Exception as e:
            print('get_query: ' + str(e))
            sys.exit(1)
        return query_json

    def get_file_name(self, url):
        file_name = url[url.rfind("/") + 1:]
        self.original_filename = file_name
        random.seed(datetime.now())
        return str(random.randrange(100000, 9999999))

    def prepare_query(self, query_json, **kwargs):
        query_json = query_json \
            .replace('{source_url}', kwargs.get('source_url')) \
            .replace('{filename}', self.filename) \
            .replace('{key}', conf.DESTINATION_KEY) \
            .replace('{secret}', conf.DESTINATION_SECRET) \
            .replace('{endpoint}', conf.DESTINATION_ENDPOINT) \
            .replace('{base_folder}', conf.DESTINATION_BASE_FOLDER)
        return query_json

    def check_status(self):
        for i in range(ITERATIONS):
            if i == ITERATIONS - 1:
                log_failed_job(self.url)
                return

            try:
                status =self.task.status()
            except Exception as error:
                print("Error getting status for job " + self.task.task_token + " from url " + self.url + ": " + error)
                continue

            if status['error']:
                log_failed_job(self.url, status['error_description'])
                return

            elif status['status'] == 'completed':
                print('Finished: ' + self.task.task_token)
                #for video in status['videos']:
                    #print(repr(video))
                    #print(video['url'])
                print('-----')
                return

            else:
                # prev_percent = jobs[task_token]['task'].percent
                # if prev_percent is None or prev_percent != status['percent']:
                print(self.task.task_token + ": " + str(status['percent']) + "%")
                # jobs[task_token]['percent'] = status['percent']

            time.sleep(SLEEP)


def read_input_links(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def log_failed_job(url, message='Error processing job'):
    if sys.version_info[0] == 2:
        url = url.decode('utf-8')
    msg = "%s: %s" % (url, message)
    print(msg)
    if sys.version_info[0] == 2:
        msg = msg.encode('utf-8')
    msg = msg + '\n'
    with open(FAILED_JOBS, "a") as log_file:
        log_file.write(msg)


input_links = read_input_links(conf.INPUT_LINKS)
client = qencode.client(conf.QENCODE_API_KEY, conf.QENCODE_API_SERVER)
if client.error:
    print(client.message)
    sys.exit(1)

def create_task(client):
    task = client.create_task()
    if task.error:
        print(task.message)
        if task.message == 'Token not found':
            print('Getting new token...')
            client = qencode.client(conf.QENCODE_API_KEY, conf.QENCODE_API_SERVER)
            return create_task(client)
    return task, client

for source_url in input_links:
    source_url = source_url.strip()
    print("URL: " + source_url)
    task, client = create_task(client)
    if task.error:
        log_failed_job(source_url, task.message)
        continue

    job = Job(task, source_url)
    job.start()
    time.sleep(1)
    while threading.activeCount() >= MAX_PARALLEL_JOBS + 1:
        print('Active jobs: ' + str(threading.activeCount() - 1))
        if threading.activeCount() >= MAX_PARALLEL_JOBS + 1:
            time.sleep(SLEEP)

while threading.activeCount() > 1:
    time.sleep(SLEEP)
print('Done!')
