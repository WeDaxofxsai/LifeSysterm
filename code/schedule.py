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
from time_struct import *
from functools import singledispatch


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
        print(self.des, self.father.des)
        return self.father

    def __str__(self):
        return "number:{}, type:{}, father:{}, des:{}, priority:{}".format(
            self.number, self.type, self.father, self.des, self.priority
        )

    def get_type(self):
        return self.type

    def get_father(self):
        return self.father

    def get_des(self):
        return self.des


class TargetIterator:
    def __init__(self, target: Target):
        self.target = target
        self.cnt = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.target.father == None:
            raise StopIteration
        self.target = self.target.father
        self.cnt += 1
        return self.target, self.cnt


class Task:
    def __init__(self, target: Target, type=None, des: str = "", priority: int = 0):
        self.target = target
        self.type = type
        self.des = des
        self.priority = priority
        self.use_time = TimeStruct("0:00", TimeFormat.FORMAT_HM)

    def get_target(self):
        return self.target

    def get_type(self):
        return self.type

    def get_des(self):
        return self.des

    def set_time(self, use_time: TimeStruct):
        self.use_time = use_time

    def use_time(self):
        return self.use_time


class TYPE_INCIDENT(Enum):
    INS_TYPE_NONE = 0
    INS_TYPE_FREE = 1
    INS_TYPE_ARRANGED = 2
    INS_REST_BOMB = 3


class Schedule:
    def __init__(
        self,
        type: TYPE_INCIDENT,
        s_time: TimeStruct = None,
        e_time: TimeStruct = None,
        task: Task = None,
        des: str = "",
    ):
        self.type = type
        self.start_time = s_time
        self.end_time = e_time
        self.task = task
        self.des = des

    def use_time(self):
        return self.end_time - self.start_time

    def __str__(self):
        return "type:{}, start_time:{}, end_time:{}, task:{}, des:{}".format(
            TYPE_INCIDENT(self.type),
            self.start_time,
            self.end_time,
            self.task,
            self.des,
        )

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


class TimeTable:
    def __init__(self):
        self.schedule_list = []
        self.schedule_list.append(
            Schedule(TYPE_INCIDENT.INS_TYPE_NONE),
            TimeStruct("0:00", TimeFormat.FORMAT_HM),
            TimeStruct("24:00", TimeFormat.FORMAT_HM),
            None,
            "未分配时间",
        )

    @singledispatch
    def add_schedule(self, obj):
        print("请传入合法类型的参数！")

    @add_schedule.register(Schedule)
    def add_schedule(self, schedule):
        for i in range(len(self.schedule_list)):
            if (
                self.schedule_list[i].type == TYPE_INCIDENT.INS_TYPE_NONE
                and self.schedule_list[i].start_time <= schedule.start_time
                and self.schedule_list[i].end_time >= schedule.end_time
            ):
                self.schedule_list[i].start_time = schedule.end_time
                self.schedule_list(i, schedule)
            elif i == len(self.schedule_list) - 1:
                print("添加失败，时间冲突")

    @add_schedule.register(Task)
    def add_schedule(self, task: Task):
        for i in range(len(self.schedule_list)):
            if (
                self.schedule_list[i].type == TYPE_INCIDENT.INS_TYPE_NONE
                and self.schedule_list[i].use_time() <= task.use_time()
            ):
                schedule = Schedule(
                    type=TYPE_INCIDENT.INS_TYPE_ARRANGED,
                    s_time=self.schedule_list[i].start_time,
                    e_time=self.schedule_list[i].start_time + task.use_time(),
                    task=task,
                    des=task.get_des(),
                )
                self.schedule_list[i].start_time = (
                    schedule_list[i].start_time + task.use_time()
                )
                self.schedule_list(i, schedule)
            elif i == len(self.schedule_list) - 1:
                print("添加失败，时间冲突")


if __name__ == "__main__":
    # 创建一个时间表
    pass
