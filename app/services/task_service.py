from app.repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository


    def get_all_tasks(self):

        return self.repository.get_all()


    def get_task(self, task_id):

        return self.repository.get_by_id(task_id)


    def create_task(self, title):

        if not title or title.strip() == "":
            raise ValueError("Title is required")

        return self.repository.create(title.strip())


    def update_task(self, task_id, title, done):

        if not title or title.strip() == "":
            raise ValueError("Title is required")

        return self.repository.update(
            task_id,
            title.strip(),
            done
        )


    def delete_task(self, task_id):

        return self.repository.delete(task_id)