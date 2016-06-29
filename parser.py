import utils
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def top(self):
         return self.items[-1]

     def size(self):
         return len(self.items)

     def __repr__(self):
         for i in self.items:
             if i :
                 print i 


class Tree:
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)




def parser(token,pos=0):
	#print token
#	print "parser###"
	i = 0
	stack = Stack()
	tree = Tree()
	oper_sq = []
	while i<len(token):
		#print i,"  ",token[i]
		if( token[i] == '(') :
			# either function or touple
			if i==0 or token[i-1]==',' or token[i-1] =='(' : #TUPLE_S 
			#	print token[i]
				stack.push("__TUPLE_S")


		elif(token[i] == ')'):

			t_list=[]
			elm=""
			while not stack.isEmpty() and elm != "__TUPLE_S" and elm !="__FUN_S" :
				
				elm = stack.top()
				stack.pop()
				t_list.append(elm)
				#t_list.reverse()
				#print elm

			# if elm == "__FUN_S":
			# 	print "function name ", t_list," : argu = ", t_list[0:-1]
			# else:
			# 	print "TUPLE_S", t_list
			t_list.reverse()
			oper_sq.append(t_list)
			#print t_list
			stack.push(t_list) 
			# tup = stack.top()
			# if("TUPLE_S" in tup):
			# 	node = create_node(tup)
			# 	insert_into_tree(node)

			# if stack.isEmpty():
			# 	print 
			# 	node = create_node(tup)
			# 	insert_into_tree(node)

			# stack.pop()
			# parser(string,i+1)

		else: # its the message 'create a node'
			if i+1 < len(token):
				if token[i+1] == '(': ## function detected
					stack.push("__FUN_S")
					stack.push(token[i])
					#print token[i]
					i=i+1
				else:
					stack.push(token[i])
			else:
				stack.push(token[i])
		i = i+1

	# print "stack element"
	# while not stack.isEmpty():
	# 	print stack.pop()

	if len(oper_sq) == 0:
		oper_sq.append(stack.top()) # if only one element 

	return oper_sq











def print_list(l):
	print "start"
	for e in l:
		print e
	print "Done!"
def sstrip(s):
		return s.strip()

def get_token(message):
	import re

	#print message
	token = re.split(r'(;|,|\(|\)|\s)\s*', message)
	t =  map(sstrip,token)
	t1=filter(lambda a: a != "", t)
	t2=filter(lambda a: a != ",", t1)
	
	return t2

def get_parsed(message):
	#print "\t".join(token)
	
	#print_list(t2)
	t2  =  get_token(message)
	res = parser(t2)
	#print "Parsing done!"
	return res

def get_steps():
	#show_principal()
	msg1= "Who is the sender ? "
	msg2= "Who is the intended recipient ?"
	msg4 = "Message is :"
	sender = utils.query_name(msg1)
	if(sender == "done"):
		return "done"
	recipient = utils.query_name(msg2)
	message_list=[]
	f_dict= {}
	message = utils.query_name(msg4)
	while "=" in message:
		tok=message.split('=')
		var= tok[0].strip()
		func= tok[1].strip()
		f_dict.update({var: func})
		# final exended token
		s_tized = func

		tmsg = get_token(func)
		#print tmsg
		for t in tmsg:
			#print t
			if t in message_list:
				#print "Found = ", t
				s_tized = s_tized.replace(t,f_dict[t])
		#print s_tized
		f_dict.update({var:s_tized})

		message_list.append(var)
		message = utils.query_name("\nNext line: ")

	# substitue the message with function   
	# final exended token

	tmsg = get_token(message)
	s_tized = message
	#print tmsg
	for t in tmsg:
		#print t
		if t in message_list:
			#print "Found = ", t
			s_tized = s_tized.replace(t,f_dict[t])
	#print s_tized
	#f_dict.update({var:s_tized})
	message = s_tized
	'''
	 Make a step ::= sender to recipient => message
	 send ( sender, recipient, message)
	'''
	step_b = "send ( "+str(sender.upper())+", "+str(recipient.upper())+", "+message+" )"
	# validate(sub_list,sender)
	# validate(sub_list,recipient)
	step = [step_b,sender,recipient,message]
	#print message
	return step


if __name__ == "__main__":
	#step = "message"
	#message = "encr ( (name1, name2), key1)"
	#get_parsed(message)
	get_steps()