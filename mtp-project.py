#!/usr/bin/python


import sys, getopt
import copy
import utils
#Read Protocol form file line by line and create IFD '''

principal=[]
subject={}
objects={}
stateCMD=[]
state=[]
associatedObj={}


def checkRead(sublabel,objectlabel):
	#""" This method call checks if user i.e. the subject can read the object w.r.t IFC."""
	#""" This method returns a dict which has boolean value True or False and changed labels of subject after a successfull read.  Save the subject label after recieving the return value """

	if set(sublabel["owner"]).issubset(set(objectlabel["readers"])):
		newsublabel = changeLabelRead(sublabel,objectlabel)
		return {"bool":True,"sublabel": newsublabel}
	else:
		return {"bool":False,"sublabel": sublabel}

#@classmethod
def changeLabelRead(sublabel,objectlabel):
#""" Returns the Changed label of subject to reflect that it may gain information after 
#reading the object and permit access. """

	newR = list(set(sublabel["readers"]).intersection(set(objectlabel["readers"])))
	newW = list(set(sublabel["writers"]).union(set(objectlabel["writers"])))
	newsubjectlabel = {"owner":sublabel["owner"],"readers": newR,"writers": newW}


	return newsubjectlabel

def checkWrite(sublabel,objectlabel):
#""" This method call checks if user i.e. the subject can write to the object w.r.t IFC."""
#""" This method returns boolean value True or False. No label change is required. """

	temp = set(sublabel["owner"]).issubset(set(objectlabel["writers"])) and set(sublabel["readers"]).issuperset(set(objectlabel["readers"])) and set(sublabel["writers"]).issubset(set(objectlabel["writers"]))                          

	if temp:
		return True
	else:
		return False

def createObjLabel(sublabel,obj_list):
#""" Returns the object label for the new object being created, derived from the subject label. """
#""" obj_id is the object primary key to refer to the object from it's label.
#Pass its pk to this method with the subject label who created it. """

	objectlabel = {"owner": sublabel["owner"], "readers": sublabel["readers"],"writers": sublabel["writers"]}
	for obj_id in obj_list:
		addPrincipal(obj_id)
		objects.update({obj_id:copy.deepcopy(objectlabel)})
	return objectlabel

def checkUpgrade(sublabel,objtemp2,objtemp3):

	if((set(sublabel["owner"]).issubset(set(objtemp2["readers"]))) and (sublabel["owner"]==objtemp2["owner"]==objtemp3["owner"]) and (set(sublabel["readers"]).issubset(set(objtemp2["readers"] ))) and (set(sublabel["writers"])==set(objtemp2["writers"])==set(objtemp3["writers"])) and  (set(objtemp3["readers"]).issubset(set(sublabel["readers"])))):
		return True
	else:
		return False
def checkDowngrade(sublabel,objtemp2,objtemp3):
	if((set(sublabel["owner"]).issubset(set(objtemp2["readers"]))) and (sublabel["owner"]==objtemp2["owner"]==objtemp3["owner"]) and (set(sublabel["readers"])==set(objtemp2["readers"])) and (set(sublabel["writers"])==set(objtemp2["writers"])==set(objtemp3["writers"])) and (set(objtemp2["readers"]).issubset(set(objtemp3["readers"]))) and ((set(sublabel["writers"])==set(sublabel["owner"])) or (set(set(objtemp3["readers"]).difference(set(objtemp2["readers"]))).issubset(set(objtemp2["writers"]))))):
		return True
	else:
		return False

def isAssociated(obj):
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

def storeState(cmd,subject,objects):
	stateCMD.append(cmd)
	state.append(merge_two_dicts(subject,objects))

def printState(): 

	for s, c in zip(state,stateCMD):
		print "\n"
		#print "--------------------------------------------------------------------------------"
		#print "!".center(80)
		#print "!".center(80)
		print str(c).center(80)
		#print "!".center(80)
		#print "V".center(80)
		
		#print "--------------------------------------------------------------------------------"
		c=0
		for k in principal:
			if c>=len(s):
				break;
			else:
				c+=1
			print k.rjust(20), "",str(s[k]["owner"]).ljust(10),"",str(s[k]["readers"]).ljust(len(subject)*8),"",s[k]["writers"]

#			print k.rjust(20), "owner : ",str(s[k]["owner"]).ljust(10),"readers : ",str(s[k]["readers"]).ljust(len(subject)*8),"writers :",s[k]["writers"]

def addPrincipal(p):
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

def initSubject(line):
	strings= line.split()
	#Initialize subject label '''
	for s in strings:
		addPrincipal(s)
		temp={"owner":[s],"readers": strings,"writers":[s]}
		subject.update({s:temp})

#### Protocol SPDL to IFD conversion __main__
def spdlToIFD(file_spdl):
	spdl=loadProtocol(file_spdl)
	i=0 # for each line in spdl 
	while i<len(spdl): 
		l= spdl[i].split()
		# check for subjects 
		if l[0]=="subject":
			i+=1
			l= spdl[i]
			initSubject(l)
			i+=1
			storeState("Initialize",subject,objects)
			printState();
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
					addPrincipal(l[0])
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
			storeState("load Saved Objects",subject,objects)
		# 	for k in cur:
		# 		print k, cur[k]
		# # now protocol begins
		else:
			tokens=spdl[i].split()
			if tokens[0]=="let":
				i+=2
			#	lethandler=spdl.next()
			#	lethandler=spdl.next()
			# tokens <sub, oper, object>
			elif tokens[1]=="create":
				# get subject label and object id 
				sublabel=subject[tokens[0]]
				obj_list=[]
				if len(tokens)>3 and tokens[3]==":=":
					obj_list.append(tokens[2])
					associatedObj[tokens[2]]=tokens[5:-1]
				#	print "\n",tokens[2],associatedObj[tokens[2]]
				else:
					obj_list=tokens[2:]

				temp_label=createObjLabel(sublabel,obj_list)
				storeState(spdl[i],subject,objects)

			elif tokens[1]=="read":
				#print "\n inside read"
				sublabel=copy.deepcopy(subject[tokens[0]])
				objlabel=copy.deepcopy(objects[tokens[2]])
				
				print sublabel,"\n",objlabel,"\n\n"
				result = checkRead(sublabel,objlabel)
				if result["bool"]==True :
					#print "-->Inside result ",result["sublabel"]
					#print "\n"
					subject[tokens[0]]=result["sublabel"]
					print "read done changed:",subject[tokens[0]]
					# if tokens[2] == "d":
					# 	printState()
					storeState(spdl[i],subject,objects)
					# printState()
					if tokens[2] == "d":
						printState()
				else:
					#need check for handling the read problem
					printState()
					print "READ DENY on CMD :"+ spdl[i] , objlabel, tokens[0]
					exit();

			elif tokens[1]=="write":
				sublabel=subject[tokens[0]]
				objlabel=objects[tokens[2]]

				result= checkWrite(sublabel,objlabel)

				if result== True:
					print "write done!"
					storeState(spdl[i],subject,objects)
				else:
					print "WRITE DENY on CMD :"+ spdl[i]
					exit()
			elif tokens[1]=="send": 
				#WebKDC send confr-page to UA
				sub = tokens[4]
				sublabel=subject[tokens[0]]
				objlabel=objects[tokens[2]]
				senttosub=subject[tokens[4]]

				#print "\nFLAG: ",spdl[i], tokens[2], objlabel, sub 
				if set([sub]).issubset(set(objlabel["readers"])) :
					print "Sent done!"
				else:
					objtemp1=copy.deepcopy(objlabel)
					objtemp1["readers"].append(sub)
					if checkDowngrade (sublabel,objlabel,objtemp1) :
						print "Downgraded Object :"+ tokens[2], objlabel, sub 
						# check for associated object ":=" token 
						objects[tokens[2]]=objtemp1
						if isAssociated( tokens[2] ) :
							dependedObj= associatedObj[tokens[2]]
							for objt1 in dependedObj:
								objects[objt1]=copy.deepcopy(objtemp1)
						storeState(spdl[i],subject,objects)
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
	printState()

	# print "\nFINAL STATE OF subject\n"

	# print '\n'.join('{} \t {} )'.format(key, val) for key, val in sorted(subject.items()))

	# print "\nFINAL STATE OF objects\n"

	# print '\n'.join('{} \t {} '.format(key, val) for key, val in sorted(objects.items()))

	print "Protocol IFD conversion successfull!!!" 

# second pass on IFD compliance checking 
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

def checkLetFormat(tokens):
	# <object> <compliance> <with> <subject>
	if tokens[0] in objects:
		if tokens[3] in subject:
			return True
	else:
		return False
principal=[]
subject={}
objects={}
stateCMD=[]
state=[]
associatedObj={}
def compliance_check(file_spdl):
	print "\n compliance check\n\n"
	print "--------------"
	
	spdl=loadProtocol(file_spdl)
	#printState()
	i=0 # for each line in spdl 
	while i<len(spdl): 
		print spdl[i]
		l= spdl[i].split()
		# check for subjects 
		if l[0]=="subject":
			i+=1
			l= spdl[i]
			initSubject(l)
			i+=1
			storeState("Initialize",subject,objects)
			#printState();
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
					addPrincipal(l[0])
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
			storeState("load Saved Objects",subject,objects)
		# 	for k in cur:
		# 		print k, cur[k]
		# # now protocol begins
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
				if checkLetFormat(tokens) == False:
					print "Not in syntex : <object> <compliance> <with> <subject>"
					exit()
				else:
					sublabel=copy.deepcopy(subject[tokens[3]])
					objlabel=copy.deepcopy(objects[tokens[0]])
					'''
					Check for compliance with subject label and object label

					'''
					objName = tokens[0]
					readerslist = tokens[3:]
					tempObjlabel = copy.deepcopy(objects[objName])
					tempObjlabel["readers"]=readerslist

					if tokens[1]=="READ-SHARED-ONLY":
						
						# IF we consider protocol designer is going to handle the label 
						print "label of Objects : ", objlabel
						print "Modified label : ", tempObjlabel
						statement = "If you want to make changes?"
						## Query with user 
						choice = query_yes_no(statement)
						if(choice == True) :
							objects[objName]=tempObjlabel

						else:
							print "Object label not updated"

					elif tokens[1]=="READ-SHARED":
						print "label of Objects : ", objlabel
						print "Modified label : ", tempObjlabel

						if set(tempObjlabel).issubset(set(objlabel["readers"])):
							print "compliance satisfied!!!"
						else:
							print "compliance not satisfied with CMD: ",spdl[i]

					else:
						print "Unspacified compliance",tokens[1]," in Command :",line[i]
				
				i+=1
			elif tokens[1]=="create":
				# get subject label and object id
				print subject 
				sublabel=subject[tokens[0]]
				obj_list=[]
				if len(tokens)>3 and tokens[3]==":=":
					obj_list.append(tokens[2])
					associatedObj[tokens[2]]=tokens[5:-1]
				#	print "\n",tokens[2],associatedObj[tokens[2]]
				else:
					obj_list=tokens[2:]

				temp_label=createObjLabel(sublabel,obj_list)
				storeState(spdl[i],subject,objects)

			elif tokens[1]=="read":
				#print "\n inside read"
				sublabel=copy.deepcopy(subject[tokens[0]])
				objlabel=copy.deepcopy(objects[tokens[2]])
				
				print sublabel,"\n",objlabel,"\n\n"
				result = checkRead(sublabel,objlabel)
				if result["bool"]==True :
					#print "-->Inside result ",result["sublabel"]
					#print "\n"
					subject[tokens[0]]=result["sublabel"]
					print "read done changed:",subject[tokens[0]]
					# if tokens[2] == "d":
					# 	printState()
					storeState(spdl[i],subject,objects)
					# printState()
					if tokens[2] == "d":
						printState()
				else:
					#need check for handling the read problem
					printState()
					print "READ DENY on CMD :"+ spdl[i] , objlabel, tokens[0]
					exit();

			elif tokens[1]=="write":
				sublabel=subject[tokens[0]]
				objlabel=objects[tokens[2]]

				result= checkWrite(sublabel,objlabel)

				if result== True:
					print "write done!"
					storeState(spdl[i],subject,objects)
				else:
					print "WRITE DENY on CMD :"+ spdl[i]
					exit()
			elif tokens[1]=="send": 
				#WebKDC send confr-page to UA
				sub = tokens[4]
				sublabel=subject[tokens[0]]
				objlabel=objects[tokens[2]]
				senttosub=subject[tokens[4]]

				#print "\nFLAG: ",spdl[i], tokens[2], objlabel, sub 
				if set([sub]).issubset(set(objlabel["readers"])) :
					print "Sent done!"
				else:
					objtemp1=copy.deepcopy(objlabel)
					objtemp1["readers"].append(sub)
					if checkDowngrade (sublabel,objlabel,objtemp1) :
						print "Downgraded Object :"+ tokens[2], objlabel, sub 
						# check for associated object ":=" token 
						objects[tokens[2]]=objtemp1
						if isAssociated( tokens[2] ) :
							dependedObj= associatedObj[tokens[2]]
							for objt1 in dependedObj:
								objects[objt1]=copy.deepcopy(objtemp1)
						storeState(spdl[i],subject,objects)
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
	printState()

from itertools import chain, combinations
def powerset(iterable):
	xs = iterable
	# note we return an iterator rather than a list
	return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )
def printLattice(plist,lattice):
	r_plist= copy.deepcopy(plist)
	r_plist.reverse() 
	for i in plist:
		 print i,' '.join(' {} '.format(val) for key, val in (lattice[i].items()))
		#print lattice[i]
		


def Lattice(file_spdl):
	l = []
	spdl=loadProtocol(file_spdl)
	i=0 # for each line in spdl 
	while i<len(spdl): 
	#	print spdl[i]
		l= spdl[i].split()
		# check for subjects 
		if l[0]=="subject":
			i+=1
			l= spdl[i].split()
			break;

	print "Lattice: "
	
	allcobm=[]
	lat={}
	lat2={}

	ind = list(powerset(l))
	revind = copy.deepcopy(ind)
	revind.reverse();

	print ind,"\n\n",revind
	for i in ind :
		allcobm.append(str(str(i).strip("(,)")))
	#print allcobm ,"\n"
	for i in allcobm :
		lat2[str(i)]=[]
	allcobm.reverse()
	for i in allcobm:
		lat[str(i)]=copy.deepcopy(lat2)

	# printLattice(allcobm,lat)
	return lat
	#print lat[ind[0]][ind[0]]
	#print '\n'.join('{} \t {} )'.format(key, val) for key, val in lat.items())
	
	
	
def putPrincipalInLattice(lattice,objects):

def main(argv): 	
	file_spdl="web-auth-1.1"
	if len(argv)<1 :
		print "Enter Protocol file in arguments!"
		exit()
	else:
		#file_spdl=argv[0]
		spdlToIFD(argv[0])
		#print "compliance checking!!!"
		#compliance_check(argv[0])
	# put all the objects into lattice 
	lattice = Lattice(argv[0]) #blanck 2d reader and writer 
	putPrincipalInLattice(lattice,objects)
	# put all object in lattice 


if __name__ == "__main__":
	main(sys.argv[1:])