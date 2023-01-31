class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class Stack:
    def __init__(self):
        self.top = None
    
    def peek(self):
        return self.top
    
    def push(self, data):
        if self.top is None:
            self.top = Node(data, None)
            return
        self.top = Node(data, self.top)
    
    def pop(self):
        if self.top is None:
            return None
        
        removed = self.top
        self.top = self.top.next

        return removed

    def print_stack(self):
        node = self.top
        while node:
            print(node.data)
            node = node.next
        



