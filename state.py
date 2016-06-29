class State:
	def __init__(self):
		self.subjects = {}
		self.objects = {}
		self.from_cmd= ""
		self.to_cmd= ""

	def __init__(self, subjects):
		self.subjects = subjects
		self.objects = {}
		self.from_cmd= "Subjects Initialization"
		self.to_cmd= ""

	def __init__(self, subjects, objects,from_cmd,to_cmd):
		self.subjects = subjects
		self.objects = objects
		self.from_cmd= from_cmd
		self.to_cmd= to_cmd



	def add_subjects(self,subjects):
		self.subjects.update(subjects)

	def add_objects(self,objects):
		self.objects.update(objects)

	def add_from_cmd(self,from_cmd):
		self.from_cmd = from_cmd

	def add_from_cmd(self,to_cmd):
		self.to_cmd = to_cmd

	def add(self,subjects,objects,from_cmd,to_cmd):
		self.subjects.update(subjects)
		self.objects.update(objects)
		self.from_cmd= from_cmd
		self.to_cmd= to_cmd

	def __repr__(self):
		print "|".center(80)
		print str(from_cmd).center(80)
		print "V".center(80)

		for k in sorted(self.subjects.keys()):
			print k.rjust(20), "",str(self.subjects[k]["owner"]).ljust(10),"",str(self.subjects[k]["readers"]).ljust(25),"",self.subjects[k]["writers"]
		for k in sorted(self.objects.keys()):
			print k.rjust(20), "",str(self.objects[k]["owner"]).ljust(10),"",str(self.objects[k]["readers"]).ljust(25),"",self.objects[k]["writers"]



class  ifd:
	""" Store each state of the protocol """
	def __init__(self, ):
		self.states = []
		self.state_no = 0

	def add_state(self,state,from_cmd,to_cmd):
		self.states.append(state)
		self.state_no = self.state_no + 1


	def current_state(self):
		return self.states[-1],self.state_no

	def __repr__(self):
		for state in states:
			print state




class protocol:
	def __init__(self):
		self.name= "New Protocol"
		self.principal = []
		self.state = State()
	def __init__(self,name,subjects):
		self.name= name 
		self.principal = sorted(subjects.keys())
		self.subjects = {}
		self.objects = {}
		self.state = State(subjects)

	def store_protcol():
		print "store protocol"

	
	def show_protocol():
		print "protocol"





