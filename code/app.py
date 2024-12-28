from pprint import pprint
import time

"""
面向用户的操作
1. 制定目标(按照层级年月周日)
2. 修改目标
3. 查看目标
4. 查看日程表

APP的操作
1. 查找用户的目标
    2). 如果是空 让用户设置
    3). 如果有目标 让用户操作
2. 
"""

from schedule import *
from time_struct import TimeStruct
from time_struct import TimeFormat


class App:
    def __init__(self):
        self.generate_targets()
        self.priority_weights = [1, 2, 3, 4]
        self.timeTable = TimeTable()
        self.tasks = self.generate_task()
        self.schedules = self.read_schedule()
        self.generate_schedule_list()

    def __cal_task_time(self):
        self.tasks.sort(key=lambda x: x.priority, reverse=True)
        priority_sum = sum(x.priority for x in self.tasks)
        free_time = self.timeTable.get_free_time()
        all_time = TimeStruct("0:00", "%H%M")
        for task in self.tasks:
            task_time = free_time.mul_for_float(task.priority / priority_sum)
            task.set_time(
                task_time.round
                if task_time.round < TimeStruct("4:00", "%H%M")
                else TimeStruct("4:00", "%H%M")
            )
            # print(task_time.round)
            all_time = all_time + task_time.round
        print("use_time", all_time)

    def generate_schedule_list(self):
        for s in self.schedules:
            self.timeTable.add_schedule(s)
        # print(self.timeTable)
        self.__cal_task_time()
        for t in self.tasks:
            self.timeTable.add_schedule(t)
        self.timeTable.reduce_schedule()
        print(self.timeTable)

    def read_schedule(self):
        schedules = []
        with open(
            "E://Life_systerm//Things//Schedule//schedule.txt", "r", encoding="utf-8"
        ) as f:
            line = f.readline()
            # 2 23:30 24:00 0 睡觉
            while line != None and line != "":
                words = line.split(" ")
                words[-1] = words[-1].strip("\n")
                s = Schedule(
                    type=int(words[0]),
                    s_time=TimeStruct(words[1], TimeFormat.FORMAT_HM),
                    e_time=TimeStruct(words[2], TimeFormat.FORMAT_HM),
                    task=None,
                    des=words[4],
                )
                schedules.append(s)
                line = f.readline()
        # for s in schedules:
        #     print(s)
        return schedules

    def test(self):
        pass

    def generate_task(self):
        tasks = []
        # print(self.targets[-1][0].father.father)
        for target in self.targets[-1]:
            priority = target.priority * self.priority_weights[-1]
            des = target.des
            # print(target.number, target.des, target.priority, self.priority_weights[-1])
            if target.father != None:
                for t, cnt in TargetIterator(target):
                    priority += t.priority * self.priority_weights[3 - cnt]
                    # print(t.number, t.des, t.priority, self.priority_weights[3 - cnt])
                # print("priority = ", priority)
            # 目标到任务的实现
            task = Task(target=target, priority=priority, des=des)
            tasks.append(task)
        # for task in tasks:
        #     print(task.target.number, task.priority, task.des)
        return tasks

    def generate_targets(self) -> list:
        self.targets = []
        self.targets.append(self.read_Target("Year_target.txt"))
        self.targets.append(self.read_Target("Mouth_target.txt"))
        self.targets.append(self.read_Target("Week_target.txt"))
        self.targets.append(self.read_Target("Day_target.txt"))

    def read_Target(self, file_path: str) -> list:
        targets = []
        with open(
            "E://Life_systerm//Things//Target//" + file_path, "r", encoding="utf-8"
        ) as f:
            line = f.readline()
            while line != None and line != "":
                words = line.split(" ")
                words[-1] = words[-1].strip("\n")
                # print(words[0], words[1], words[2], words[3])
                a = Target(
                    number=int(words[0]),
                    father=(
                        None
                        if int(words[2]) == 0
                        else self.targets[-1][int(words[2]) - 1]
                    ),
                    des=words[1],
                    priority=int(words[3]),
                )
                targets.append(a)
                line = f.readline()
        return targets

    def save_Target(self):
        pass

    def set_Target_for_user(self):
        pass

    def modify_Target_for_user(self):
        pass

    def view_Target_for_user(self):
        pass

    def view_Schedule_for_user(self):
        pass


if __name__ == "__main__":
    app = App()
