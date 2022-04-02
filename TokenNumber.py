
from logging import root


class PatientRecord:
    def __init__(self, age, name, Pid):
        self.PatId = str(Pid) + str(age).rjust(2, '0')
        self.name = name
        self.age = age
        self.left = None
        self.right = None
        self.parent = None
        self.prevTail = None


class TestingQueue:
    
    def __init__(self):
        self.root = None
        self.tail = None
        self.size = 0

    def getMaximum(self):
        return self.root.PatId

    def setTail(self, node):
        if(node.parent is None):
            self.tail = node
            while(self.tail.left is not None):
                self.tail = self.tail.left

        elif(node.parent.left is node):
            self.tail = node.parent.right
            while(self.tail.left is not None):
                self.tail = self.tail.left

        elif(node.parent.right is node):
            self.setTail(node.parent)

    def enqueuePatient(self, node:PatientRecord):
        if(self.root is None):  # if tree empty
            self.root = PatientRecord(age, name, Pid)
            self.tail = self.root  # last node is current
        elif(self.tail.left is None):  # if last node left empty
            # set to left node of last node
            self.tail.left = PatientRecord(age, name, Pid)
            self.tail.left.parent = self.tail
            self.maxHeapify(self.tail.left)
        else:
            self.tail.right = PatientRecord(age, name, Pid)
            self.tail.right.parent = self.tail
            self.maxHeapify(self.tail.right)
            prevTail = self.tail
            self.setTail(self.tail)
            self.tail.prevTail = prevTail
        self.size = self.size + 1

    def swapNodeData(self, a, b):
        a.PatId, b.PatId = b.PatId, a.PatId
        a.name, b.name = b.name, a.name
        a.age, b.age = b.age, a.age

    def maxHeapify(self, node):
        if(node.parent is not None):  # if not root
            if(node.parent.age < node.age):  # if current is smaller than parent then swap
                self.swapNodeData(node.parent, node)
                self.maxHeapify(node.parent)





if __name__ == '__main__':

    testingQueue = TestingQueue()
    pid_init = 0

    try:
        with open("inputPS1a.txt", 'r') as input:
            for line in input:
                name, age = line.strip().split(', ')
                testingQueue.enqueuePatient(
                    age, name, str(pid_init).rjust(4, '0'))
                pid_init = pid_init + 1
    except:
        print("Error")

    print(testingQueue.size)
    print(testingQueue.root.PatId)
    print(testingQueue.root.left.PatId)
