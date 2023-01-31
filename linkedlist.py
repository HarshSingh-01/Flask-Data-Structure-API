class Node:
	def __init__(self, data=None, next=None):
		self.data = data
		self.next = next

class LinkedList:
	def __init__(self,):
		self.head = None
		self.last = None

	def printLL(self):
		node = self.head
		ll = ""
		while node:
			ll += str(node.data) + " -> "
			node = node.next
		
		ll += "None"
		print(ll)

	def insert_at_beg(self, data):
		if self.head is None:
			self.head =  Node(data, None)
			self.last = self.head
			return

		self.head = Node(data, self.head)

	def insert_at_end(self, data):
		if self.head is None:
			self.insert_at_beg(data)
			return
		
		self.last.next = Node(data, None)
		self.last = self.last.next
	
	def to_list(self):
		array = []
		node = self.head
		while node:
			array.append(node.data)
			node = node.next
		
		return array
	
	def get_user_by_id(self, user_id):
		node = self.head
		while node:
			if node.data["id"] is int(user_id):
				return node.data
			node = node.next
		
		return None


	


	