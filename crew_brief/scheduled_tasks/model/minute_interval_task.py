class MinuteIntervalTask:

    def __init__(
        self,
        task_name,
        script_path,
        working_dir,
        python_path,
        interval_minutes,
        description,
        remove_exists = False,
        run_as_user = None,
    ):
        self.task_name = task_name
        self.script_path = script_path
        self.working_dir = working_dir
        self.python_path = python_path
        self.interval_minutes = interval_minutes
        self.description = description
        self.remove_exists = remove_exists
        self.run_as_user = run_as_user

    def as_dict(self):
        return {
            'task_name': self.task_name,
            'script_path': self.script_path,
            'working_dir': self.working_dir,
            'python_path': self.python_path,
            'interval_minutes': self.interval_minutes,
            'description': self.description,
            'remove_exists': self.remove_exists,
            'run_as_user': self.run_as_user,
        }
