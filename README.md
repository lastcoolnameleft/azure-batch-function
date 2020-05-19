# Create an Azure Batch Task from Azure Function

## Requirements

* Azure Batch Pool and Job must already be created
* Fill in config.py with required values
* Start the Azure Function with: `func start`
* Test the function: `curl 'http://localhost:7071/api/HttpExample?name=foo'` 
* Verify the task completed: `az batch task show --job-id <JOB ID FROM config.py> --task-id <TASK ID FROM curl>`
