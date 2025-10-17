class InMemoryStorage:
    def __init__(self):
        self._projects: Dict[str, Project] = {}
        self._tasks: Dict[str, Task] = {}
        self._project_tasks: Dict[str, List[str]] = {}
        
        # Load limits from environment with defaults
        self.max_projects = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 100))
        self.max_tasks_per_project = int(os.getenv('MAX_NUMBER_OF_TASKS', 1000))
    
    def create_task(self, task: Task) -> None:
        project_tasks = self._project_tasks.get(task.project_id, [])
        if len(project_tasks) >= self.max_tasks_per_project:
            raise LimitExceededError(f"Cannot exceed maximum of {self.max_tasks_per_project} tasks per project")
        
        self._tasks[task.id] = task
        if task.project_id not in self._project_tasks:
            self._project_tasks[task.project_id] = []
        self._project_tasks[task.project_id].append(task.id)
        
    def delete_task(self, task_id: str) -> None:
        if task_id in self._tasks:
            task = self._tasks[task_id]
            if task.project_id in self._project_tasks:
                # Remove task from project's task list
                self._project_tasks[task.project_id] = [
                    tid for tid in self._project_tasks[task.project_id] 
                    if tid != task_id
                ]
            del self._tasks[task_id]