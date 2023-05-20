import json

pre1 = "\data\luogu\\"

class Luogu:
    def getlastvp(self,people):
        f = open(pre1 + 'lastvp.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]

    def setlastvp(self, people, problem):
        f = open(pre1+'lastvp.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre1+"lastvp.json", 'w')
        f2.write(b)
        f2.close()

    def getlast(self, people):
        f = open(pre1+'last.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]

    def setlast(self, people, problem):
        f = open(pre1+'last.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre1+"last.json", 'w')
        f2.write(b)
        f2.close()

    def addpeople(self, people):
        f = open(pre1+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = "233"
        b = json.dumps(a)
        f2 = open(pre1+"names.json", 'w')
        f2.write(b)
        f2.close()

    def delpeople(self, people):
        f = open(pre1+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        del (a[people])
        b = json.dumps(a)
        f2 = open(pre1+"names.json", 'w')
        f2.write(b)
        f2.close()

    def getall(self):
        f = open(pre1+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        s = set()
        for x in a:
            s.add(x)
        return s

    def setGroup(self, people, group_id):
        f = open(pre1+'group.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = group_id
        b = json.dumps(a)
        f2 = open(pre1+"group.json", 'w')
        f2.write(b)
        f2.close()

    def getGroup(self, people):
        f = open(pre1+'group.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]


Luogu = Luogu()

pre = "\data\codeforces\\"
class Codeforces:
    def getlastvp(self,people):
        f = open(pre + 'lastvp.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]

    def setlastvp(self, people, problem):
        f = open(pre+'lastvp.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre+"lastvp.json", 'w')
        f2.write(b)
        f2.close()

    def getlast(self, people):
        f = open(pre+'last.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]

    def setlast(self, people, problem):
        f = open(pre+'last.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre+"last.json", 'w')
        f2.write(b)
        f2.close()

    def addpeople(self, people):
        f = open(pre+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = "233"
        b = json.dumps(a)
        f2 = open(pre+"names.json", 'w')
        f2.write(b)
        f2.close()

    def delpeople(self, people):
        f = open(pre+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        del (a[people])
        b = json.dumps(a)
        f2 = open(pre+"names.json", 'w')
        f2.write(b)
        f2.close()

    def getall(self):
        f = open(pre+'names.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        s = set()
        for x in a:
            s.add(x)
        return s

    def setGroup(self, people, group_id):
        f = open(pre+'group.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = group_id
        b = json.dumps(a)
        f2 = open(pre+"group.json", 'w')
        f2.write(b)
        f2.close()

    def getGroup(self, people):
        f = open(pre+'group.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        return a[people]


Codeforces = Codeforces()

pre2 = "data\nickname\\"


class names:
    def getname(self, people):
        f = open(pre2 + 'nickname.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        if people in a:
            return a[people]
        return -1

    def setname(self, people, problem):
        f = open(pre2 + 'nickname.json', 'r')
        content = f.read()
        f.close()
        a = json.loads(content)
        a[people] = problem
        b = json.dumps(a)
        f2 = open(pre2 + "nickname.json", 'w')
        f2.write(b)
        f2.close()


names = names()
