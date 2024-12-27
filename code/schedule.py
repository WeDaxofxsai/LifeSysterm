"""
人生系统，将我的整个日程进行抽象。首先是划分几种类别的时间
    公务时间
    娱乐时间
    学习时间
    休息时间
    其他时间
分为这几个时间段后，将这些事件填进日程中。事件也被分类
    公务事件
    娱乐事件
    学习事件
    休息事件
"""

from enum import Enum


class TYPE_INCIDENT(Enum):
    INS_TYPE_NONE = 0
    INS_TYPE_FREE = 1
    INS_TYPE_ARRANGED = 2
    INS_REST_BOMB = 3


class Target:
    def __init__(
        self,
        number: int = 0,
        type=None,
        father=None,
        des: str = "",
        priority: int = 0,
    ):
        self.number = number
        self.type = type
        self.father = father
        self.des = des
        self.priority = priority

    def __iter__(self):
        return self

    def __next__(self):
        if self.father == None:
            print("This is the root node.")
            return StopIteration
        else:
            return self.father

    def get_type(self):
        return self.type

    def get_father(self):
        return self.father

    def get_des(self):
        return self.des


class Task:
    def __init__(self, target: Target, type: None, des: str = "", priority: int = 0):
        self.target = target
        self.type = type
        self.des = des

    def get_target(self):
        return self.target

    def get_type(self):
        return self.type

    def get_des(self):
        return self.des


class Schedule:
    def __init__(
        self, type: TYPE_INCIDENT, s_time: int, e_time: int, task: Task, des: str = ""
    ):
        self.type = type
        self.start_time = s_time
        self.end_time = e_time
        self.task = task

    def use_time(self):
        return self.end_time - self.start_time

    def get_type(self):
        return self.type

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_task(self):
        return self.task

    def get_des(self):
        return self.des


if __name__ == "__main__":
    a = Incident(TYPE_INCIDENT.INS_LEARN)
    a.show()
