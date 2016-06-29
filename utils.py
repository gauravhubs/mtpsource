import sys 
import state
from itertools import chain, combinations

def powerset(iterable):
	xs = iterable
	# note we return an iterator rather than a list
	return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )

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

def query_response(question,valid):
    """Ask a question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    #valid = {"yes": True, "y": True, "ye": True,
    #         "no": False, "n": False}
    # if default is None:
    #     prompt = " [y/n] "
    # elif default == "yes":
    #     prompt = " [Y/n] "
    # elif default == "no":
    #     prompt = " [y/N] "
    # else:
    #     raise ValueError("invalid default answer: '%s'" % default)

    prompt="/".join(map(str,valid))
    while True:
        sys.stdout.write(question +"\nGive Your Response as [ "+ prompt + " ] : ")
        choice = raw_input()
        print choice
        if int(choice) in valid:
            return choice
        else:
            sys.stdout.write("\nPlease respond with  [ "+ prompt+" ] :\n")

def query_name(msg):
    prompt= " : "
    sys.stdout.write(msg + prompt)
    return (raw_input()).strip()

def query_name_list(msg):
    prompt= " : "
    sys.stdout.write(msg + prompt)
    s = raw_input()
    l_str = s.strip().split()

    return l_str

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def query_numbers(msg):
    prompt = " [ 1/2/3/... ] "

    sys.stdout.write(msg)
    choice = raw_input("\nEx : " + prompt)
    try:
        res = int(choice)
    except Exception ,e:
        print "Program halted incorrect data entered",type(choice)
    return res