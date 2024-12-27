from pprint import pprint

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


class App:
    def __init__(self):
        self.generate_targets()
        # pprint(self.targets)
        self.priority_weight = {"year": 1, "month": 1, "week": 1, "day": 1}
        self.generate_task()

    def test(self):
        pass

    def generate_task(self):
        tasks = []
        # print(self.targets[-1])
        for target in self.targets[-1]:
            priority = 0
            des = ""
            if target.father != 0:
                priority += target.priority
            else:
                for t in target:
                    priority += t.priority
                    print(t.number, t.father, t.des, t.priority)
            # print(target.number, target.father, target.des, priority)

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
