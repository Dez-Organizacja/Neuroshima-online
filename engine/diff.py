class Diff:
    def __init__(self):
        self.diffs = {
            "list" : self.diff_list,
            "dict" : self.diff_dict
        }
        self.stack = []

    def print_stack(self):
        print("STACK")
        for message in self.stack[::-1]:
            print(message)
        print("----------------")


    def compare(self, a, b):
        status = self.diff(a, b)
        if(not status):
            print("a:", a)
            print("b:", b)
            self.print_stack()
        return status

    def diff(self, a, b):
        if(type(a) != type(b)):
            self.stack.append(("a:", a))
            self.stack.append(("b:", b))
            self.stack.append("rózne typy")
            return False

        function = self.diffs.get(type(a).__name__, None)
        if(function is None):
            return self.diff_else(a, b)
        else:
            return function(a, b)


    def diff_dict(self, dict1, dict2):
        keys1 = dict1.keys()
        keys2 = dict2.keys()
        if(len(keys1) != len(keys2)):
            self.stack.append("różna długość")
            return False

        for key in keys1:
            if(not key in keys2):
                self.stack.append(("brakuje", key))
                return False
            
            
            if(not self.diff(dict1[key], dict2[key])):
                self.stack.append("-------->")
                self.stack.append(("key", key))
                # self.stack.append(dict2)
                # self.stack.append(dict1)
                return False
        return True

    def diff_else(self, a, b):
        if(a != b):
            self.stack.append(b)
            self.stack.append(a)
        return (a == b)

    def diff_list(self, list1, list2):
        if(len(list1) != len(list2)):
            self.stack.append("różna długość")
            return False
        
        for i in range(len(list1)):
            a = list1[i]
            b = list2[i]
            if(not self.diff(a, b)):
                self.stack.append("-------->")
                self.stack.append(("index", i))
                # self.stack.append(list2)
                # self.stack.append(list1)
                return False

        return True
    

# a = [[1, 3, {'frakcja': 'moloch', 'nazwa': 'szturmowiec', 'rotacja': 0, 'rany': 1}], 
#      [2, 4, {'frakcja': 'borgo', 'nazwa': 'sztab', 'rotacja': 0, 'rany': 3}], 
#      [3, 5, {'frakcja': 'moloch', 'nazwa': 'sztab', 'rotacja': 1, 'rany': 0}]
#      ]

# b = [[1, 3, {'frakcja': 'moloch', 'nazwa': 'szturmowiec', 'rotacja': 0, 'rany': 1}], 
#      [2, 4, {'frakcja': 'borgo', 'nazwa': 'szturmowiec', 'rotacja': 0, 'rany': 3}], 
#      [2, 4, {'frakcja': 'moloch', 'nazwa': 'sztab', 'rotacja': 0, 'rany': 0}]
#      ]

# print(Diff().compare(a, b))