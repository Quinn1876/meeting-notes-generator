from clickup import ClickUp
from google_docs import generate_meeting_notes

def convertTaskListToParentListTree(task_list):
  task_dict = {}
  parent_list = []
  child_list = []
  try:
    for task in task_list:
      task_dict[task.task_id] = task
      if (task.parent_id == None):
        parent_list.append(task)
      else:
        child_list.append(task)

    for task in child_list:
      if (task.parent_id in task_dict.keys()):
        task_dict[task.parent_id].addChild(task)
  except Exception:
    print(task_dict.keys())
    raise Exception
  return parent_list




if __name__=='__main__':
  # spring list is default, second list is for the autodoc project
  in_progress_tasks = [task for task in [*ClickUp.getTasks(), *ClickUp.getTasks(list_id=84232391)] if task.isInProgress and (not task.isDesign)]

  parent_task_list = convertTaskListToParentListTree(in_progress_tasks)
  google_task_list = []

  for task in parent_task_list:
    google_task_list.append(str(task))
    for child in task.getListOfChildren():
      google_task_list.append(f'\t{str(child)}')
  member_list=["Quinn", "Evan", "Joshua", "Hassan", "William", "Zeel", "Suvasan", "Steven", "Muhammad", "Kush", "Jeff Z"]
  slideshow = "https://teamwaterloop.ca"
  generate_meeting_notes("Spring", 2021, member_list, google_task_list, slideshow)

