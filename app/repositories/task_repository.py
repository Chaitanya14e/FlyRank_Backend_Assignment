from abc import ABC, abstractmethod


class TaskRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, task_id):
        pass

    @abstractmethod
    def create(self, title):
        pass

    @abstractmethod
    def update(self, task_id, title, done):
        pass

    @abstractmethod
    def delete(self, task_id):
        pass