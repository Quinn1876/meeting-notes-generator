import requests
from time import sleep

## User Defined file
from config import CLICKUP_API_KEY
## End of User Defined files

## -------------------------------- Start Assignee ---------------
class Assignee:
  def __init__(self, name) -> None:
      self.name = name
      pass
  @classmethod
  def from_response_task_assignee(cls, response_task_assignee):
    return cls(response_task_assignee["username"])


## -------------------------------- Start Tag ---------------
class Tag:
  def __init__(self, name) -> None:
      self.name = name
      pass
  @classmethod
  def from_response_task_tag(cls, response_task_tag):
    return cls(response_task_tag["name"])


## -------------------------------- Start Task ---------------
class Task:
  def __init__(self, task_name, url, status_text, assignees, task_id, parent_id, tags) -> None:
    self.task_name = task_name
    self.url = url
    self.status_text = status_text
    self.assignees = assignees
    self.task_id = task_id
    self.parent_id = parent_id
    self.children = [] # Filled Elsewhere
    self.tags = tags

  @classmethod
  def from_response_task(cls, response_task):
    # print(response_task)
    return cls(response_task["name"],
               response_task["url"],
               response_task["status"]["status"],
               [Assignee.from_response_task_assignee(assignee) for assignee in response_task["assignees"]],
               response_task['id'],
               response_task["parent"],
               [Tag.from_response_task_tag(tag) for tag in response_task["tags"]])

  @property
  def isInProgress(self):
    return self.status_text == "in progress"
  @property
  def isOpen(self):
    return self.status_text == "Open"
  @property
  def isInReview(self):
    return self.status_text == "in code review"

  @property
  def isDesign(self):
    return 'design' in [tag.name for tag in self.tags]


  def __str__(self):
    return f'{", ".join([assignee.name for assignee in self.assignees])} - {self.task_name} ({self.url})'

  def addChild(self, child):
    self.children.append(child)

  def getListOfChildren(self):
    return self.children


## -------------------------------- Start ClickupException ---------------
class ClickUpException(Exception):
  def __init__(self, msg) -> None:
    self.msg = msg


## -------------------------------- Start ClickUp ---------------
class ClickUp:
  '''
  Class ClickUp

  This is an API wrapper for clickup which will be expanded to include more functionality as needed
  '''
  headers = {
    'Authorization': CLICKUP_API_KEY,
    'Content-Type': 'application/json'
  }

  status_codes = {
    'OK': 200,
    'RATE_LIMITED': 429
  }

  @staticmethod
  def formatTasks(response_tasks):
    if (len(response_tasks) == 0):
      return []
    return [Task.from_response_task(task) for task in response_tasks]

  @classmethod
  def getTasks(cls, list_id = None, include_subtasks=True):
    '''
    fn: getTasks
    brief: Gets the tasks for a given list_id. If no list_id is passed, then a default is used
    '''
    DEFAULT_LIST_ID = 71521416 ## Spring 2021

    pageCounter = 0
    res_json = None;
    task_list = [];
    list_id = list_id if list_id is not None else DEFAULT_LIST_ID
    rate_limited = False

    BASE_URL = "https://api.clickup.com/api/v2/list"
    GET_TASKS_QUERY = lambda page = 0 : f'{BASE_URL}/{list_id}/task?page={page}&subtasks={"true" if include_subtasks else "false"}';


    while pageCounter == 0 or len(res_json) == 100 or rate_limited:
      rate_limited = False
      response = requests.get(GET_TASKS_QUERY(page=pageCounter), headers=cls.headers)
      # Error Checking
      if response.status_code == cls.status_codes['RATE_LIMITED']:
        sleep(1)
        rate_limited = True
        continue
      elif response.status_code != cls.status_codes['OK']:
        print('Error Processing:', response.url)
        print('Unknown Status Code Received', response.status_code)
        print(response.text)
        raise ClickUpException(f'Unknown Response Code: {response.status_code}')

      res_json = response.json()
      task_list = [*task_list, *cls.formatTasks(res_json["tasks"])]
      pageCounter += 1

    return task_list




