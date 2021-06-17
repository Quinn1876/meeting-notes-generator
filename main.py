from clickup import ClickUp

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
  in_progress_tasks = [task for task in ClickUp.getTasks() if task.isInProgress and (not task.isDesign)]

  parent_task_list = convertTaskListToParentListTree(in_progress_tasks)

  for task in parent_task_list:
    print(str(task))
    for child in task.getListOfChildren():
      print(f'\t{str(child)}')

