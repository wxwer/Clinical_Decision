# -*- coding: utf-8 -*-

class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, v):
        self.stack.append(v)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            raise LookupError("stack is empty")

    def is_empty(self):
        return not bool(self.stack)

    def top(self):
        return self.stack[-1]
    def __len__(self):
        return len(self.stack)
    def pushsq(self,sq):
        if(type(sq)==list):
            self.stack.extend(sq)
        else:
            print('输入的不是列表')
            print(sq)
            raise Exception
    def print(self):
        for i in range(len(self.stack)):
            print(self.stack[len(self.stack)-i-1])
