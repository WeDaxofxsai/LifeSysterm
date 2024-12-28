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
from functools import singledispatchmethod


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

    def __str__(self):
        return "type:{}, des:{}, priority:{}, use_time:{}".format(
            self.type, self.des, self.priority, self.use_time
        )

    def get_target(self):
        return self.target

    def get_type(self):
        return self.type

    def get_des(self):
        return self.des

    def set_time(self, use_time: TimeStruct):
        self.use_time = use_time


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

    @property
    def use_time(self):
        return self.end_time - self.start_time

    def __str__(self):
        return "type:{}, start_time:{}, end_time:{}, task_des:{}".format(
            TYPE_INCIDENT(self.type),
            self.start_time,
            self.end_time,
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
            Schedule(
                TYPE_INCIDENT.INS_TYPE_NONE,
                TimeStruct("0:00", TimeFormat.FORMAT_HM),
                TimeStruct("24:00", TimeFormat.FORMAT_HM),
                None,
                "未分配时间",
            )
        )
        self.remain_time = TimeStruct("24:00", TimeFormat.FORMAT_HM)

    def get_free_time(self):
        return self.remain_time

    def __str__(self):
        return (
            "---------------------------------\n"
            + "TimeTable:\n{}".format(
                "\n".join([str(schedule) for schedule in self.schedule_list])
            )
            + "\nremain_time:{}".format(self.remain_time)
            + "\n---------------------------------"
        )

    def show_schedule(self):
        for i in self.schedule_list:
            print(i)

    @singledispatchmethod
    def add_schedule(self, arg):
        raise NotImplementedError("Cannot negate a")

    @add_schedule.register
    def _(self, schedule: Schedule):
        for i in range(len(self.schedule_list)):
            if (
                self.schedule_list[i].type == TYPE_INCIDENT.INS_TYPE_NONE
                and self.schedule_list[i].start_time <= schedule.start_time
                and self.schedule_list[i].end_time >= schedule.end_time
            ):
                if self.schedule_list[i].start_time < schedule.start_time:
                    stick_schedule = Schedule(
                        TYPE_INCIDENT.INS_TYPE_NONE,
                        self.schedule_list[i].start_time,
                        schedule.start_time,
                        None,
                        "未分配时间",
                    )
                    self.schedule_list.insert(i, stick_schedule)
                    i += 1
                self.schedule_list[i].start_time = schedule.end_time
                self.schedule_list.insert(i, schedule)
                self.remain_time -= schedule.use_time
                # print(self.schedule_list)
                if self.schedule_list[-1].start_time == self.schedule_list[-1].end_time:
                    self.schedule_list.pop()
                return
            elif i == len(self.schedule_list) - 1:
                print("添加失败，时间冲突")

    @add_schedule.register
    def _(self, task: Task):
        for i in range(len(self.schedule_list)):
            if (
                self.schedule_list[i].type == TYPE_INCIDENT.INS_TYPE_NONE
                and task.use_time
                <= self.schedule_list[i].end_time - self.schedule_list[i].start_time
            ):
                stick_schedule = Schedule(
                    TYPE_INCIDENT.INS_TYPE_ARRANGED,
                    self.schedule_list[i].start_time,
                    self.schedule_list[i].start_time + task.use_time,
                    task,
                    task.des,
                )
                self.schedule_list[i].start_time = stick_schedule.end_time
                self.schedule_list.insert(i, stick_schedule)
                i += 1
                if self.schedule_list[i].start_time == self.schedule_list[i].end_time:
                    self.schedule_list.remove(self.schedule_list[i])
                self.remain_time -= task.use_time
                return
            elif i == len(self.schedule_list) - 1:
                print(task, "添加失败，时间冲突")
                print("现在的日程为")
                self.show_schedule()
                # print(self.schedule_list)

    def reduce_schedule(self):
        for i in self.schedule_list:
            if i.type == TYPE_INCIDENT.INS_TYPE_NONE:
                i.type = TYPE_INCIDENT.INS_TYPE_ARRANGED
                i.des = "空闲时间"
        self.remain_time = TimeStruct("0:00", TimeFormat.FORMAT_HM)

    # def add_schedule(self, i: str, j: str):
    #     print("add_task")


if __name__ == "__main__":
    # 创建一个时间表
    a = TimeTable()
    a.add_schedule(22)
