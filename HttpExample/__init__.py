import logging
from . import config

import datetime
import io
import os
import sys
import time
import azure.functions as func
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batch_auth
import uuid

def add_tasks(batch_service_client, job_id, word):
    print('Adding {} tasks to job [{}]...'.format(word, job_id))

    tasks = list()

    command = "/bin/bash -c \"echo {}\"".format(word)
    task_id = 'Task-' + str(uuid.uuid4())
    tasks.append(batch.models.TaskAddParameter(
        id=task_id,
        command_line=command))

    batch_service_client.task.add_collection(job_id, tasks)
    return task_id

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start_time = datetime.datetime.now().replace(microsecond=0)
    print('Sample start: {}'.format(start_time))
    print()

    # Create a Batch service client. We'll now be interacting with the Batch
    # service in addition to Storage
    credentials = batch_auth.SharedKeyCredentials(config._BATCH_ACCOUNT_NAME,
                                                  config._BATCH_ACCOUNT_KEY)

    batch_client = batch.BatchServiceClient(
        credentials,
        batch_url=config._BATCH_ACCOUNT_URL)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        task_id = add_tasks(batch_client, config._JOB_ID, name)
        return func.HttpResponse(f"Task created {task_id}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
