class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next
    

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def enqueue(self, data):
        if self.head is None and self.tail is None:
            self.head = self.tail = Node(data, None)
            return
        
        self.tail.next = Node(data, None)
        self.tail = self.tail.next
        return
    
    def dequeue(self):
        if self.head is None:
            return None

        removed = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None

        return removed

    def print_queue(self):
        node = self.head
        while node:
            print(node.data, end=" ")
            node = node.next
        return
    


