#!/usr/bin/python
import sys, getopt
import copy
import utils
import pydot

#Read Protocol form file line by line and create IFD '''

def label(owner,readers,writers):
	l = {"owner": sorted(map(upper_case,owner)), "readers": sorted(map(upper_case,readers)),"writers": sorted(map(upper_case,writers)) }
	return l

def valid_label(sub_list,label):

	if set(label["owner"]).issubset(set(sub_list)) and set(label["readers"]).issubset(set(sub_list)) and set(label["writers"]).issubset(set(sub_list)):
		return True
	else:
		return False 

def get_init_subject_label(subject_list,s):
	sub = upper_case(s)
	label = {"owner": [sub], "readers": subject_list,"writers": [sub]}
	return label

def upper_case(s):
	return s.upper()

def print_label(temp_label_changed):
	print "owner : "+ str(temp_label_changed["owner"])
	print "readers : "+ str( temp_label_changed["readers"])
	print "writers : "+ str(temp_label_changed["writers"])


def init_subjects(subject_list):
	## return dict of {sub_name1 : label1, sub_name2 : label2, ...}
	m_s_list = sorted(map(upper_case,subject_list))
	subjects = {} ## dict
	for s in m_s_list:
		subjects[s] = get_init_subject_label(m_s_list,s) 

	return subjects


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

def createObjLabel(sublabel):
#""" Returns the object label for the new object being created, derived from the subject label. """
#""" obj_id is the object primary key to refer to the object from it's label.
#Pass its pk to this method with the subject label who created it. """

	objectlabel = {"owner": sublabel["owner"], "readers": sublabel["readers"],"writers": sublabel["writers"]}
	return objectlabel
'''
	Objects updated with added label with object list
'''

def createObjectWithLabel(objects,obj_list,objectlabel):
	for obj_id in obj_list:
		objects.update({obj_id:copy.deepcopy(objectlabel)})

def createObject(objects,sublabel,obj_list):
	objectlabel=createObjLabel(sublabel)
	createObjectWithLabel(objects,obj_list,objectlabel)

## subject label, object label , new object label to be downgraded
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

def getPowerList(sub_list):
	''' Enumrate all combination of labels or powerset of subjects'''

	p_list = list(powerset(sub_list))
	#p_list=map(list,p_list)
	return p_list

def printlable(label):
	for i in label:
		print i,
	print ""
def getAllLabels(sub_list):
	''' Powerset list of subjects '''
	p_list = getPowerList(sorted(sub_list))
	'''get reverse of list'''
	p_list_rev = copy.deepcopy(p_list)
	p_list_rev.reverse()

	labelset= []
	for i in p_list_rev:
		for j in p_list:
			labelset.append([i,j])

	#map(printlable,labelset)
	revlabelId ={}
	for i in range( len(labelset)):
		revlabelId.update({str(labelset[i]): i})

	#print revlabelId 

	return labelset,revlabelId
	#map(mix,p_list,p_list_rev)


def generateLattice(sub_list):
	''' Enumrate all combination of labels or powerset of subjects'''

	allcobm=[]
	lat={}
	lat2={}

	ind = list(powerset(sub_list))
	revind = copy.deepcopy(ind)
	revind.reverse();
	for i in ind :
		i=sorted(i)
		allcobm.append(str(str(i).strip("(,)")))

	for i in allcobm :
		lat2[str(i)] = { }
	allcobm.reverse()
	for i in allcobm:
		lat[str(i)]=copy.deepcopy(lat2)
	
	return lat,allcobm
	#print lat[ind[0]][ind[0]]
	#print '\n'.join('{} \t {} )'.format(key, val) for key, val in lat.items())

def putPrincipalInLattice(lattice,objects):
	p_set = lattice[1]
	lat =lattice[0]
	#print "\n\n\n"
	
	# for comb in p_set:
	# 	print comb

	# for comb in lat:
	# 	print comb
	# #print "####"
		# str = (comb.split()).strip("',")
		# print str
	#For each object plaace it on the lattice matrix

	
	for obj in objects:
		
		name = str(obj)
		label = copy.deepcopy(objects[obj])
		reader = str(sorted(label["readers"]))
		#str1 = ' '.join(reader)
		writer = str(sorted(label["writers"]))
		(lat[reader][writer]).update( { obj : label })
		#print obj ," : \t ",reader," => ",writer

def insertInLattice(lattice,objects):
	p_set = lattice[1]
	lat =lattice[0]
	# print "\n\n\n"
	
	# # for comb in p_set:
	# # 	print comb

	# for comb in lat:
	# 	print comb
	# print "####"
		# str = (comb.split()).strip("',")
		# print str
	#For each object plaace it on the lattice matrix

	for obj in objects:
		
		name = str(obj)
		label = copy.deepcopy(objects[obj])
		reader = str(sorted(label["readers"]))
		#str1 = ' '.join(reader)
		writer = str(sorted(label["writers"]))
		(lat[reader][writer]).update( { obj : label })
#		print obj ," : \t ",reader," => ",writer



from itertools import chain, combinations
def powerset(iterable):
	xs = iterable
	# note we return an iterator rather than a list
	return chain.from_iterable( sorted(combinations(xs,n)) for n in range(len(xs)+1) )

def printLattice(lattice):
	r_plist= copy.deepcopy(lattice[1])
	lat = lattice[0]
	r_plist.reverse() 
	print "lattice structure:  "
	print "".ljust(25),"".ljust(10).join(r_plist)
	for i in lattice[1]:
		print str(i).ljust(25),
		for j in r_plist:
			
			print str(len((lat[i][j]).keys())).ljust(10)," ",
		print ""
		# print i,' '.join(' {} '.format(val) for key, val in (lattice[i].items()))
		#print lattice[i]

from operator import itemgetter


def sortList(rows):
	''' It contains [[(R)(W)],.,...]'''
	return sorted(rows, key= itemgetter(0))
def sortSeclevel(seclevel):
	for i in range(len(seclevel)):
		for j in range(len(seclevel[0])):
			seclevel[i][j] = sortList(seclevel[i][j])


def getRow(seclevel,rows,i):
	ii = rows[i][0]
	jj = rows[i][1]
	return seclevel[ii][jj]

def is_lower(labellist,node1,node2):
	''' readers set and writers set connected only if r1 is subset of r2 and w1 is superset of w2 '''
	rw1 = labellist[node1]
	rw2 = labellist[node2]

	r1 =rw1[0]
	w1 = rw1 [1]

	r2 =rw2[0]
	w2 = rw2 [1]

	if set(r2).issubset(set(r1)) and set(w2).issuperset(set(w1)):
		return True
	else:
		return False
	

def get_connection(labellist,seclevel,rows):

	i=1;
	#graph = {} # graph adjecy list
	conn = dict((k, []) for k in range(len(labellist)))
	dir_conn = dict((k, []) for k in range(len(labellist)))

	while i < (len(rows) ):
		# all node in n1
		'''getRow() will give list of labels's nodes '''
		ilevel = getRow(seclevel,rows,i)
		#print ilevel
		j=i-1
		while j >= 0 :
			jlevel = getRow(seclevel,rows,j)
			''' We have two list of node's ith and jth level '''
			''' is_connceted() a function which will chek if node1 and node2 is connected '''
			for node1 in ilevel:
				for node2 in jlevel:
					
					if node2 not in list(conn[node1]) and is_lower(labellist,node1,node2):
						''' store edges '''
						dir_conn[node1].append(node2)
						conn[node1].append(node2)
						conn[node1] = list( set(conn[node1]).union(set(conn[node2])))
			j = j-1
		i=i+1

	return dir_conn,conn


def saveGraph(DirectConnection):
	import pydot
	graph = pydot.Dot( graph_type='digraph', rankdir='BT')
	node=[]
	for i in range(len(DirectConnection)):
		 
		nod= pydot.Node(name=str(i),style="filled", fillcolor="green" )
		# graph.add_node(nod)
		#nod=pydot.Node(name=str(i),style="filled", fillcolor=color,label=str(labellist[i]))
		node.append(nod)

		#node.append(pydot.Node(i,  style="filled", fillcolor="red" ))
		

	for k in DirectConnection:
		for v in DirectConnection[k]:
			graph.add_node(node[k])
			graph.add_node(node[v])
			
			graph.add_edge(pydot.Edge(node[k], node[v]))
	# graph.set_label(filename)
	graph.write_png('lattice_graph1.png', prog='dot')
	print "lattice saved in file : lattice_graph1.png!!!"




def initSeclevel(n):
	#print "\n seclevel"
	seclevel={}
	for i in range(n):
		seclevel[i]={}
		for j in range(n):
			seclevel[i][j]=[]
	#mapedID= copy.deepcopy(seclevel)

	return seclevel

def getRowsMappedId(n,seclevel,revlabelId):
	rows = []
	mapedID= copy.deepcopy(seclevel)

	for i in range(n):
		for j in range(n-1,-1,-1):
			rows.append([i,j])
			mapedID[i][j] = []
			for el in seclevel[i][j]:
				 mapedID[i][j].append(revlabelId[str(el)])
			#print " ( ",i,j, " ) ", len(seclevel[i][j]) ," => ",seclevel[i][j]
			#print " ( ",i,j, " ) ", len(mapedID[i][j]) ," => ",mapedID[i][j]

	return rows,mapedID
def generateLatticeStructure(sub_list):
	size = len(sub_list)
	n= size + 1
	'''no of levels n+1 * n+1 and based on the numbers of priniple in labels '''
	lattice = []
	seclevel = {}
	getlabOut = getAllLabels(sorted(sub_list))
	labellist = getlabOut[0]
	revlabelId = getlabOut[1]
	''' Rows of security levels based readers and writers count '''
	for i in range(n*n):
		lattice.append([])
	
	seclevel = initSeclevel(n) 

	for rw in labellist:
		''' lable has set(),reader and set() writer'''
		r=rw[0]
		w=rw[1]

		count_r = len(r)
		count_w = len(w)

		pos  = labellist.index(rw)
		''' save position only'''
		#seclevel[count_r][count_w].append(pos)
		''' all the labels in this security level'''
		seclevel[count_r][count_w].append(rw)

	sortSeclevel(seclevel)

	rows, mapedID = getRowsMappedId(n,seclevel,revlabelId)
	# rows = []
	# for i in range(n):
	# 	for j in range(n-1,-1,-1):
	# 		rows.append([i,j])
	# 		mapedID[i][j] = []
	# 		for el in seclevel[i][j]:
	# 			 mapedID[i][j].append(revlabelId[str(el)])
	# 		#print " ( ",i,j, " ) ", len(seclevel[i][j]) ," => ",seclevel[i][j]
	# 		print " ( ",i,j, " ) ", len(mapedID[i][j]) ," => ",mapedID[i][j]

	'''sort the label with readers then writers inside the sec-level'''
	resConn=get_connection(labellist,mapedID,rows)

	# print "############################\n ############### Direct connection \n"
	
	DirectConnection =resConn[0]

	#	rows = []
	'''
	# print commented for debug purpose
	for i in range(n):
		for j in range(n-1,-1,-1):
			print " ( ",i,j, " ) ", len(mapedID[i][j]) ," : ",
			for el in mapedID[i][j]: 
				print el," => ",DirectConnection[el] ,",",
			print ""
	'''
	# # create a list with security classes 
	# #allcobm = list(powerset(sub_list))

	# allcobm=[]
	# ind = list(powerset(sub_list))

	# for i in ind :
	# 	i=sorted(i)
	# 	#allcobm.append( str(i).strip("(,)"))
	# 	allcobm.append(i)
	#seclevel={}
	# for i in allcobm:
		
	# 	l=len(i),
	# 	seclevel[l].append(i)

		# seclevel[i]={}
		# for j in range(n):
		# 	seclevel[i][j]=[]
	# rows = []
	# for i in range(n):
	# 	for j in range(n-1,-1,-1):
	# 		rows.append([i,j])
	# 		print " ( ",i,j, " ) ", seclevel[i][j]
	# #print "\n".join([i]) for i in rows

	saveGraph(DirectConnection)

	return seclevel,mapedID,DirectConnection,labellist,revlabelId

def generateLatticeWithPrincipal(DirectConnection,labellist,listPrincipalNode,principal="objects",filename="default"):
	color = "blue"
	if principal == "objects":
		color= "green"
	elif principal == "subjects":
		color= "red"

	else:
		print "ERROR: function!!!"

	graph = pydot.Dot('lattice', graph_type='digraph', rankdir='BT')
	node=[]
	for i in range(len(DirectConnection)):
		if i not in listPrincipalNode.keys():
			nod= pydot.Node(i)
		else:
			nod=pydot.Node(name=str(i),style="filled", fillcolor=color,label=str(labellist[i]))
		
		graph.add_node(nod)
		node.append(nod)


	for k in DirectConnection:
		for v in DirectConnection[k]:
			graph.add_edge(pydot.Edge(node[k], node[v]))

	filename1="lattice_full_"+principal+"_"+filename+".png"
	graph.set_label(filename)
	graph.write_png(filename1, prog='dot')
	print "lattice saved in file : "+filename1+"!!!"

def addObjectctsToLattice(DirectConnection,labellist,revlabelId,objects,file_name="default"):
	listPrincipalNode = {}
	''' Fetch all the label's id '''
	for elem in objects:
		''' Get label Id form revlabelId for principal label '''
		label = objects[elem]

		rset = tuple(sorted(label["readers"]))
		wset = tuple(sorted(label["writers"]))

		lid = revlabelId[str([rset,wset])]
		listPrincipalNode.update({lid : elem })


	generateLatticeWithPrincipal(DirectConnection,labellist,listPrincipalNode,principal="objects",filename=file_name)

def addSubjectsToLattice(DirectConnection,labellist,revlabelId,subjects,file_name="default"):
	listPrincipalNode = {}
	''' Fetch all the label's id '''
	for elem in subjects:
		''' Get label Id form revlabelId for principal label '''
		label = subjects[elem]

		rset = tuple(sorted(label["readers"]))
		wset = tuple(sorted(label["writers"]))

		lid = revlabelId[str([rset,wset])]
		listPrincipalNode.update({lid : elem })

	generateLatticeWithPrincipal(DirectConnection,labellist,listPrincipalNode,principal="subjects",filename=file_name)



def getReadersWriters(label):
	'''
		Return readers and writers touple
	'''
	rset = tuple(sorted(label["readers"]))
	wset = tuple(sorted(label["writers"]))

	return [rset,wset]

def getLabelId(revlabelId,label):
	''' 
		It will return label Id 
	'''
	rset = tuple(sorted(label["readers"]))
	wset = tuple(sorted(label["writers"]))

	return revlabelId[str([rset,wset])]
	

def printDictonary(dict_t):
	for k in dict_t:
		print k, ": ",dict_t[k]


def saveObjectLatttice(associated_DC,labellist,labelObejctsDict,filename):
	import pydot
	graph = pydot.Dot( graph_type='digraph', rankdir='BT')
	node={}
	for i in labelObejctsDict:
		 
		nod= pydot.Node(name=str(i),style="filled", fillcolor="green", label=str(labelObejctsDict[i])  )
		graph.add_node(nod)
		#nod=pydot.Node(name=str(i),style="filled", fillcolor=color,label=str(labellist[i]))
		node[i]=nod

		#node.append(pydot.Node(i,  style="filled", fillcolor="red" ))
		

	for k in associated_DC:
		for v in associated_DC[k]:
			graph.add_edge(pydot.Edge(node[k], node[v]))
	f_name= "lattice_Object_"+filename+".png"
	graph.write_pngf(_name, prog='dot')
	print "lattice saved in file : "+f_name




def createObjectLattice(sub_list,labellist,revlabelId,objects,file_name="default"):

	'''
		TODO:

		1. Get enumrated rw label's for sub_list, reverseId <= from Argument
		2. Get dict of {labels: objects}
		3. Get Object label as node Id form reverseId <= create node for generating lattice
		4. Place objects on their corrosponding security level

	'''
	#2. dict of label with object 

	seclevel = initSeclevel(len(sub_list)+1)
	# put labels on there respective security level
	labelObejctsDict={}
	objectlebelset ={}
	for obj in objects:
		obj_label = objects[obj]
		rw= getReadersWriters(obj_label)
		objectlebelset[str(rw)] = rw
		
		l_ID = getLabelId(revlabelId,objects[obj])
		if l_ID not in labelObejctsDict.keys():
			labelObejctsDict[l_ID]=[obj]
		else:
			labelObejctsDict[l_ID].append(obj)

	for d_rw in objectlebelset:
		rw=objectlebelset[d_rw]
		r=rw[0]
		w=rw[1]

		count_r = len(r)
		count_w = len(w)

		#pos  = labellist.index(rw)
		#''' save position only'''
		#mapedID[count_r][count_w].append(pos)
		#''' all the labels in this security level'''
		seclevel[count_r][count_w].append(rw)

	#printDictonary(labelObejctsDict)


	'''
		genrate Direct relation ship among labels 
	'''
	rows, mapedID = getRowsMappedId(len(sub_list)+1,seclevel,revlabelId)

	resConn=get_connection(labellist,mapedID,rows)

	# print "############################\n ############### Direct connection \n"
	
	DirectConnection =resConn[0]

	n= len(sub_list)+1
	associated_DC={}
	for i in range(n):
		for j in range(n-1,-1,-1):
			#print " ( ",i,j, " ) ", len(mapedID[i][j]) ," : ",
			for el in mapedID[i][j]: 
				associated_DC[el]=DirectConnection[el]
				#print el," => ",DirectConnection[el] ,",",
			#print ""
	#printDictonary(labelObejctsDict)
	saveObjectLatttice(associated_DC,labellist,labelObejctsDict,file_name)


def saveSubjectLatttice(associated_DC,labellist,labelObejctsDict,filename):
	import pydot
	graph = pydot.Dot( graph_type='digraph', rankdir='BT')
	node={}
	for i in labelObejctsDict:
		 
		nod= pydot.Node(name=str(i),style="filled", fillcolor="red", label=str(labelObejctsDict[i]) )
		graph.add_node(nod)
		#nod=pydot.Node(name=str(i),style="filled", fillcolor=color,label=str(labellist[i]))
		node[i]=nod

		#node.append(pydot.Node(i,  style="filled", fillcolor="red" ))
		

	for k in associated_DC:
		for v in associated_DC[k]:
			graph.add_edge(pydot.Edge(node[k], node[v]))
	f_name= filename+".png"
	graph.set_label(filename)
	graph.write_png(f_name, prog='dot')
	print "lattice saved in file : "+f_name



def createSubjectLattice(sub_list,labellist,revlabelId,objects,file_name="default"):

	'''
		TODO:

		1. Get enumrated rw label's for sub_list, reverseId <= from Argument
		2. Get dict of {labels: objects}
		3. Get Object label as node Id form reverseId <= create node for generating lattice
		4. Place objects on their corrosponding security level

	'''
	#2. dict of label with object 

	seclevel = initSeclevel(len(sub_list)+1)
	# put labels on there respective security level
	labelObejctsDict={}
	objectlebelset ={}
	for obj in objects:
		obj_label = objects[obj]
		rw= getReadersWriters(obj_label)
		objectlebelset[str(rw)] = rw
		
		l_ID = getLabelId(revlabelId,objects[obj])
		if l_ID not in labelObejctsDict.keys():
			labelObejctsDict[l_ID]=[obj]
		else:
			labelObejctsDict[l_ID].append(obj)

	for d_rw in objectlebelset:
		rw=objectlebelset[d_rw]
		r=rw[0]
		w=rw[1]

		count_r = len(r)
		count_w = len(w)

		#pos  = labellist.index(rw)
		#''' save position only'''
		#mapedID[count_r][count_w].append(pos)
		#''' all the labels in this security level'''
		seclevel[count_r][count_w].append(rw)

	#printDictonary(labelObejctsDict)


	'''
		genrate Direct relation ship among labels 
	'''
	rows, mapedID = getRowsMappedId(len(sub_list)+1,seclevel,revlabelId)

	resConn=get_connection(labellist,mapedID,rows)

	# print "############################\n ############### Direct connection \n"
	
	DirectConnection =resConn[0]

	n= len(sub_list)+1
	associated_DC={}
	for i in range(n):
		for j in range(n-1,-1,-1):
			#print " ( ",i,j, " ) ", len(mapedID[i][j]) ," : ",
			for el in mapedID[i][j]: 
				associated_DC[el]=DirectConnection[el]
				#print el," => ",DirectConnection[el] ,",",
			#print ""
	#printDictonary(labelObejctsDict)
	saveSubjectLatttice(associated_DC,labellist,labelObejctsDict,file_name)
	
def save_principal_lattice(associated_DC,labellist,principal_label_dict,nodes_to_color,file_name):
	import pydot
	graph = pydot.Dot( graph_type='digraph', rankdir='BT')
	node={}

	'''
		"principal_to_color" has the name of the node to be higlighted
		TODO:
			1: take out  
	'''

	
	for i in principal_label_dict:
		 
		nod= pydot.Node(name=str(i), label=str(principal_label_dict[i]) )
		graph.add_node(nod)
		#nod=pydot.Node(name=str(i),style="filled", fillcolor=color,label=str(labellist[i]))
		node[i]=nod

		#node.append(pydot.Node(i,  style="filled", fillcolor="red" ))
	# add colored node for showing changes
	for i in nodes_to_color:
		nod= pydot.Node(name=str(i),style="filled", fillcolor="green", label=str(principal_label_dict[i]) )
		graph.add_node(nod)
		node[i]=nod
	

	for k in associated_DC:
		for v in associated_DC[k]:
			graph.add_edge(pydot.Edge(node[k], node[v]))
	f_name= file_name.split()[0]+".png"
	graph.set_label(file_name)
	graph.write_png(f_name, prog='dot')
	#print "lattice saved in file : "+f_name

def create_principal_lattice(labellist,revlabelId,subjects,objects,c_principal,file_name="default"):
	'''
		c_principal = those should only be higlighted with color
		TODO
			reverse map the principal id with label
			check object name and its case 
				lower => object
				uppper => subject 
			find 
	'''
	sub_list = sorted(subjects.keys())
	seclevel = initSeclevel(len(sub_list)+1)

	principal_label_set = {}
	principal_label_dict={} # dict with label vs pincipal's name list for the purpose of lattice label name
	nodes_to_color = {}
	# add subjects first
	for sub in subjects:
		sub_label = subjects[sub]
		rw= getReadersWriters(sub_label)
		principal_label_set[revlabelId[str(rw)]] = rw
		if revlabelId[str(rw)] not in principal_label_dict:
			principal_label_dict[revlabelId[str(rw)]] = [sub]
		else:
			principal_label_dict[revlabelId[str(rw)]].append(sub)

		## change color
		if sub in c_principal:
			if revlabelId[str(rw)] not in nodes_to_color:
				nodes_to_color[revlabelId[str(rw)]] = [sub]
			else:
				nodes_to_color[revlabelId[str(rw)]].append(sub)

	# add objects 
	for obj in objects:
		obj_label = objects[obj]
		rw= getReadersWriters(obj_label)
		principal_label_set[revlabelId[str(rw)]] = rw
		if revlabelId[str(rw)] not in principal_label_dict:
			principal_label_dict[revlabelId[str(rw)]] = [obj]
		else:
			principal_label_dict[revlabelId[str(rw)]].append(obj)

	### changed color node


		if obj in c_principal:
			if revlabelId[str(rw)] not in nodes_to_color:
				nodes_to_color[revlabelId[str(rw)]] = [obj]
			else:
				nodes_to_color[revlabelId[str(rw)]].append(obj)


	## add all label to seclevel and get their respective id  
	#printDictonary(principal_label_dict)

	for d_rw in principal_label_set:
		rw=principal_label_set[d_rw]
		r=rw[0]
		w=rw[1]

		count_r = len(r)
		count_w = len(w)

		#pos  = labellist.index(rw)
		#''' save position only'''
		#mapedID[count_r][count_w].append(pos)
		#''' all the labels in this security level'''
		seclevel[count_r][count_w].append(rw)

	# replace label with its ID => mapedID

	rows, mapedID = getRowsMappedId(len(sub_list)+1,seclevel,revlabelId)

	# get all connection with the label id 
	res_Conn=get_connection(labellist,mapedID,rows)
	
	# get all DirectConnection list fro res_Conn 
	DirectConnection =res_Conn[0]

	# get only the required nodes which are interconnect or take into  connection
	n= len(sub_list)+1
	associated_DC={}
	for i in range(n):
		for j in range(n-1,-1,-1):
			#print " ( ",i,j, " ) ", len(mapedID[i][j]) ," : ",
			for el in mapedID[i][j]: 
				associated_DC[el]=DirectConnection[el]
				#print el," => ",DirectConnection[el] ,",",
			#print ""

	save_principal_lattice(associated_DC,labellist,principal_label_dict,nodes_to_color,file_name)



# '''
# '''

# def create_principal_lattice(sub_list,labellist,revlabelId,subjects,objects,file_name="default"):
# 	'''
# 		"put only subject and object into lattice based on there labels relation with color code"
# 	'''
# 	seclevel_obj = initSeclevel(len(sub_list)+1)
# 	seclevel_sub = initSeclevel(len(sub_list)+1)
	
# 	# put labels on there respective security level
# 	labelObejctsDict={}
# 	labelSubjectDict={}

# 	objectlebelset = {}
# 	subjectlabelset = {}
# 	for obj in objects:
# 		obj_label = objects[obj]
# 		rw= getReadersWriters(obj_label)
# 		objectlebelset[str(rw)] = rw
		
# 		l_ID = getLabelId(revlabelId,objects[obj])
# 		if l_ID not in labelObejctsDict.keys():
# 			labelObejctsDict[l_ID]=[obj]
# 		else:
# 			labelObejctsDict[l_ID].append(obj)


# 	for sub in objects:
# 		sub_label = subjects[sub]
# 		rw= getReadersWriters(sub_label)
# 		subjectlebelset[str(rw)] = rw
		
# 		l_ID = getLabelId(revlabelId,objects[obj])
# 		if l_ID not in labelObejctsDict.keys():
# 			labelSubjectDict[l_ID]=[obj]
# 		else:
# 			labelSubjectDict[l_ID].append(obj)


# 	for d_rw in objectlebelset:
# 		rw=objectlebelset[d_rw]
# 		r=rw[0]
# 		w=rw[1]

# 		count_r = len(r)
# 		count_w = len(w)

# 		#pos  = labellist.index(rw)
# 		#''' save position only'''
# 		#mapedID[count_r][count_w].append(pos)
# 		#''' all the labels in this security level'''
# 		seclevel_obj[count_r][count_w].append(rw)


# 	for d_rw in subjectlebelset:
# 		rw=subjectlebelset[d_rw]
# 		r=rw[0]
# 		w=rw[1]

# 		count_r = len(r)
# 		count_w = len(w)

# 		#pos  = labellist.index(rw)
# 		#''' save position only'''
# 		#mapedID[count_r][count_w].append(pos)
# 		#''' all the labels in this security level'''
# 		seclevel_sub[count_r][count_w].append(rw)
# 	printDictonary(labelObejctsDict)


# 	'''
# 		genrate Direct relation ship among labels 
# 	'''
# 	rows, mapedID = getRowsMappedId(len(sub_list)+1,seclevel,revlabelId)

# 	resConn=get_connection(labellist,mapedID,rows)

# 	print "############################\n ############### Direct connection \n"
	
# 	DirectConnection =resConn[0]

# 	n= len(sub_list)+1
# 	associated_DC={}
# 	for i in range(n):
# 		for j in range(n-1,-1,-1):
# 			print " ( ",i,j, " ) ", len(mapedID[i][j]) ," : ",
# 			for el in mapedID[i][j]: 
# 				associated_DC[el]=DirectConnection[el]
# 				print el," => ",DirectConnection[el] ,",",
# 			print ""
# 	printDictonary(labelObejctsDict)
# 	saveSubjectLatttice(associated_DC,labellist,labelObejctsDict,file_name)