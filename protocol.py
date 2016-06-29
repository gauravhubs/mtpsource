import copy
import rwfm
class State:
	# def __init__(self):
	# 	self.subjects = {}
	# 	self.objects = {}
	# 	self.from_cmd= ""
	# 	self.to_cmd= ""

	# def __init__(self, subjects):
	# 	self.subjects = subjects
	# 	self.objects = {}
	# 	self.from_cmd= "Subjects Initialization"
	# 	self.to_cmd= ""

	def __init__(self, subjects, objects,from_cmd,changed_principal="None"):
		self.subjects = copy.deepcopy(subjects)
		self.objects = copy.deepcopy(objects)
		self.from_cmd= from_cmd
		self.state_string= self.string_format_state()
		
		# for lattice genration
		self.sub_list = sorted(subjects.keys())
		res_enum_label = rwfm.getAllLabels(self.sub_list)
		self.labellist = res_enum_label[0]
		self.revlabelId=  res_enum_label[1]
		self.updated_principal=[changed_principal]
		self.lattice_gen()
		#self.to_cmd= to_cmd
	def lattice_gen(self):
		# rwfm.create_principal_lattice(subjects,objects,c_principal,file_name=filename)
		'''
			given  = rwfm.create_principal_lattice(labellist,revlabelId,subjects,objects,c_principal,file_name=filename)
			need changed subject so that it can be highlighted
		'''
		#print "###Indside lattice_gen",self.updated_principal
		if(self.updated_principal[0] == "None"):
			rwfm.create_principal_lattice(self.labellist,self.revlabelId,self.subjects,self.objects,self.sub_list,file_name=self.from_cmd)
		else:
			rwfm.create_principal_lattice(self.labellist,self.revlabelId,self.subjects,self.objects,self.updated_principal,file_name=self.from_cmd)



	def add_subjects(self,subjects):
		self.subjects.update(subjects)

	def add_objects(self,objects):
		self.objects.update(objects)

	def add_from_cmd(self,from_cmd):
		self.from_cmd = from_cmd


	def add(self,subjects,objects,from_cmd,to_cmd):
		self.subjects.update(subjects)
		self.objects.update(objects)
		self.from_cmd= from_cmd
		self.to_cmd= to_cmd

	def __repr__(self):
		# print "|".center(80)
		# print str(self.from_cmd).center(80)
		# print "V".center(80)
		
		sstr = "|".center(80)
		sstr = sstr +"\n"+ str(self.from_cmd).center(80)
		sstr = sstr +"\n"+"V".center(80)

		print sstr
		for k in sorted(self.subjects.keys()):
			#sstr = sstr+ "\n"+ k.rjust(20), "",str(self.subjects[k]["owner"]).ljust(10),"",str(self.subjects[k]["readers"]).ljust(25),"",self.subjects[k]["writers"]
			print k.rjust(20), "",str(self.subjects[k]["owner"]).ljust(10),"",str(self.subjects[k]["readers"]).ljust(25),"",self.subjects[k]["writers"]
		
		for k in sorted(self.objects.keys()):
			#sstr = sstr + "\n"+ k.rjust(20), "",str(self.objects[k]["owner"]).ljust(10),"",str(self.objects[k]["readers"]).ljust(25),"",self.objects[k]["writers"]
			print k.rjust(20), "",str(self.objects[k]["owner"]).ljust(10),"",str(self.objects[k]["readers"]).ljust(25),"",self.objects[k]["writers"]
		return ""
	def string_format_state(self):
		sstr = "|".center(80)
		sstr = sstr +"\n"+ str(self.from_cmd).center(80)
		sstr = sstr +"\n"+"V".center(80)
		for k in sorted(self.subjects.keys()):
			sstr = str(sstr) + "\n"+ str(k.rjust(20)), "",str(self.subjects[k]["owner"]).ljust(10),"",str(self.subjects[k]["readers"]).ljust(25),"",str(self.subjects[k]["writers"])
		for k in sorted(self.objects.keys()):
			sstr = str(sstr) + "\n"+ str(k.rjust(20)), "",str(self.objects[k]["owner"]).ljust(10),"",str(self.objects[k]["readers"]).ljust(25),"",str(self.objects[k]["writers"])
		return str(sstr)
	
	def get_state_string(self):
		return self.state_string


# class  ifd:
# 	""" Store each state of the protocol """
# 	def __init__(self, ):
# 		self.states = []
# 		self.state_no = 0

# 	def add_state(self,state,from_cmd,to_cmd):
# 		self.states.append(state)
# 		self.state_no = self.state_no + 1


# 	def current_state(self):
# 		return self.states[-1],self.state_no

# 	def __repr__(self):
# 		for state in states:
# 			print state




class Protocol:
	def __init__(self,name):
		self.name= name
		self.principal = []
		self.state=[]
		self.current_state = ""
		self.spdl_cmd = []
		self.function = {}
	# def __init__(self,name,subjects):
	# 	self.name= name 
	# 	self.principal = sorted(subjects.keys())
	# 	self.objects = {}
	# 	self.functions = {}
	# 	self.step = [ {"sender": []}, {"recipent": []}, {"message": []}]
	# 	self.state = State(subjects)
	# 	self.ifd = []
	# 	self.spdl=[] 
	# 	self.current_state = self.state
	
	def store_protcol():
		print "store protocol"

	
	def show_protocol():
		print "protocol"

	def add_state(self,state):
		
		self.current_state = state
		self.state.append(self.current_state)

	def add_step(self,step):
		##{"sender": []}, {"recipent": []}, {"message": []} step

		step.append(step)
	def add_functions(self,functions):
		self.function.update(functions)

	def get_ifd(self):
		print "########  IFD  #######"
		for s in self.state:
			if s != None:
				print s
	def save_ifd(self,filename="New_Protocol_IDF"):
		file = open(filename+".ifd", 'w')
		import sys
		orig_sys = sys.stdout
		sys.stdout = file
		print self.name.center(80)
		for s in self.state:
			if s != None:
				print s
		file.close()
		sys.stdout= orig_sys
	def put_spdl_cmd(self,cmd):
		self.spdl_cmd.append(cmd)

	def save_spdl_cmd(self,filename="New_Protocol_SPDL.txt"):
		file = open(filename + "_spdl_cmd.spdl", 'w')
		import sys
		orig_sys = sys.stdout
		sys.stdout = file
		print (self.name + " SPDL").center(80)
		for cmd in self.spdl_cmd:
				print cmd
		file.close()
		sys.stdout= orig_sys

	def lattice_transition(self):
		
		pass

