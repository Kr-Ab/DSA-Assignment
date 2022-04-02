
class PatientRecord:
    Pid = 0

    def __init__(self):
        self.PatId = ""
        self.name = ""
        self.age = 0
        self.left = None
        self.right = None
        self.parent = None
        self.prevTail = None

    def registerPatient(self, name, age):
        self.PatId = str(PatientRecord.Pid).rjust(
            4, '0') + str(age).rjust(2, '0')
        self.name = name
        self.age = age
        self.left = None
        self.right = None
        self.parent = None
        self.prevTail = None
        PatientRecord.Pid = PatientRecord.Pid + 1


class TestingQueue:

    def __init__(self):
        self.root = None
        self.tail = None
        self.size = 0

    def nextPatient(self):  # returns the root
        return self.root

    def enqueuePatient(self, node):  # insert a node in the heap
        if(self.root is None):
            self.root = node
            self.tail = self.root
        elif(self.tail.left is None):
            self.tail.left = node
            self.tail.left.parent = self.tail
            self.maxHeapify(self.tail.left)
        else:
            self.tail.right = node
            self.tail.right.parent = self.tail
            self.maxHeapify(self.tail.right)
            prevTail = self.tail
            self.setTail(self.tail)
            self.tail.prevTail = prevTail
        self.size = self.size + 1

    def _dequeuePatient(self):  # removes the root from heap but doesnt return anything
        if self.root is None:
            return
        if self.tail.right:
            self.swapNodeData(self.tail.right, self.root)
            self.tail.right = None
            self.revMaxHeapify(self.root)
        elif self.tail.left:
            self.swapNodeData(self.tail.left, self.root)
            self.tail.left = None
            self.revMaxHeapify(self.root)
        else:
            if self.tail is self.root:
                self.tail = None
                self.root = None
            else:
                self.tail = self.tail.prevTail
                self._dequeuePatient()
                self.size = self.size + 1
        self.size = self.size - 1

    def setTail(self, node):  # helper
        if(node.parent is None):
            self.tail = node
            while(self.tail.left):
                self.tail = self.tail.left

        elif(node.parent.left is node):
            self.tail = node.parent.right
            while(self.tail.left):
                self.tail = self.tail.left

        elif(node.parent.right is node):
            self.setTail(node.parent)

    def revMaxHeapify(self, node):  # helper
        if (node is None or node.left is None):
            return
        max = node.left
        if (node.right):
            if (max.age < node.right.age or (max.age == node.right.age and int(max.PatId) > int(node.right.PatId))):
                max = node.right
        if(max.age > node.age or (max.age == node.age and int(max.PatId) < int(node.PatId))):
            self.swapNodeData(node, max)
            self.revMaxHeapify(max)

    def swapNodeData(self, a, b):  # helper
        a.PatId, b.PatId = b.PatId, a.PatId
        a.name, b.name = b.name, a.name
        a.age, b.age = b.age, a.age

    def maxHeapify(self, node):  # helper
        if(node.parent):
            if(node.parent.age < node.age or (node.parent.age == node.age and int(node.parent.PatId) > int(node.PatId))):
                self.swapNodeData(node.parent, node)
                self.maxHeapify(node.parent)


# run with "python TokenNumber.py" command in PWD

if __name__ == '__main__':

    testingQueue = TestingQueue()
    pid_init = 0

    try:
        with open("inputPS1a.txt", 'r') as input:
            for line in input:
                name, age = line.strip().split(', ')
                patient = PatientRecord()
                patient.registerPatient(name, age)
                testingQueue.enqueuePatient(patient)
                pid_init = pid_init + 1
        while (True):
            node = testingQueue.nextPatient()
            if(node is not None):
                print(node.PatId, node.name)
                testingQueue._dequeuePatient()
            else:
                break
    except Exception as e:
        print("Error", e)
