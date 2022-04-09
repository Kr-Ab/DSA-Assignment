
from copyreg import constructor


class PatientRecord:
    Pid = 0
    # constructor

    def __init__(self):
        self.PatId = ""
        self.name = ""
        self.age = 0
        self.left = None
        self.right = None
        self.parent = None
        self.prevTail = None

    # initialise the values of the patient
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

    # copies the values of one node to another (deepcopy)
    def copyNode(self, node):
        self.PatId = node.PatId
        self.name = node.name
        self.age = node.age


class TestingQueue:

    def __init__(self):
        self.root = None
        self.tail = None
        self.size = 0

    # returns the root
    def nextPatient(self):
        return self.root

    # insert a node in the heap
    def enqueuePatient(self, node):
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

    # removes the root from heap but doesnt return anything
    def _dequeuePatient(self):
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

    # sets and updates the reference of the tail where new node is to be enqueued
    def setTail(self, node):
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

    # bubbles down the smallest root node while dequeing the heap
    def revMaxHeapify(self, node):
        if (node is None or node.left is None):
            return
        max = node.left
        if (node.right):
            if (max.age < node.right.age or (max.age == node.right.age and int(max.PatId) > int(node.right.PatId))):
                max = node.right
        if(max.age > node.age or (max.age == node.age and int(max.PatId) < int(node.PatId))):
            self.swapNodeData(node, max)
            self.revMaxHeapify(max)

    # swaps the values between two nodes
    def swapNodeData(self, a, b):
        a.PatId, b.PatId = b.PatId, a.PatId
        a.name, b.name = b.name, a.name
        a.age, b.age = b.age, a.age

    # heapifies the binary tree and creates max heap
    def maxHeapify(self, node):
        if(node.parent):
            if(node.parent.age < node.age or (node.parent.age == node.age and int(node.parent.PatId) > int(node.PatId))):
                self.swapNodeData(node.parent, node)
                self.maxHeapify(node.parent)


# run with "python TokenNumber.py" command, make sure to be in PWD

# validates the Input for a Patient
def isValidInputPatient(inp):
    if len(inp.split(",")) != 2:
        return "Invalid Input "
    n, a = inp.split(",")
    if not all(x.isalpha() or x == " " for x in n):
        return "Enter proper name "
    if not(a.strip().isnumeric() and int(a) <= 99 and int(a) > 0):
        return "Enter Valid Age "
    return True

# validates the Input for a New Patient


def isValidInputnewPatient(inp):
    if len(inp.split(":")) != 2:
        return "Invalid Input "
    newPat = inp.split(":")[1].strip()
    res = isValidInputPatient(newPat)
    return res

# validates the Input for Next Patient


def isValidInputnextPatient(inp):
    if len(inp.split(":")) != 2:
        return "Invalid Input "
    numofPat = inp.split(":")[1].strip()
    if not(numofPat.strip().isnumeric() and int(numofPat) > 0):
        return "Enter Valid Number of Patients "
    return True


# main function
if __name__ == '__main__':

    h1 = TestingQueue()
    h2 = TestingQueue()

    num_invalid_inputs = 0
    str_invalid_input = []

    try:
        f = open("outputPS1.txt", "w")

        # reading the initial input file 'inputPS1a.txt'
        with open("inputPS1a.txt", 'r') as input:
            for line in input:
                if PatientRecord.Pid <= 9999:
                    # validating the input
                    if(isValidInputPatient(line.strip()) == True):
                        name, age = line.strip().split(',')
                        age = int(age.strip())
                        patient = PatientRecord()
                        patient.registerPatient(name, age)
                        h1.enqueuePatient(patient)

                    else:
                        str_invalid_input.append(line)
                        num_invalid_inputs += 1
                else:
                    f.write("----------------------------- \n")
                    f.write(
                        "-----Maximum Pid Limit Exceeded. Cannot register more Patients-------\n")
                    f.write("----------------------------- \n")
                    break

        f.write("---- registered Patient --------------- \n")
        f.write("No of patients added: "+str(h1.size)+"\n")
        if(h1.size > 0):
            f.write("Refreshed Queue: \n")

        # looping writing the heap to the file
        while (h1.size > 0):
            node = PatientRecord()
            node.copyNode(h1.nextPatient())
            if(node is not None):
                res = str(node.PatId)+", "+str(node.name)+'\n'
                f.write(res)
                h1._dequeuePatient()
                temp = PatientRecord()
                temp.copyNode(node)
                h2.enqueuePatient(temp)
            else:
                break

        if (num_invalid_inputs > 0):
            f.write("--------------------------------- \n")
            f.write(str(num_invalid_inputs)+" Invalid Input \n")
            for each in str_invalid_input:
                f.write(each)
        f.write("----------------------------- \n")
        h1.root = h2.root
        h1.size = h2.size
        h1.tail = h2.tail
        h2.root = h2.tail = None
        h2.size = 0

        maxlimitflag = 0

        # reading the input file 'inputPS1b.txt'
        with open("inputPS1b.txt", 'r') as input:
            for line in input:
                if(line.strip()[:10].lower() == "newpatient"):
                    if PatientRecord.Pid <= 9999:
                        # validating the new Patient
                        validation = isValidInputnewPatient(line.strip())
                        if(validation == True):
                            name, age = line.strip().split(
                                ':')[1].strip().split(",")
                            age = int(age.strip())
                            patient = PatientRecord()
                            patient.registerPatient(name, age)
                            f.write(
                                "---- new Patient entered --------------- \n")
                            f.write("Patient Details: "+str(patient.name)+", " +
                                    str(patient.age)+", "+str(patient.PatId)+"\n")
                            f.write("Refreshed Queue: \n")
                            h1.enqueuePatient(patient)
                            while (h1.size > 0):
                                node = PatientRecord()
                                node.copyNode(h1.nextPatient())
                                if(node is not None):
                                    res = str(node.PatId)+", " + \
                                        str(node.name)+'\n'
                                    f.write(res)
                                    h1._dequeuePatient()
                                    temp = PatientRecord()
                                    temp.copyNode(node)
                                    h2.enqueuePatient(temp)
                                else:
                                    break
                            f.write("----------------------------- \n")
                            h1.root = h2.root
                            h1.size = h2.size
                            h1.tail = h2.tail
                            h2.root = h2.tail = None
                            h2.size = 0
                        else:
                            f.write(str(validation)+f": '{line.strip()}' \n")
                            f.write("---------------------------- \n")
                    else:
                        if not maxlimitflag:
                            f.write("----------------------------- \n")
                            f.write(
                                "-----Maximum Pid Limit Exceeded. Cannot register more Patients-------\n")
                            f.write("----------------------------- \n")
                            maxlimitflag = 1
                elif(line.strip()[:11].lower() == "nextpatient"):
                    # validating the Next Patient
                    validation = isValidInputnextPatient(line.strip())
                    if(validation == True):
                        num_of_pat_disp = int(
                            line.strip().split(':')[1].strip())
                        f.write("--------next Patient: " +
                                str(num_of_pat_disp)+"--------------- \n")
                        if(num_of_pat_disp > h1.size):
                            f.write("Only "+str(h1.size) + " patients left \n")
                        for i in range(min(num_of_pat_disp, h1.size)):
                            node = PatientRecord()
                            node.copyNode(h1.nextPatient())
                            if(node is not None):
                                res = "Next Patient for Testing is: " + \
                                    str(node.PatId)+", "+str(node.name)+'\n'
                                f.write(res)
                                h1._dequeuePatient()
                            else:
                                break
                        f.write("----------------------------------------- \n")
                    else:
                        f.write(str(validation)+f": '{line.strip()}' \n")
                        f.write("---------------------------- \n")
                else:
                    f.write(f"Check Input: '{line.strip()}' \n")
                    f.write("---------------------------- \n")

        # closing the file
        f.close()
    except Exception as e:
        print("Error", e)
