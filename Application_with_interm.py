import utils
import sys
import rwfm
import protocol as prot
import parser
import copy

objectID = 0 ## global

def welcome():


	## cli
	msg_welcome = ("welcome!!!").center(80)

	spdl_language = """
			SPDL language syntax :
		principal ::=  P1 | P2 | .... | Pn 
		fn        ::=  f1 | f2 | .....| fn
		object    ::=  O1 | O2 | .... | On 
		msg       ::= object | fn( msg , msg ,...) | (msg, msg, ...)
		step      ::= send ( principal, principal, msg)
		protocol  ::= step | step; protocol
					"""

	print msg_welcome
	print spdl_language

def get_Response(msg_q_start,msg_q_start_valid):

	response = utils.query_response(question=msg_q_start,valid=msg_q_start_valid)
	return response

def get_principal(pr_num):
	pr=[]
	for i in range(pr_num):
		pr.append(str(raw_input(str(i+1) +" : ")).upper())
	return sorted(pr)

def check_valid_label(sub_list,o_label):
	#print "object label check_valid_label :",o_label
	return rwfm.valid_label(sub_list,o_label)

def validate_with_principal(principal,sender):
	if set(sender.strip()).issubset(set(principal)):
		return True
	else:
		return False

def show_list(list_v):
	print ""
	for el in list_v:
		print el
	print "" 
def get_init_objects(sub_list):

	msg = "No of initial objects : "
	o_num = utils.query_numbers(msg)

	objects_list = []
	init_objects = {}
	for i in range(o_num):
		# for each object get owenr, subject, object list
		name_msg = str(i+1) +" object name "
		o_name = utils.query_name(name_msg)
		o_owner = utils.query_name_list("\t"+o_name + " owner list")
		o_readers = utils.query_name_list("\t"+o_name + " readers list")
		o_writers = utils.query_name_list("\t"+o_name + " writers list")

		'''
			create label and add to objects dict with case property for subject 
		'''
		o_label =rwfm.label(o_owner,o_readers,o_writers)
		
		if not check_valid_label(sub_list,o_label):	## validate with case and sorting as well
			print "objects not in with valid subject of the protocol system!!!"
			break

		init_objects[o_name]=o_label
		# for showing change in ifd
		objects_list.append(o_name)

	return objects_list,init_objects

def get_token(message):
	token = re.split(r'(;|,|\(|\)|\s)\s*', message)
	t =  map(sstrip,token)
	t1=filter(lambda a: a != "", t)
	t2=filter(lambda a: a != ",", t1)
	return t2

def get_steps_intermediate(objects_list):
	msg1= "Who is the sender ? "
	msg2= "Who is the intended recipient ?"
	msg4 = "Message is "
	sender = utils.query_name(msg1).strip().upper()
	if(sender == "DONE"):
		return "done"
	recipient = utils.query_name(msg2).strip().upper()

	message = utils.query_name(msg4)
	operation = []
	while "=" in message:
		tok=message.split('=')
		var= tok[0].strip()
		func= tok[1].strip()
		oper_seq = parse_msg(func) # sequence of message and functions
		local_operation	= get_operations(oper_seq,objects_list,sender,i_obj=var)
		operation.extend(local_operation)
		message = utils.query_name("\nNext line")

	oper_seq = parse_msg(message) # sequence of message and functions
	local_operation	= get_operations(oper_seq,objects_list,sender)
	operation.extend(local_operation)


	#step_b = "send ( "+str(sender)+", "+str(recipient)+", "+message.strip()+" )"
	step = [message,sender,recipient,operation]
	#print message
	'''
	return function name and expended function 
	'''
	return step

	
def get_steps():
	#show_principal()
	msg1= "Who is the sender ? "
	msg2= "Who is the intended recipient ?"
	msg4 = "Message is "
	sender = utils.query_name(msg1).strip().upper()
	if(sender == "DONE"):
		return "done"
	recipient = utils.query_name(msg2).strip().upper()
	message_list=[]
	f_dict= {}
	orig_function = {}
	message = utils.query_name(msg4)
	while "=" in message:
		tok=message.split('=')
		var= tok[0].strip()
		func= tok[1].strip()
		orig_function.update({var:copy.deepcopy(func)})
		f_dict.update({var: func})
		# final exended token
		s_tized = func

		tmsg = parser.get_token(func)
	#	print tmsg
		for t in tmsg:
			#print t
			if t in message_list:
	#			print "Found = ", t
				s_tized = s_tized.replace(t,f_dict[t])
	#	print s_tized
		f_dict.update({var:s_tized})

		message_list.append(var)
		message = utils.query_name("\nNext line : ")

	# substitute the message with function   
	# final extended token

	tmsg = parser.get_token(message)
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
	step_b = "send ( "+str(sender)+", "+str(recipient)+", "+message.strip()+" )"
	# validate(sub_list,sender)
	# validate(sub_list,recipient)
	step = [step_b,sender,recipient,message]
	#print message
	'''
	return function name and expended function 
	'''
	return step,orig_function,f_dict,message_list


def parse_msg(msg):
	'''
		Parse the message and get the required basic local operation read, create
	'''
	#print "Message parsing :"
	lisp_parsed_msg =  parser.get_parsed(msg)
	#print "lisp_parsed_msg : "
	#show_list(lisp_parsed_msg)
	#print "print done!\n"
	return lisp_parsed_msg

def sstrip(s):
	return s.strip()
def get_operations(oper_seq,objects_list,sender,i_obj="_NONE"):
	global objectID
	# for each oper's sequence get read create message if its present in objects_list
	read_create_seq = []
	#temp_object_list = []
	#print "Inside get_operations\n"

	# if len(oper_seq) ==1 :
	# 	msg = oper_seq[0]
	# 	if msg in objects_list :
	# 		local_op =str(sender) + " read " + str(msg)
	# 	else:
	# 		local_op =str(sender) + " create " + str(msg)
	# 		#'TODO:  add create opeation with state IFD'
	# 		objects_list.append(msg)
	# 	read_create_seq.append(local_op)
	#	 
	# else:
	
	for msg in oper_seq:
		#print msg
		i_state = ""
		if isinstance(msg, basestring):
			#print "isinstance true"
			if msg in objects_list :
				local_op =str(sender) + " read " + str(msg)
			else:
				local_op =str(sender) + " create " + str(msg)
			#'TODO:  add create operation with state IFD'
			objects_list.append(msg)
			read_create_seq.append(local_op)
		elif len(msg) > 1:
			# handle '__TUPLE_S'
			j=0
			if msg[0] == "__TUPLE_S":
				j = 1
				i_state = "Tup_"+str(objectID)

			
			elif msg[0] == "__FUN_S":
				j = 2
				i_state = "fun_"+str(objectID)
			objectID= objectID + 1
			
			while  j<len(msg):
				# check for message exist in object list 
				#if not isinstance(msg[j], basestring) or utils.is_number(msg[j]):
				if not isinstance(msg[j], basestring) or utils.is_number(msg[j]):
					j = j +1
					#local_op =str(sender) + " create " + str(i_state) 
					'''
						create intermediate funtion as well READ them
					'''
					#print "Not read or created",msg[j-1]
					continue

				local_op=""
				if msg[j] in objects_list :
					local_op =str(sender) + " read " + str(msg[j])
				else:
					local_op =str(sender) + " create " + str(msg[j])
					#'TODO:  add create operation with state IFD'
					objects_list.append(msg[j])
				read_create_seq.append(local_op)
				j = j+1 
			#objects_list.append(msg[j])
			#read_create_seq.append(str(sender)+ " create "+str(msg))

	#show_list(read_create_seq)
	if(i_obj != "_NONE"):
		local_op =str(sender) + " create " + str(i_obj)
		objects_list.append(i_obj)
		read_create_seq.append(local_op)
	return read_create_seq

			# handle '__FUNCT_S'
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
def  save_lattice_file(p_name):
	import os
	os.system("echo 'Generation of lattice pdf'")
	# if which("convert") == None:
	# 	print "Install:: apt-get install ImageMagick "
	# else :
	# 	os.system("convert $(find *.png | sort -n) "+p_name+"_lattice.pdf")
	os.system("convert $(find *.png | sort -n) "+p_name+"_lattice.pdf")

		
def clean_image():
	import os
	os.system("rm *.png")
def new_protocol():
	l_counter = 0
	title = "New Protocol".center(80)
	msg_name = "Give name of new protocol"
	msg_q_nos_p = "Numbers of principals in this protocol"
	msg_exist_obj = "Numbers of existing objects in system"
	
	print title
	clean_image()
	p_name = utils.query_name(msg_name)
	pr_num = utils.query_numbers(msg_q_nos_p)
	
	# lsit of principle <subjects>"In UPPER CASE"
	principal = get_principal(pr_num)
	
	subjects = rwfm.init_subjects(principal)
	objects = {}
	# list of Initial objectec in lower case 
	objects_list, init_objects = get_init_objects(principal) # done
	#principal.extend(objects_list)
	# global protocol = prot.Protocol(p_name)
	#print "saved state\n"
	#print principal,"\n",objects_list,init_objects
	
	objects.update(init_objects)
	'''
	Now initialize protocol :

	give name of protocol
	put subject and objects in to it
	annotate initial labels 
	save a copy of the state of the protocol
	'''
	##########################BEGIN###################

	protocol = prot.Protocol(p_name)
	l_counter +=1
	protocol.add_state(prot.State(subjects,init_objects,str(l_counter)+" "+"load initial objects"))
	##########################END#####################
	
	# protocol.add_state(State(subjects,objects,"Protocol initialize"))
	protocol.get_ifd()
	while True:
		oper_seq_label = {}
		
		#step_ret=get_steps() # sender recipient and msg
		step_int=get_steps_intermediate(objects_list)
		# if step_ret == "done":
		# 	break
		if step_int == "done":
			break
		else:
			step = step_int
			#functions = step_ret[1]
			#functions_expended = step_ret[2]

			#protocol.add_functions(functions)
			message, sender, recipient, local_operation = step # step a list object
			#print message
			if not validate_with_principal(principal,sender) and not validate_with_principal(principal,recipient) :
				print "Not in correct format"
			#oper_seq = parse_msg(message) # sequence of message and functions

			#local_operation	= get_operations(oper_seq,objects_list,sender) 
			## A read object
			## A create object

			for op in local_operation:
				token = op.strip().split()
				map(sstrip,token)
				print token
				sublabel = subjects[token[0]]
				ll_op = token[1]
				protocol.put_spdl_cmd(op)
				### save the counter to lattice :: for lattice order 
				l_counter +=1
				if ll_op == "read" or ll_op == "READ":
					## change of subject label
					objlabel = objects[token[2]]
					result = rwfm.checkRead(sublabel,objlabel)
					if result["bool"]==True :
						#print "-->Inside result ",result["sublabel"]
						#print "\n"
						subjects[token[0]]=result["sublabel"]
						protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+op,token[0]))
						print " %s Read done!!\nSubject label Updated:"%token[2],token[0]," ",subjects[token[0]]
					else:
						#printState(state,stateCMD,principal)
						print "READ DENY on CMD :"+ op , objlabel, token[0]
						exit()
				elif ll_op == "create" or ll_op == "CREATE":
					## update object dict
					temp_label=rwfm.createObjLabel(sublabel)
					temp_label_changed = copy.deepcopy(temp_label)
					objects[token[2]]= copy.deepcopy(temp_label)
					
					protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+op,token[2]))
					'''
						Ask for intended readers of the object
					'''
					print "Currently reader set of object <%s> is "% token[2],temp_label["readers"]
					if utils.query_yes_no("Do you want to change readers"):

						intention_msg = "Please give intended readers of the object <"+token[2]+"> "
						let_readers_set = sorted(list(set(utils.query_name_list(intention_msg))))
						####################################################################################
						let_form  = "\tlet\n\t\t " + token[2] +" READABLE-BY "+str(let_readers_set)+ "\n\ttel"
						print let_form
						protocol.put_spdl_cmd(let_form)
						####################################################################################
						temp_label_changed["readers"]= let_readers_set
						print "New labels of object <%s> :\n"%token[2]
						rwfm.print_label(temp_label_changed)
						#print "Downgrade or upgrade checking!"
						s_lrset = len(temp_label_changed["readers"])
						s_trset = len(temp_label["readers"])
						if s_lrset == s_trset:
						 	if set(temp_label_changed["readers"]).issubset(set(temp_label["readers"])):
								print "No change!"
							else :
								## check for upgrade 
								print "Upgrade check!"
								if rwfm.checkUpgrade(sublabel,temp_label,temp_label_changed) or rwfm.checkDowngrade(sublabel,temp_label,temp_label_changed): 
									print "Upgrading done!"
									objects[token[2]] = temp_label_changed
									n_op = token[0] + " Upgrades "+token[2] 
									
									l_counter +=1
									### save the counter to lattice :: for lattice order 
									protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+n_op,token[2]))
									
									#protocol.put_spdl_cmd(n_op)
								else:
									protocol.get_ifd()
									print "Upgrading not possible! exiting!!!"
									exit(1)

						elif s_lrset > s_trset :
							print "Downgrade check!"
							if rwfm.checkDowngrade(sublabel,temp_label,temp_label_changed):
								print "Downgrading done!"
								objects[token[2]] = temp_label_changed
								n_op = token[0] + " Downgrades "+token[2] 
								### save the counter to lattice :: for lattice order 
								l_counter +=1
								protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+n_op,token[2]))
								#protocol.put_spdl_cmd(n_op)
							else:
								print "Downgrading not possible"
								exit(1)
						else:
							print "Upgrade check!"
							if rwfm.checkUpgrade(sublabel,temp_label,temp_label_changed):
								print "Upgrading done!"
								objects[token[2]] = temp_label_changed
								n_op = token[0] + " Upgrades "+token[2] 
								### save the counter to lattice :: for lattice order 
								l_counter +=1
								protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+n_op,token[2]))
								#protocol.put_spdl_cmd(n_op)
							else:
								print "Upgrading not possible! exit!!"
								exit(1)
				else:
					print "Unknown command !"
					exit()
				# protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+op))
			print "Local operation :"
			show_list(local_operation)
			'''
				Before send check for recipient can read msg or can be downgraded  
			'''
			#print sender +" send "+ message + " to "+recipient
			#objects[str(message)] = copy.deepcopy(subjects[sender]) # holds the lub of all the objects as all the objects has been read
			oper_send = sender+" send "+message+" to "+recipient
			print oper_send

			objlabel=objects[str(message).strip()]
			sublabel=subjects[sender]
			if set([recipient]).issubset(set(objlabel["readers"])) :
				print "Readers of object < %s > are :"%message, objlabel["readers"] 
				print "Sent done!"
			else:
				objtemp1=copy.deepcopy(objlabel)
				objtemp1["readers"].append(recipient)
				if rwfm.checkDowngrade (sublabel,objlabel,objtemp1) :
					print "Downgraded Object :"+ message, objlabel, sublabel 
					# check for associated object ":=" token 
					downgrade_list =[]
					objects[str(message)]=objtemp1
					# downgrade_list.append(tokens[2])

					# if isAssociated( tokens[2],associatedObj) :
					# 	dependedObj= associatedObj[tokens[2]]
					# 	for objt1 in dependedObj:
					# 		objects[objt1]=copy.deepcopy(objtemp1)
					# 		downgrade_list.append(objt1)

					obj_d_msg=sender+" "+ " Downgrades "+message
					

					# storeState(state,stateCMD,obj_d_msg,subjects,objects)
					# storeFullState(f_state,f_state_CMD,obj_d_msg,subjects,objects)
					# store_change(current_change,obj_d_msg,downgrade_list)
					print "Downgrade Done! "
					### save the counter to lattice :: for lattice order 
					l_counter +=1
					protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+obj_d_msg,message))
				else:
					#printState()
					print "Downgrading Fail! on cmd: " + sender +" -> "+recipient+" :: "+message
					exit()
			'''
				TODOAfter send operation the reading of sent message to recipient should be done
			'''
			#################################################################
			
			protocol.put_spdl_cmd(oper_send)
			#################################################################
			print "message received at recipient and processed at that place "

			'''

			TODO let command inclusion 
				1. Ask Designer whether the sender has intended recipients or want to change the readers set
				2. get new reader set and check for downgrading 
				3. Downgrade / upgrade possible or not
				4. Possible allow for next state 
				6. Continue with the protocol
			'''
			
			print "Current Readers of <%s> is :"% str(message), str(objects[str(message)]["readers"])
			####################################################################################
			# intention_msg = "Please give intended readers of the object <"+message+"> "
			# let_readers_set = sorted(list(set(utils.query_name_list(intention_msg))))
			let_form  = "\tlet\n\t\t " + message +" READABLE-BY "+str(objects[str(message)]["readers"])+ "\n\ttel"
			print let_form
			protocol.put_spdl_cmd(let_form)
			####################################################################################
			# ll_state = get_local_states(protocol,local_operation)
			'''
				Asynchronous Read operation on sent objects "message"
			'''
			objlabel = objects[message]
			sublabel = subjects[recipient]
			result = rwfm.checkRead(sublabel,objlabel)
			if result["bool"]==True :
				#print "-->Inside result ",result["sublabel"]
				#print "\n"
				subjects[recipient]=result["sublabel"]
				op = recipient + " read "+ message
				### save the counter to lattice :: for lattice order 
				l_counter +=1
				protocol.add_state( prot.State(subjects,objects,str(l_counter)+" "+op,recipient))
				print "Read done!  subject label Updated:",token[0]," ",subjects[token[0]]
			else:
				#printState(state,stateCMD,principal)
				print "READ DENY on CMD :"+ op , objlabel, token[0]
				exit()
			
	print "\nSuccess!!!"
	#protocol.get_ifd()
	protocol.save_ifd(filename=p_name)
	protocol.save_spdl_cmd(filename = p_name)
	save_lattice_file(p_name)
	#print p_name,pr_num

def existing_protocol():
	print "inside existing "

def main():

	welcome()
	msg_q_start = """
	Choose your choice of : 
		1. Design New Protocol
		2. Re-Design Existing Protocol 
			"""
	msg_q_start_valid = { 1:"Design New Protocol", 2: "Re Design Existing Protocol"}
	response=get_Response(msg_q_start,msg_q_start_valid.keys())

	if response == "1" :
		new_protocol()
	elif response == "2": 
		existing_protocol()


if __name__ == "__main__":
	# if len(sys.argv[1:])<1 :
	# 	print "Enter Protocol file in arguments!"
	# 	exit()
	main()
