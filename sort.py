from Pyro4 import expose
from os import stat
from heapq import merge

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        nums = self.read_input()
        n = len(nums)
        step = n / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(nums[i*step:i*step+step]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)
    
    @staticmethod
    @expose
    def mymap(arr):
            arr_size = len(arr)
            for _ in range(arr_size):
                for i in range(_ % 2, arr_size - 1, 2):
                    if arr[i + 1] < arr[i]:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
            return arr
 
    @staticmethod
    def myreduce(mapped):
        res = []
        wknum = len(mapped)
        res = mapped[0].value
        for i in range(1, wknum):
            res = list(merge(res, list(mapped[i].value)))
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        
        array = []
        for line in f:
            array.append([int(x) for x in line.split()])
        f.close()

        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        for a in output:
            f.write(str(a) + "\n")
            
        f.close()

