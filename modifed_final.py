#!/usr/bin/python


import sys, getopt
import copy
import utils
import rwfm


''' gloable variable '''
''' ends '''



def isAssociated(obj,associatedObj):
	if obj in associatedObj:
		return True
	else: 
		False
def merge_two_dicts(x, y):
	'''Given two dicts, merge them into a new dict as a deep copy.'''
	z = copy.deepcopy(x)
	zz= copy.deepcopy(y)
	z.update(zz)
	return z

def storeState(state,stateCMD,cmd,subjects,objects):
	stateCMD.append(cmd)
	state.append(merge_two_dicts(subjects,objects))

def storeFullState(f_state,f_state_CMD,cmd,subjects,objects):
	f_state_CMD.append(cmd)
	#initialize f_state
	if "subjects" not in f_state:
		f_state["subjects"]=[]
	if "objects" not in f_state:
		f_state["objects"]=[]

	f_state["subjects"].append(copy.deepcopy(subjects))
	f_state["objects"].append(copy.deepcopy(objects))


def print_full_state(f_state,f_state_CMD):

	print "Full state of protocol"

	for cmd, sub, obj in zip(f_state_CMD,f_state["subjects"],f_state["objects"]):
		print cmd.center(80)
		print "subjects =>"
		for k in sub:
			print k.rjust(20), "",str(sub[k]["owner"]).ljust(10),"",str(sub[k]["readers"]).ljust(25),"",sub[k]["writers"]
		for k in obj:
			print k.rjust(20), "",str(obj[k]["owner"]).ljust(10),"",str(obj[k]["readers"]).ljust(25),"",obj[k]["writers"]

# def get_diff_state(s1,s2):

# 	sub1 = s1[1]
# 	sub2 = s2[1]

# 	obj1 = copy.deepcopy(s1[2])
# 	obj2 = copy.deepcopy(s2[2])

# 	sub3 = {}
# 	obj3 = {}
# 	# set difference of obj2 - obj1 new object
# 	mod_o_list=list(set(obj2.keys()) - set(obj1.keys()))
# 	for k in mod_o_list:
# 		obj3[k]=obj2[k]
# 		del obj2[k]

# 	if len(obj1) == len(obj2):

def printCurrentState(state,stateCMD,principal): 

	#for s, c in zip(state,stateCMD):
	s= state[-1]
	c= stateCMD[-1]
	print "\n Current State "
	#print "--------------------------------------------------------------------------------"
	#print "!".center(80)
	#print "!".center(80)
	print str(c).center(80)
	#print "!".center(80)
	#print "V".center(80)
	
	#print "--------------------------------------------------------------------------------"
	print ""
	c=0
	for k in principal:
		if c>=len(s):
			break;
		else:
			c+=1
		print k.rjust(20), "",str(s[k]["owner"]).ljust(10),"",str(s[k]["readers"]).ljust(25),"",s[k]["writers"]
	print "\n"
#			print k.rjust(20), "owner : ",str(s[k]["owner"]).ljust(10),"readers : ",str(s[k]["readers"]).ljust(len(subject)*8),"writers :",s[k]["writers"]


def printState(state,stateCMD,principal): 

	for s, c in zip(state,stateCMD):
		print ""
		#print "--------------------------------------------------------------------------------"
		#print "!".center(80)
		#print "!".center(80)
		print str(c).center(80)
		#print "!".center(80)
		#print "V".center(80)
		
		#print "--------------------------------------------------------------------------------"
		print ""
		c=0
		for k in principal:
			if c>=len(s):
				break;
			else:
				c+=1
			print k.rjust(20), "",str(s[k]["owner"]).ljust(10),"",str(s[k]["readers"]).ljust(25),"",s[k]["writers"]

#			print k.rjust(20), "owner : ",str(s[k]["owner"]).ljust(10),"readers : ",str(s[k]["readers"]).ljust(len(subject)*8),"writers :",s[k]["writers"]

def addPrincipal(principal,p):
	principal.append(p)


def loadProtocol(p_spdl):
	clean_lines = []
	with open(p_spdl, "r") as f:
		for line in f:
			cleanedLine = line.strip()
			if cleanedLine: # is not empty
				if cleanedLine[0]!='#':
					clean_lines.append(cleanedLine)
	return clean_lines

## initialize the subjects with subject in a line 
def initSubject(subjects,strings):
	#strings= line.split()
	#Initialize subject label '''
	for s in strings:
		#addPrincipal(principal,s)
		temp={"owner":[s],"readers": strings,"writers":[s]}
		subjects.update({s:temp})

def updateObjects(objects,obj_list,temp_label):
	for ob in obj_list:
		objects[ob]=copy.deepcopy(temp_label)


def store_change(current_change,cmd,c_list):
	if "cmd" not in current_change:
		current_change["cmd"] = []
	if "principal" not in current_change:
		current_change["principal"]= []

	current_change["cmd"].append(cmd)
	current_change["principal"].append(c_list)

def show_change_cmd_state(current_change):

	for cmd, principal in zip(current_change["cmd"],current_change["principal"]):
		print cmd, " ::  changed principal :: => :: ", principal


def spdlToIFD(file_spdl):

	''' Variables to be used '''
	principal=[]
	subjects={}
	objects={}
	stateCMD=[]
	state=[]
	#for full state
	f_state={}
	f_state_CMD=[]
	# added
	current_change={}
	associatedObj={}
	
	spdl=loadProtocol(file_spdl)
	i=0 

	'''end'''

	# for each line in spdl 
	while i<len(spdl): 
		l= spdl[i].split()
		# check for subjects 
		if l[0]=="subject":
			i+=1
			l= spdl[i].split()
			
			initSubject(subjects,l)
			for s in l:
				print s +" ##\n "
				addPrincipal(principal,s)
			i+=1
			storeState(state,stateCMD,"Initialize",subjects,objects)
			storeFullState(f_state,f_state_CMD,"Initialize",subjects,objects)
			store_change(current_change,"Initialize",sorted(subjects.keys()))
			#printState(state,stateCMD,principal)
		# laod prev assumptions
		elif l[0] == "prev":
			i+=1 # goto next line
			l=spdl[i].split()
			while l[0]!="verp":
				temp={"owner":[],"readers":[],"writers":[]}
				# in
				if l[0] in objects:
					temp = objects[l[0]] 
				else:
					addPrincipal(principal,l[0])
					objects[l[0]] = temp
				
				if l[1] == "owner":
						(objects[l[0]])["owner"].extend(l[2:])
				elif l[1]== "readers":
						(objects[l[0]])["readers"].extend(l[2:])
				elif l[1]== "writers":
						(objects[l[0]])["writers"].extend(l[2:])
				i+=1
				l=spdl[i].split()
				#print line
			storeState(state,stateCMD,"load Saved Objects",subjects,objects)
			storeFullState(f_state,f_state_CMD,"load Saved Objects",subjects,objects)
			store_change(current_change,"Initialize",sorted(objects.keys()))
		# now protocol begins
		
		else:
			tokens=spdl[i].split()
			if tokens[0]=="let":
				i+=2
			#	lethandler=spdl.next()
			#	lethandler=spdl.next()
			# tokens <sub, oper, object>
		
			elif tokens[1]=="create":
				# get subject label and object id 
				sublabel=subjects[tokens[0]]
				obj_list=[]
				if len(tokens)>3 and tokens[3]==":=":
					obj_list.append(tokens[2])
					associatedObj[tokens[2]]=tokens[5:-1]
				#	print "\n",tokens[2],associatedObj[tokens[2]]
				else:
					obj_list=tokens[2:]
				for p in obj_list:
					addPrincipal(principal,p)
				temp_label=rwfm.createObjLabel(sublabel)
				
				# put all object with labels in object dictornary
				updateObjects(objects,obj_list,temp_label)

				# Save state
				storeState(state,stateCMD,spdl[i],subjects,objects)
				storeFullState(f_state,f_state_CMD,spdl[i],subjects,objects)
				store_change(current_change,spdl[i],obj_list)
			elif tokens[1]=="read":
				#print "\n inside read"
				sublabel=copy.deepcopy(subjects[tokens[0]])
				objlabel=copy.deepcopy(objects[tokens[2]])
				
				#print sublabel,"\n",objlabel,"\n\n"
				result = rwfm.checkRead(sublabel,objlabel)
				if result["bool"]==True :
					#print "-->Inside result ",result["sublabel"]
					#print "\n"
					subjects[tokens[0]]=result["sublabel"]
					print "read done!  subject label Updated:",tokens[0]," ",subjects[tokens[0]]
					# if tokens[2] == "d":
					# 	printState()
					storeState(state,stateCMD,spdl[i],subjects,objects)
					storeFullState(f_state,f_state_CMD,spdl[i],subjects,objects)
					store_change(current_change,spdl[i],[tokens[0]])
					# printState()
					# if tokens[2] == "d":
					# 	printState(state,stateCMD,principal)
				else:
					#need check for handling the read problem
					#printState(state,stateCMD,principal)
					print "READ DENY on CMD :"+ spdl[i] , objlabel, tokens[0]
					exit();

			elif tokens[1]=="write":
				sublabel=subjects[tokens[0]]
				objlabel=objects[tokens[2]]

				result= rwfm.checkWrite(sublabel,objlabel)

				if result== True:
					print "write done!"
					storeState(state,stateCMD,spdl[i],subjects,objects)
					storeFullState(f_state,f_state_CMD,spdl[i],subjects,objects)
				else:
					print "WRITE DENY on CMD :"+ spdl[i]
					exit()
			elif tokens[1]=="send": 
				#WebKDC send confr-page to UA
				sub = tokens[4]
				sublabel=subjects[tokens[0]]
				objlabel=objects[tokens[2]]
				senttosub=subjects[tokens[4]]

				#print "\nFLAG: ",spdl[i], tokens[2], objlabel, sub 
				if set([sub]).issubset(set(objlabel["readers"])) :
					print "Sent done!"
				else:
					objtemp1=copy.deepcopy(objlabel)
					objtemp1["readers"].append(sub)
					if rwfm.checkDowngrade (sublabel,objlabel,objtemp1) :
						print "Downgraded Object :"+ tokens[2], objlabel, sub 
						# check for associated object ":=" token 
						downgrade_list =[]
						objects[tokens[2]]=objtemp1
						downgrade_list.append(tokens[2])

						if isAssociated( tokens[2],associatedObj) :
							dependedObj= associatedObj[tokens[2]]
							for objt1 in dependedObj:
								objects[objt1]=copy.deepcopy(objtemp1)
								downgrade_list.append(objt1)

						obj_d_msg=tokens[0]+" "+ " Downgrades "+tokens[2]
						

						storeState(state,stateCMD,obj_d_msg,subjects,objects)
						storeFullState(f_state,f_state_CMD,obj_d_msg,subjects,objects)
						store_change(current_change,obj_d_msg,downgrade_list)
						print "Downgrade Done! "
						
					else:
						#printState()
						print "Downgrading Fail! on cmd: " +spdl[i]
						exit()
			elif tokens[1]=="receive":
				print "receive"
			else :
				print "UnKnown Command "+ spdl[i]
		i+=1
	show_change_cmd_state(current_change)
	#printState(state,stateCMD,principal)

	# print "\nFINAL STATE OF subject\n"

	# print '\n'.join('{} \t {} )'.format(key, val) for key, val in sorted(subject.items()))

	# print "\nFINAL STATE OF objects\n"

	# print '\n'.join('{} \t {} '.format(key, val) for key, val in sorted(objects.items()))

	print "\n Protocol IFD conversion successfull!!!" 
	return principal,state,stateCMD,subjects,objects,f_state,f_state_CMD,current_change

'''helping function compliance check '''

def checkLetFormat(tokens,subjects,objects):
	# <object> <compliance> <with> <subject>
	if tokens[0] in objects:
		if tokens[3] in subjects:
			return True
	else:
		return False

def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")

def compliance_check(file_spdl):
	print "#####\n###"
	''' Variables to be used '''
	principal=[]
	subjects={}
	objects={}
	stateCMD=[]
	state=[]
	associatedObj={}
	
	spdl=loadProtocol(file_spdl)
	i=0 

	'''end'''

	# for each line in spdl 
	while i<len(spdl): 
		l= spdl[i].split()
		# check for subjects 
		if l[0]=="subject":
			i+=1
			l= spdl[i].split()
			
			initSubject(subjects,l)
			for s in l:
				print s +" ##\n "
				addPrincipal(principal,s)
			i+=1
			storeState(state,stateCMD,"Initialize",subjects,objects)
			#printState(state,stateCMD,principal)
		# laod prev assumptions
		elif l[0] == "prev":
			i+=1 # goto next line
			l=spdl[i].split()
			while l[0]!="verp":
				temp={"owner":[],"readers":[],"writers":[]}
				# in
				if l[0] in objects:
					temp = objects[l[0]] 
				else:
					addPrincipal(principal,l[0])
					objects[l[0]] = temp
				
				if l[1] == "owner":
						(objects[l[0]])["owner"].extend(l[2:])
				elif l[1]== "readers":
						(objects[l[0]])["readers"].extend(l[2:])
				elif l[1]== "writers":
						(objects[l[0]])["writers"].extend(l[2:])
				i+=1
				l=spdl[i].split()
				#print line
			storeState(state,stateCMD,"load Saved Objects",subjects,objects)
		
		# now protocol begins
		
		else:
			tokens=spdl[i].split()

			if tokens[0]=="let":

				
				'''
				let
					<object> <compliance> <with> <subject>
					login-form READ-SHARED-ONLY with WebKDC
				tel
				
				'''
				i+=1 # next line 
				tokens=spdl[i].split()


				if checkLetFormat(tokens,subjects,objects) == False:
					print "Not in syntex : <object> <compliance> <with> <subject>"
					exit()
				else:
					prevStmtSubject = (stateCMD[-1]).split()[0]
					sublabel=copy.deepcopy(subjects[prevStmtSubject])
					objlabel=copy.deepcopy(objects[tokens[0]])
					'''
					Check for compliance with subject label and object label

					'''
					objName = tokens[0]
					readerslist = tokens[3:]
					tempObjlabel = copy.deepcopy(objlabel)
					tempObjlabel["readers"]=readerslist

					printCurrentState(state,stateCMD,principal)
					print spdl[i],"\n"

					if tokens[1]=="READ-SHARED-ONLY":
						
						# IF we consider protocol designer is going to handle the label 
						print "label of ",objName, " = \t", objlabel
						print "Modified label of  ", objName, " = \t",tempObjlabel,"\n\n"
						statement = "\t If you want to make changes to 'object' "+ objName +" ? "  
						## Query with user 
						choice = query_yes_no(statement)
						if(choice == True) :
							if rwfm.checkUpgrade(sublabel,objlabel,tempObjlabel) :
								

								objects[objName]=copy.deepcopy(tempObjlabel)
								if isAssociated( objName,associatedObj) :
									dependedObj= associatedObj[tokens[2]]
									for objt1 in dependedObj:
										objects[objt1]=copy.deepcopy(tempObjlabel)

								print "Object lable Updated!!"
							else:
								printCurrentState(state,stateCMD,principal)
								print "Object : ", objName," label cannot be Modify" 


						else:
							print "Object = %s label not changed!" %objName

					elif tokens[1]=="READ-SHARED":
						print "label of Objects : ",objName, " = ", objlabel
						print "Modified label : ",objName, " = ", tempObjlabel

						if set(tempObjlabel["readers"]).issubset(set(objlabel["readers"])):
							print "compliance satisfied!!!"
						else:
							print "compliance not satisfied with CMD: ",spdl[i]

					else:
						print "Unspacified compliance",tokens[1]," in Command :",line[i]
				
				i+=1
			
			elif tokens[1]=="create":
				# get subject label and object id 
				sublabel=subjects[tokens[0]]
				obj_list=[]
				if len(tokens)>3 and tokens[3]==":=":
					obj_list.append(tokens[2])
					associatedObj[tokens[2]]=tokens[5:-1]
				#	print "\n",tokens[2],associatedObj[tokens[2]]
				else:
					obj_list=tokens[2:]
				for p in obj_list:
					addPrincipal(principal,p)
				temp_label=rwfm.createObjLabel(sublabel)
				
				# put all object with labels in object dictornary
				updateObjects(objects,obj_list,temp_label)

				# Save state
				storeState(state,stateCMD,spdl[i],subjects,objects)

			elif tokens[1]=="read":
				#print "\n inside read"
				sublabel=copy.deepcopy(subjects[tokens[0]])
				objlabel=copy.deepcopy(objects[tokens[2]])
				
				#print sublabel,"\n",objlabel,"\n\n"
				result = rwfm.checkRead(sublabel,objlabel)
				if result["bool"]==True :
					#print "-->Inside result ",result["sublabel"]
					#print "\n"
					subjects[tokens[0]]=result["sublabel"]
					print "read done!  subject label Updated:",tokens[0]," ",subjects[tokens[0]]
					# if tokens[2] == "d":
					# 	printState()
					storeState(state,stateCMD,spdl[i],subjects,objects)
					# printState()
					# if tokens[2] == "d":
					# 	printState(state,stateCMD,principal)
				else:
					#need check for handling the read problem
					#printState(state,stateCMD,principal)
					print "READ DENY on CMD :"+ spdl[i] , objlabel, tokens[0]
					exit();

			elif tokens[1]=="write":
				sublabel=subjects[tokens[0]]
				objlabel=objects[tokens[2]]

				result= rwfm.checkWrite(sublabel,objlabel)

				if result== True:
					print "write done!"
					storeState(state,stateCMD,spdl[i],subjects,objects)
				else:
					print "WRITE DENY on CMD :"+ spdl[i]
					exit()
			elif tokens[1]=="send": 
				#WebKDC send confr-page to UA
				sub = tokens[4]
				sublabel=subjects[tokens[0]]
				objlabel=objects[tokens[2]]
				senttosub=subjects[tokens[4]]

				#print "\nFLAG: ",spdl[i], tokens[2], objlabel, sub 
				if set([sub]).issubset(set(objlabel["readers"])) :
					print "Sent done!"
				else:
					objtemp1=copy.deepcopy(objlabel)
					objtemp1["readers"].append(sub)
					if rwfm.checkDowngrade (sublabel,objlabel,objtemp1) :

						print "Downgraded Object :"+ tokens[2], objlabel, sub 
						
						''' Update the subjects label '''

						# check for associated object ":=" token 
						objects[tokens[2]]=objtemp1
						if isAssociated( tokens[2],associatedObj) :
							dependedObj= associatedObj[tokens[2]]
							for objt1 in dependedObj:
								objects[objt1]=copy.deepcopy(objtemp1)
								obj_d_msg=tokens[0]+" "+ " Downgrades "+tokens[2]
						storeState(state,obj_d_msg,spdl[i],subjects,objects)
						print "Downgrade Done! "
						
					else:
						#printState()
						print "Downgrading Fail! on cmd: " +spdl[i]
						exit()
			elif tokens[1]=="receive":
				print "receive"
			else :
				print "UnKnown Command "+ spdl[i]
		i+=1
	#printState(state,stateCMD,principal)



def generateLatticeForEachState(FullStateIFD,reslattice):

	# principal = FullStateIFD[0]
	# state = FullStateIFD[1]
	# stateCMD = FullStateIFD[2]
	# subjects1 = FullStateIFD[3]
	f_state= FullStateIFD[5]
	f_state_CMD=FullStateIFD[6]
	current_change=FullStateIFD[7]
	#sub_list= sorted(subjects1.keys())


	DirectConnection=reslattice[2]
	labellist = reslattice[3]
	revlabelId=reslattice[4]
	count=0
	for subjects, objects ,cmd, c_cmd, c_principal in zip(f_state["subjects"],f_state["objects"],f_state_CMD,current_change["cmd"],current_change["principal"]):
		
		filename=str(count) +"_"+ cmd
		count=count+1
		# subjects= ifs["subjects"]
		# objects= ifs["objects"]
		# rwfm.createObjectLattice(sub_list,labellist,revlabelId,objects,file_name=filename)
		# rwfm.addObjectctsToLattice(DirectConnection,labellist,revlabelId,objects,file_name=filename)
		# rwfm.createSubjectLattice(sub_list,labellist,revlabelId,subjects,file_name=filename)
		# rwfm.addSubjectsToLattice(DirectConnection,labellist,revlabelId,subjects,file_name=filename)
		if cmd == c_cmd:
			rwfm.create_principal_lattice(labellist,revlabelId,subjects,objects,c_principal,file_name=filename)









def main(filename):
	'''filename is web-auth-1.1  '''
	'''spdl to Ifd convert and 
	return in order principal,state,stateCMD,subjects,objects,f_state,f_state_CMD,current_change'''
	
	FullStateIFD=spdlToIFD(filename[0])
	principal = FullStateIFD[0]
	state=FullStateIFD[1]
	stateCMD=FullStateIFD[2]
	subjects = FullStateIFD[3]
	objects = FullStateIFD[4]
	f_state= FullStateIFD[5]
	f_state_CMD=FullStateIFD[6]
	current_change= FullStateIFD[7]

	print_full_state(f_state,f_state_CMD)
	

	'''compliance checking,  It will pop up and ask for designers concent for canging lables as per the compliance'''
	###compliance_check(filename[0])
	'''put all the objects into lattice, Enumerate lattice structure 
		1. Fetch all subject
		2. Genrate lattice graph
		3. Put objects on the respective lattice labels 
	''' 
	sub_list= FullStateIFD[3].keys()
	''' For testing purpose we are taking 3 subject A B C '''
	# sub_list = [ "A", "B","C"]
	print "subject => ",sub_list
	''' => 1. generate lattice '''
	
	#lattice = rwfm.generateLattice(sub_list) #blanck 2d n+1 * n+1 lists
	
	reslattice=rwfm.generateLatticeStructure(sorted(sub_list))
	DirectConnection=reslattice[2]
	labellist = reslattice[3]
	revlabelId=reslattice[4]
	'''
		return seclevel,mapedID,DirectConnection,labellist,revlabelId
				0			1		2				3			4
		plotlattice(directconnection,mappedID)
		incorporateObjectsIntolattice(objects,lablellist)

	'''
	generateLatticeForEachState(FullStateIFD,reslattice)

	'''
	Genrate Objects lattice structure!
	'''
	##rwfm.createObjectLattice(sub_list,labellist,revlabelId,objects)
	# print "Writing objects to lattice!"
	##rwfm.addObjectctsToLattice(DirectConnection,labellist,revlabelId,objects)
	# print "lattice updated : done!"

	''' Print lattice of last state of spdl'''
	# last_change = current_change["principal"][-1]
	# print last_change
	#rwfm.create_principal_lattice(labellist,revlabelId,subjects,objects,last_change,file_name="last_state")
	#graph = rwfm.generateGraph(lattice)
	# p_list = rwfm.getPowerList(sub_list)
	# p_list=map(list,p_list)
	# for l in p_list:
	# 	print l
	# 	# for v in l:
	# 	# 	print v,






	'''
	#sec_level = rwfm.generateSecLevel(sub_list)
	#power list of principal 
	# p_list = lattice[1]
	# #print p_list
	# objects = copy.deepcopy(FullStateIFD[4])
	# rwfm.putPrincipalInLattice(lattice,objects)
	# rwfm.printLattice(lattice)

	# compliance_check()
	'''
	# put all object in lattice 
if __name__ == "__main__":
	if len(sys.argv[1:])<1 :
		print "Enter Protocol file in arguments!"
		exit()
	main(sys.argv[1:])
