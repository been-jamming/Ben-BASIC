#----------Ben-BASIC----------
#-------------By:-------------
#----------Ben Jones----------
#
#	Usage
#
#first, import the module with:
#-import Interpret
#or use a more advanced method like:
#-from Interpret import Tokens as t
#
#	Classes
#
#-t = Interpret.Tokens(self, string, variables)      Creates an instance of the Tokens class.
#	-t.tokens                                        Gets the tokens from the last Tokenize call.
#	-t.char                                          Gets the character position after the Tokenize call.
#	-t.string                                        Gets the string the Tokenize function works on.
#-t.NextCharacter(self)                              Returns the next character in the string.
#-t.PreviousCharacter(self)                          Returns the previous character in the string.
#-t.Tokenize(self)                                   Tokenizes the string.
#
#	Functions
#
#-data = Interpret.Interpret(string)                 Interprets the given expressison, and returns a list
#                                                    of data values representing the simplified values of
#                                                    the expression.
#
#-Run_Line(string)                                   Runs a given line of Ben-BASIC code. Must begin with
#                                                    a command and follow with expressions seperated by
#                                                    commas
#
#-Run_File(filename)                                 Runs a program in the given filename. Each line in
#                                                    the file corresponds to that number line of code.
#
#-Command_Line()                                     Starts Ben-BASIC in command line mode. To enter a
#                                                    program, start with a line number, followed by a
#                                                    space and then some code. Type "run" to run it. ex:
#                                                   ->>> 10 Input name, "Enter your name: "
#                                                   ->>> 20 print "Hello "+name
#                                                   ->>> run
#                                                   -<<< Enter your name: Ben Jones
#                                                   -<<< Hello Ben Jones
#                                                    You can also enter in normal commands from the
#                                                    command line. ex:
#                                                   ->>> print int(221/4)
#                                                   -<<< 55


import random, math, sys, time
try:
	import pygame
	pygame.init()
except ImportError:
	pygame = False

digits = ["1","2","3","4","5","6","7","8","9","0"]
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
operations = ["+","-","*","/"]
whitespace = [" ","	"]
seperators = [",",":"]
comparison = ["<",">","=","!"]
loops = []
looptypes = ["if","for","while"]
gosubs = []
labels = {}

INTEGER, FLOAT, CHARACTER, STRING, LIST, MATRIX, ADD, SUBTRACT, MULTIPLY, DIVIDE, PARENTHESES, VARIABLE, FUNCTION, SEPERATOR, ARRAY, COMPARISON = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768

linenum = 0
screen = False
exit = False
color = (255,255,255)

click = [-1, -1]
keys = []
lastmx = None
lastmy = None
open_file = None

#	---Funtions---

def Nothing(args):
	return str(args[0])
def Str(args):
	if len(args)!=1:
		raise Exception("Argument Error: function str takes 1 argument")
	else:
		out = (args[0][0], STRING)
		return out
def Float(args):
	if len(args)!=1:
		raise Exception("Argument Error: function float takes 1 argument")
	else:
		try:
			return (str(float(args[0][0])), FLOAT)
		except:
			raise Exception("Conversion Error: could not convert "+args[0][0]+" to a float")
def Not(args):
	if len(args)!=1:
		raise Exception("Argument Error: function not takes 1 argument")
	else:
		if args[0][1] == INTEGER or args[0][1] == FLOAT:
			if int(args[0][0]) == 1:
				return ("0.0", FLOAT)
			else:
				return ("1.0", FLOAT)
		else:
			raise Exception("Argument Error: argument must be a float or integer")
def Sqrt(args):
	if len(args)!=1:
		raise Exception("Argument Error: function sqrt takes 1 argument")
	else:
		if args[0][1] == INTEGER or args[0][1] == FLOAT:
			return (str(float(float(args[0][0])**0.5)), FLOAT)
		else:
			raise Exception("Argument Error: argument must be a float or integer")
def Rand(args):
	if args != [("None", None)]:
		raise Exception("Argument Error: rand takes 0 arguments")
	return (str(random.random()), FLOAT)
def Randint(args):
	if len(args) == 2:
		if args[0][1] == INTEGER:
			lower = int(args[0][0])
		else:
			raise Exception("Argument Error: argument must be an integer")
		if args[1][1] == INTEGER:
			upper = int(args[1][0])
		else:
			raise Exception("Argument Error: argument must be an integer")
		return (str(random.randint(lower, upper)), INTEGER)
	else:
		raise Exception("Argument Error: randint takes 2 arguments")
def Int(args):
	if len(args) == 1:
		try:
			return(str(int(float(args[0][0]))), INTEGER)
		except:
			raise Exception("Conversion Error: could not convert "+args[0][0]+" to an integer")
	else:
		raise Exception("Argument Error: function int takes 1 argument")
def Exp(args):
	if len(args) == 1:
		if args[0][1] == FLOAT or args[0][1] == INTEGER:
			return (str(math.exp(float(args[0][0]))), FLOAT)
		else:
			raise Exception("Argument Error: argument must be an integer or float")
	elif len(args) == 2:
		if (args[0][1] == FLOAT or args[0][1] == INTEGER) and (args[0][1] == FLOAT or args[0][1] == INTEGER):
			return (str(float(args[1][0])**float(args[0][0])), FLOAT)
	else:
		raise Exception("Argument Error: function exp takes 1 argument")
def Log(args):
	if len(args) == 1 and args[0] != (None, None):
		if args[0][1] == FLOAT or args[0][1] == INTEGER:
			return (str(math.log(float(args[0][0]))), FLOAT)
		else:
			raise Exception("Argument Error: argument must be an integer or float")
	elif len(args) == 2:
		if (args[0][1] == FLOAT or args[0][1] == INTEGER) and (args[1][1] == FLOAT or args[1][1] == INTEGER):
			return (str(math.log(float(args[0][0]), float(args[1][0]))), FLOAT)
		else:
			raise Exception("Argumen Error: argument must be an integer or float")
	else:
		raise Exception("Argument Error: function log takes 1-2 arguments")
def Sin(args):
	if len(args) == 1 and args[0] != (None, None):
		if args[0][1] == FLOAT or args[0][1] == INTEGER:
			return (str(math.sin(float(args[0][0]))), FLOAT)
		else:
			raise Exception("Argument Error: argument must be an integer or float")
	else:
		raise Exception("Argument Error: function sin takes 1 argument")
def Cos(args):
	if len(args) == 1 and args[0] != (None, None):
		if args[0][1] == FLOAT or args[0][1] == INTEGER:
			return (str(math.cos(float(args[0][0]))), FLOAT)
		else:
			raise Exception("Argument Error: argument must be an integer or float")
	else:
		raise Exception("Argument Error: function cos takes 1 argument")
def Tan(args):
	if len(args) == 1 and args[0] != (None, None):
		if args[0][1] == FLOAT or args[0][1] == INTEGER:
			return (str(math.tan(float(args[0][0]))), FLOAT)
		else:
			raise Exception("Argument Error: argument must be an integer or float")
	else:
		raise Exception("Argument Error: function tan takes 1 argument")
def Eval(args):
	if len(args) == 1 and args[0] != (None, None):
		if args[0][1] == STRING:
			return Interpret(args[0][0])[0][0]
		else:
			raise Exception("Argument Error: argument must be a string")
	else:
		raise Exception("Argument Error: function eval takes 1 argument")
def Mousex(args):
	return (str(pygame.mouse.get_pos()[0]), INTEGER)
def Mousey(args):
	return (str(pygame.mouse.get_pos()[1]), INTEGER)
def Mousedx(args):
	global lastmx
	x = pygame.mouse.get_pos()[0]
	if lastmx == None:
		lastmx = x
		return ("0", INTEGER)
	else:
		dx = x - lastmx
		lastmx = x
		return (str(dx), FLOAT)
def Mousedy(args):
	global lastmy
	y = pygame.mouse.get_pos()[1]
	if lastmy == None:
		lastmy = y
		return ("0", INTEGER)
	else:
		dy = y - lastmy
		lastmy = y
		return (str(dy), FLOAT)
def Winexit(args):
	global exit
	if exit == True:
		exit = False
		return ("1", INTEGER)
	else:
		return ("0", INTEGER)
def Clickx(args):
	global click
	cx = click[0]
	click[0] = -1
	return (str(cx), INTEGER)
def Clicky(args):
	global click
	cy = click[1]
	click[1] = -1
	return (str(cy), INTEGER)
def Keypress(args):
	global keys
	if len(keys) == 0:
		return ("-1", INTEGER)
	else:
		return (str(keys.pop(0)), INTEGER)
def Chr(args):
	if len(args) == 1:
		if args[0][1] == INTEGER:
			return (chr(int(args[0][0])), STRING)
		else:
			raise Exception("Argument Error: argument must be an integer")
	else:
		raise Exception("Argument Error: chr takes 1 argument")
def Len(args):
	if len(args) != 1:
		raise Exception("Argument Error: Len takes 1 argument")
	if args[0][1] != STRING:
		raise Exception("Argument Error: argument must be a string")
	return (str(len(args[0][0])), INTEGER)
def Mid(args):
	if len(args) == 3:
		if (args[1][1] != INTEGER) or (args[2][1] != INTEGER):
			raise Exception("Argument Error: argument must be an integer")
		if args[0][1] != STRING:
			raise Exception("Argument Error: argument must be a string")
		return (args[0][0][int(args[1][0])-1:][:int(args[2][0])], STRING)
	else:
		raise Exception("Argument Error: mid takes 3 arguments")
def Right(args):
	if len(args) == 2:
		if args[1][1] != INTEGER:
			raise Exception("Argument Error: argument must be an integer")
		if args[0][1] != STRING:
			raise Exception("Argument Error: argument must be a string")
		return (args[0][0][-int(args[1][0]):], STRING)
	else:
		raise Exception("Argument Error: left takes 3 arguments")
def Left(args):
	if len(args) == 2:
		if args[1][1] != INTEGER:
			raise Exception("Argument Error: argument must be an integer")
		if args[0][1] != STRING:
			raise Exception("Argument Error: argument must be a string")
		return (args[0][0][:int(args[1][0])], STRING)
	else:
		raise Exception("Argument Error: right takes 3 arguments")
def Find(args):
	if len(args) != 2:
		raise Exception("Argument Error: find takes 2 arguments")
	if args[0][1] != STRING or args[1][1] != STRING:
		raise Exception("Argument Error: argument must be a string")
	return (str(args[0][0].find(args[1][0])+1), INTEGER)
def Readf(args):
	global open_file
	if len(args) > 1:
		raise Exception("Argument Error: readf takes 0-1 arguments")
	if open_file == None:
		raise Exception("File Error: no file opened")
	if args[0][1] == None:
		return (open_file.read(), STRING)
	elif args[0][1] == INTEGER:
		return (open_file.read(int(args[0][0])), STRING)
	else:
		raise Exception("Argument Error: argument must be an integer")
def Readlinef(args):
	global open_file
	if len(args) > 1 or args[0][1] != None:
		raise Exception("Argument Error: readlinef takes 0 arguments")
	if open_file == None:
		raise Exception("File Error: no file opened")
	li = open_file.readline()
	if "\n" in li:
		li = li[:-1]
	return (li, STRING)
def Cursorf(args):
	global open_file
	if len(args) > 1 or args [0][1] != None:
		raise Exception("Argument Error: cursorf takes 0 arguments")
	if open_file == None:
		raise Exception("File Error: no file opened")
	return (str(open_file.tell())+1, INTEGER)

#	---Commands---

def Let(simplified, orig, tokenized):
	global data, arrays
	varname = tokenized[0][0]
	if tokenized[0][1] == VARIABLE:
		data[varname] = simplified[1]
	else:
		if varname[0] in arrays:
			arrays[varname[0]] = Set_Array(arrays[varname[0]], list(reversed(Interpret(varname[1])[0])), list(simplified[1]))
		else:
			raise Exception("Argument Error: array "+varname[0]+" not recognized")
def Input(simplified, orig, tokenized):
	global data
	varname = orig.split(",", 1)[0].strip()
	if '"' in varname:
		raise Exception("Argument Error: argument must be a variable name")
	if varname[0] in digits:
		raise Exception("Argument Error: variable name must not begin with a digit")
	if len(simplified) == 2:
		message = simplified[1][0]
	elif len(simplified) == 1:
		message = "?: "
	else:
		raise Exception("Syntax Error: Input takes 1-2 arguments")
	data[varname] = (raw_input(message), STRING)
def Print(simplified, orig, tokenized):
	for message in simplified:
		print message[0]
def Goto(simplified, orig, tokenized):
	global lines, linenum, labels
	if len(simplified) > 1:
		raise Exception("Argument Error: goto takes 1 argument")
	if tokenized[0][1] != VARIABLE:
		raise Exception("Argument Error: argument must be a label name")
	if not tokenized[0][0] in labels:
		for l in range(len(lines)):
			curline = str(lines[l])
			curline = curline.strip()+" "
			parts = curline.split(" ", 1)
			if parts[0] == "label":
				lastline = linenum
				linenum = l
				Run_Line(curline)
				linenum = lastline
	linenum = labels[tokenized[0][0]]
def Gosub(simplified, orig, tokenized):
	global lines, linenum, labels
	if len(simplified) > 1:
		raise Exception("Argument Error: gosub takes 1 argument")
	if tokenized[0][1] != VARIABLE:
		raise Exception("Argument Error: argument must be a label name")
	gosubs.append(linenum)
	if not tokenized[0][0] in labels:
		for l in range(len(lines)):
			curline = str(lines[l])
			curline = curline.strip()+" "
			parts = curline.split(" ", 1)
			if parts[0] == "label":
				lastline = linenum
				linenum = l
				Run_Line(curline)
				linenum = lastline
	linenum = labels[tokenized[0][0]]
def Return(simplified, orig, tokenized):
	global linenum
	linenum = gosubs.pop()
def If(simplified, orig, tokenized):
	global linenum, loops
	loops.append(["If", 0])
	if float(simplified[0][0]) != 1.0:
		count = 1
		while count != 0:
			Next_Line()
			comm = (lines[linenum].strip() + " ").split(" ",1)[0]
			if count == 1 and comm == "else":
				break
			if comm in looptypes:
				count += 1
			if lines[linenum].strip() == "end":
				count -= 1
		if comm == "end":
			Prev_Line()
def While(simplified, orig, tokenized):
	global linenum, loops
	if len(simplified) != 1:
		raise Exception("Argument Error: while takes 1 argument")
	if simplified[0][1] != INTEGER:
		raise Exception("Argument Error: argument must be an integer")
	if float(simplified[0][0]) == 1.0:
		loops.append(["While", orig, linenum])
	else:
		count = 1
		while count != 0:
			Next_Line()
			comm = (lines[linenum].strip() + " ").split(" ")[0]
			if comm in looptypes:
				count += 1
			if lines[linenum].strip() == "end":
				count -= 1
def Else(simplified, orig, tokenized):
	global linenum, lines
	while lines[linenum].strip() != "end":
		Next_Line()
	Prev_Line()
def Clear(simplified, orig, tokenized):
	print(chr(27)+"[2J")
def For(simplified, orig, tokenized):
	global loops, linenum
	if len(simplified) != 3:
		raise Exception("ArgumentError: command for takes exactly 3 arguments")
	else:
		varname = orig.split(",")[0].strip()
		if simplified[1][1] != INTEGER or simplified[2][1] != INTEGER:
			raise Exception("ArgumentError: argument must be an integer")
		else:
			start = int(simplified[1][0])
			end = int(simplified[2][0])-1
			data[varname] = (str(start), INTEGER)
			loops.append(["For", varname, end, linenum])
def End(simplified, orig, tokenized):
	global loops, linenum
	if len(loops) == 0:
		return
	loop = loops[-1]
	if loop[0] == "If":
		loops.pop()
		return
	elif loop[0] == "For":
		varval = int(data[loop[1]][0])
		if varval <= loop[2]:
			data[loop[1]]=(str(varval+1), INTEGER)
			linenum = loop[3]
		else:
			loops.pop()
		return
	elif loop[0] == "While":
		condition = Interpret(loop[1])[0][0]
		if condition != ("1", INTEGER) and condition != ("0", INTEGER):
			raise Exception("Argument Error: condition resulted in neither true nor false")
		if condition == ("1", INTEGER):
			linenum = loop[2]
		elif condition == ("0", INTEGER):
			loops.pop()
		return
def Dim(simplified, orig, tokenized):
	global data, arrays
	simplified.pop(0)
	varname = orig.split(",")[0]
	li = [None, None]
	for arg in simplified:
		if arg[1] == INTEGER:
			li = [li]*int(arg[0])
		else:
			raise Exception("Argument Error: argument must be an integer")
	arrays[varname] = li
def Screen(simplified, orig, tokenized):
	global screen
	if pygame == False:
		raise Exception("Screen Error: screen not available")
	if len(simplified) != 2:
		raise Exception("Argument Error: screen takes 2 arguments")
	if simplified[0][1] != INTEGER or simplified[1][1] != INTEGER:
		raise Exception("Argument Error: argument must be an integer")
	screen = pygame.display.set_mode((int(simplified[0][0]), int(simplified[1][0])))
def Title(simplified, orig, tokenized):
	global screen
	if screen == False:
		raise Exception("Screen Error: screen not initialized")
	if len(simplified) != 1:
		raise Exception("Argument Error: title takes 1 argument")
	if simplified[0][1] != STRING:
		raise Exception("Argument Error: arugment must be a string")
	pygame.display.set_caption(simplified[0][0])
def Keyrepeat(simplified, orig, tokenized):
	if len(simplified) != 1 and len(simplified) != 2:
		raise Exception("Argument Error: keyrepeat takes 0 or 2 arguments")
	if len(simplified) == 1:
		if simplified[0][1] != None:
			raise Exception("Argument Error: keyrepeat takes 0 or 2 arguments")
		pygame.key.set_repeat()
	else:
		if simplified[0][1] != INTEGER or simplified[1][1] != INTEGER:
			raise Exception("Argument Error: argument must be an integer")
		pygame.key.set_repeat(int(simplified[0][0]), int(simplified[1][0]))
def Fullscreen(simplified, orig, tokenized):
	global screen
	if len(simplified) != 1:
		raise Exception("Argument Error: fullscreen takes 1 argument")
	if simplified[0][1] != INTEGER:
		raise Exception("Argument Error: argument must be an integer")
	if simplified[0][0] == "1":
		screen = pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(screen.get_size())
def Color(simplified, orig, tokenized):
	global color
	if len(simplified) != 3:
		raise Exception("Arugment Error: color takes 3 arguments")
	if simplified[0][1] != INTEGER or simplified[1][1] != INTEGER or simplified[2][1] != INTEGER:
		raise Exception("Argument Error: arugment must be a string")
	color = (int(simplified[0][0]), int(simplified[1][0]), int(simplified[2][0]))
def Rect(simplified, orig, tokenized):
	global screen, color
	if len(simplified) != 4 and len(simplified) != 5:
		raise Exception("Arugment Error: rect takes 4-5 arguments")
	for s in simplified:
		if s[1] != INTEGER:
			raise Exception("Arugment Error: argument must be an integer")
	if len(simplified) == 4:
		width = 0
	else:
		width = int(simplified[4][0])
	if screen == False:
		raise Exception("Screen Error: screen not initialized")
	x1 = int(simplified[0][0])
	y1 = int(simplified[1][0])
	x2 = int(simplified[2][0])
	y2 = int(simplified[3][0])
	pygame.draw.rect(screen, color, (x1,y1,x2-x1,y2-y1), width)
def Line(simplified, orig, tokenized):
	global screen, color
	if len(simplified) != 4 and len(simplified) != 5:
		raise Exception("Arugment Error: line takes 4-5 arguments")
	for s in simplified:
		if s[1] != INTEGER:
			raise Exception("Arugment Error: argument must be an integer")
	if len(simplified) == 4:
		width = 1
	else:
		width = int(simplified[4][0])
	if screen == False:
		raise Exception("Screen Error: screen not initialized")
	x1 = int(simplified[0][0])
	y1 = int(simplified[1][0])
	x2 = int(simplified[2][0])
	y2 = int(simplified[3][0])
	pygame.draw.line(screen, color, (x1,y1), (x2,y2), width)
def Update(simplified, orig, tokenized):
	if screen == False:
		raise Exception("Screen Error: screen not initialized")
	pygame.display.flip()
def List(simplified, orig, tokenized):
	global lines
	start = 0
	ending = len(lines)
	if len(simplified) >= 1:
		if simplified[0][1] != None:
			if simplified[0][1] != INTEGER:
				raise Exception("Argument Error: argument must be an integer")
			start = int(simplified[0][0])
	if len(simplified) == 2:
		if simplified[1][1] != INTEGER:
			raise Exception("Argument Error: argument must be an integer")
		ending = int(simplified[1][0])+1
	elif len(simplified) > 2:
		raise Exception("Argument Error: list takes 0-2 arguments")
	for i in range(start, ending):
		try:
			if lines[i].strip() != "":
				print str(i)+" "+lines[i]
				time.sleep(0.1)
		except IndexError:
			break
def Insert(simplified, orig, tokenized):
	global lines
	if len(simplified) != 2:
		raise Exception("Argument Error: insert takes 2 arguments")
	if simplified[0][1] != INTEGER:
		raise Exception("Argument Error: argument must be an integer")
	line = int(simplified[0][0])
	statement = orig.split(",",1)[1].strip()
	lines.insert(line, statement)
def Openf(simplified, orig, tokenized):
	global open_file
	if simplified[0][1] == None or len(simplified) > 2:
		raise Exception("Argument Error: openf takes 1-2 arguments")
	mode = "r"
	if len(simplified) == 2:
		if simplified[1][1] == STRING:
			mode = simplified[1][0]
		else:
			raise Exception("Argument Error: argument must be a string")
	filename = simplified[0][0]
	if open_file != None:
		open_file.close()
	open_file = open(filename, mode)
def Closef(simplified, orig, tokenized):
	global open_file
	if len(simplified) != 1 or simplified[0][1] != None:
		raise Exception("Argument Error: closef takes 0 arguments")
	if open_file != None:
		open_file.close()
		open_file = None
def Seekf(simplified, orig, tokenized):
	global open_file
	if len(simplified) > 1 or simplified[0][1] == None:
		raise Exception("Argument Error: seek takes 1 argument")
	if simplified[0][1] != INTEGER:
		raise Exception("Argument Error: argument must be a string")
	if open_file == None:
		raise Exception("File Error: no file opened")
	open_file.seek(int(simplified[0][0])-1)
def Writef(simplified, orig, tokenized):
	global open_file
	if len(simplified) > 1 and simplified[0][1] == None:
		raise Exception("Argument Error: write takes 1 argument")
	if simplified[0][1] != STRING:
		raise Exception("Argument Error: argument must be a string")
	if open_file == None:
		raise Exception("File Error: no file opened")
	open_file.write(simplified[0][0])
def Replacef(simplified, orig, tokenized):
	global open_file
	if len(simplified) != 3:
		raise Exception("Argument Error: replacef takes 3 arguments")
	if simplified[0][1] != STRING:
		raise Exception("Argument Error: argument must be a string")
	if simplified[1][1] != INTEGER or simplified[1][1] != INTEGER:
		raise Exception("Argument Error: argument must be an integer")
	if open_file == None:
		raise Exception("File Error: no file opened")
	cursor = open_file.tell()
	name = open_file.name
	open_file.close()
	open_file = open(name)
	contents = open_file.read()
	open_file.close()
	left = contents[:int(simplified[1][0])-1]
	right = contents[int(simplified[2][0]):]
	open_file = open(name, "w")
	open_file.write(left+simplified[0][0]+right)
	open_file.close()
	open_file = open(name, "r+")
	open_file.seek(cursor)
def Label(simplified, orig, tokenized):
	global labels, linenum
	if len(simplified) > 1:
		raise Exception("Argument Error: label takees 1 argument")
	if tokenized[0][1] != VARIABLE:
		raise Exception("Argument Error: argument must be a label name")
	labels[tokenized[0][0]] = linenum
#	---Array Operations---

def Get_Array(varname, simplified):
	li = arrays[varname]
	for arg in reversed(simplified):
		if arg[1] == INTEGER:
			try:
				li = li[int(arg[0])]
			except:
				raise Exception("Argument Error: invalid array indicies")
		else:
			raise Exception("Argument Error: argument must be an integer")
	return li
def Set_Array(li, args, value):
	if len(args) != 0:
		index = int(args.pop(0)[0])
		try:
			li[index] = Set_Array(list(li[index]), args, value)
		except:
			raise Exception("Argument Error: invalid array indicies")
	else:
		return value
	return li

#	---Global Dictionary Definitions---

functions = {"nothing": Nothing, "str": Str, "float": Float, "not":Not, "sqrt":Sqrt, "rand":Rand, "randint":Randint, "int":Int, "exp":Exp, "log":Log, "sin":Sin, "cos":Cos, "tan":Tan, "eval":Eval, "mousex":Mousex, "mousey":Mousey, "mousedx":Mousedx, "mousedy":Mousedy, "winexit":Winexit, "clickx":Clickx, "clicky":Clicky, "keypress":Keypress, "chr":Chr, "len":Len, "mid":Mid, "left":Left, "right":Right, "find":Find, "readf":Readf, "readlinef":Readlinef, "cursorf":Cursorf}
commands = {"let": Let, "input": Input, "print":Print, "goto":Goto, "gosub":Gosub, "return":Return, "if":If, "else":Else, "clear":Clear, "for":For, "while":While, "end":End, "dim":Dim, "screen":Screen, "title":Title, "color":Color, "rect":Rect, "update":Update, "line": Line, "list":List, "insert":Insert, "openf":Openf, "closef":Closef, "seekf":Seekf, "writef":Writef, "replacef":Replacef, "label":Label, "keyrepeat":Keyrepeat, "fullscreen":Fullscreen}

#	---Global Variable Definitions---

data = {"PI":("3.1415927", FLOAT), "E":("2.718281828"), "VERSION":("Ben-BASIC 1.5", STRING)}
arrays = {}
lines = []
linenumbers = []
highest = 0

#	---Tokens Class---

class Tokens():
	def __init__(self, string, variables):
		self.string = string
		self.variables = variables
		self.tokens =  []
		self.char = 0
	def NextCharacter(self):
		try:
			out = self.string[self.char]
		except:
			return "EOL"
		self.char+=1
		return out
	def PreviousCharacter(self):
		if self.char == 0:
			return "BOL"
		else:
			self.char -= 1
			return self.string[self.char]
	def Tokenize(self):
		char = ""
		while char != "EOL":
			token = ""
			char = self.NextCharacter()
			if char in digits:
				while char in digits or char == ".":
					token += char
					char = self.NextCharacter()
				self.PreviousCharacter()
				if "." in token:
					self.tokens.append((token, FLOAT))
				else:
					self.tokens.append((token, INTEGER))
				token = ""
			elif char == "+":
				self.tokens.append(("+", ADD))
			elif char == "-":
				try:
					prev = self.tokens[-1][1]
				except:
					prev = "BOL"
				if (prev != FLOAT and prev != INTEGER and prev != VARIABLE and prev != FUNCTION and prev != PARENTHESES ):
					ch = self.NextCharacter()
					if ch in alphabet:
						st = "-1*"
						count = 0
						while ch in alphabet or count != 0:
							st += ch
							ch = self.NextCharacter()
							if ch == "(":
								count += 1
							elif ch == ")":
								count -= 1
						if ch != ")":
							self.PreviousCharacter()
						else:
							st += ")"
						self.tokens.append((st, PARENTHESES))
					elif ch in digits:
						st = "-"
						while ch in digits or ch == ".":
							st += ch
							ch = self.NextCharacter()
						self.PreviousCharacter()
						self.tokens.append((st, FLOAT))
					elif ch == "(":
						st = "-1*"
						count = 1
						while count != 0:
							st += ch
							ch = self.NextCharacter()
							if ch == "(":
								count += 1
							elif ch == ")":
								count -= 1
						self.tokens.append((st+")", PARENTHESES))
				else:
					self.tokens.append(("-", SUBTRACT))
			elif char == "*":
				self.tokens.append(("*", MULTIPLY))
			elif char == "/":
				self.tokens.append(("/", DIVIDE))
			elif char == '"':
				c = self.NextCharacter()
				st = ""
				while c != '"' and c != "EOL":
					st+=c
					c = self.NextCharacter()
				st = st.decode("string_escape")
				self.tokens.append((st, STRING))
			elif char == "'":
				c = self.NextCharacter()
				st = ""
				while c != "'" and c != "EOL":
					st+=c
					c = self.NextCharacter()
					st = st.decode("string_escape")
				self.tokens.append((st, STRING))
			elif char == "(":
				c = self.NextCharacter()
				count = 1
				st = ""
				while count != 0 and c != "EOL":
					st+=c
					if c == "(":
						count += 1
					elif c == ")":
						count -= 1
					c = self.NextCharacter()
				self.tokens.append((st[:-1], PARENTHESES))
				self.PreviousCharacter()
			elif char in alphabet:
				func = char
				c = self.NextCharacter()
				while c != "(" and (not c in whitespace) and (not c in operations) and c!="EOL" and c != "," and not c in comparison:
					func+=c
					c = self.NextCharacter()
				if c == "(":
					c = self.NextCharacter()
					count = 1
					st = ""
					while count != 0 and c != "EOL":
						st+=c
						if c == "(":
							count += 1
						elif c == ")":
							count -= 1
						c = self.NextCharacter()
					self.tokens.append(((func, st[:-1]), FUNCTION))
					self.PreviousCharacter()
				elif (c in whitespace) or (c in operations) or c=="EOL" or c=="," or c in comparison:
					self.PreviousCharacter()
					self.tokens.append((func, VARIABLE))
				if c == "EOL":
					self.NextCharacter()
			elif char in comparison:
				if char != "!":
					self.tokens.append((char, COMPARISON))
				else:
					self.tokens.append(("!=", COMPARISON))
					self.NextCharacter()
			elif char in seperators:
				self.tokens.append((char, SEPERATOR))
			elif char in whitespace:
				pass
			else:
				self.tokens.append((char, -1))

#	--Interpret Function---

def Interpret(string):
	global data, functions, arrays, screen
	t = Tokens(string, [])
	t.Tokenize()
	ans = None
	operation = None
	output = []
	anstype = None
	tokenized = list(t.tokens)
	for token in range(len(t.tokens)):
		if t.tokens[token][1] == FUNCTION:
			if t.tokens[token][0][0] in functions:
				out = functions[t.tokens[token][0][0]](Interpret(t.tokens[token][0][1])[0])
				t.tokens[token] = (out[0], out[1])
			elif t.tokens[token][0][0] in arrays:
				out = Get_Array(t.tokens[token][0][0], Interpret(t.tokens[token][0][1])[0])
				t.tokens[token] = out
	for token in range(len(t.tokens)):
		if t.tokens[token][1] == PARENTHESES:
			out = Interpret(t.tokens[token][0])[0][0]
			t.tokens[token] = out
	for token in range(len(t.tokens)):
		if t.tokens[token][1] == VARIABLE:
			if t.tokens[token][0] in data:
				t.tokens[token] = data[t.tokens[token][0]]
	for token in range(len(t.tokens)):
		if t.tokens[token][1] == ADD:
			operation = ADD
		elif t.tokens[token][1] == SUBTRACT:
			operation = SUBTRACT
		elif t.tokens[token][1] == MULTIPLY:
			operation = MULTIPLY
		elif t.tokens[token][1] == DIVIDE:
			operation = DIVIDE
		elif t.tokens[token][0] == "=" and t.tokens[token][1] == COMPARISON:
			operation = "="
		elif t.tokens[token][0] == "!=" and t.tokens[token][1] == COMPARISON:
			operation = "!="
		elif t.tokens[token][0] == "<" and t.tokens[token][1] == COMPARISON:
			operation = "<"
		elif t.tokens[token][0] == ">" and t.tokens[token][1] == COMPARISON:
			operation = ">"
		elif t.tokens[token] == ("or", VARIABLE):
			operation = "or"
		elif t.tokens[token] == ("and", VARIABLE):
			operation = "and"
		elif t.tokens[token][1] == INTEGER or t.tokens[token][1] == FLOAT:
			if ans == None:
				ans = float(t.tokens[token][0])
			if anstype == None:
				anstype = FLOAT
			if operation == ADD:
				ans += float(t.tokens[token][0])
			elif operation == SUBTRACT:
				ans -= float(t.tokens[token][0])
			elif operation == MULTIPLY:
				ans *= float(t.tokens[token][0])
			elif operation == DIVIDE:
				ans /= float(t.tokens[token][0])
		if operation == "=":
			if t.tokens[token+1][1] == anstype or (t.tokens[token+1][1] == INTEGER and anstype == FLOAT) or (t.tokens[token+1][1] == FLOAT and anstype == INTEGER):
				if anstype == STRING:
					if t.tokens[token+1][0] == ans:
						ans = 1.0
					else:
						ans = 0.0
				else:
					if float(t.tokens[token+1][0]) == ans:
						ans = 1.0
					else:
						ans = 0.0
			else:
				ans = 0.0
			anstype = FLOAT
			operation = None
		elif operation == "!=":
			if t.tokens[token+1][1] == anstype or (t.tokens[token+1][1] == INTEGER and anstype == FLOAT) or (t.tokens[token+1][1] == FLOAT and anstype == INTEGER):
				if anstype == STRING:
					if t.tokens[token+1][0] == ans:
						ans = 0.0
					else:
						ans = 1.0
				else:
					if float(t.tokens[token+1][0]) == ans:
						ans = 0.0
					else:
						ans = 1.0
			else:
				ans = 1.0
			anstype = FLOAT
			operation = None
		elif operation == "<":
			if (t.tokens[token+1][1] == INTEGER or t.tokens[token+1][1] == FLOAT) and (anstype == INTEGER or anstype == FLOAT):
				if float(t.tokens[token+1][0]) > ans:
					ans = 1.0
				else:
					ans = 0.0
			anstype = FLOAT
			operation = None
		elif operation == ">":
			if (t.tokens[token+1][1] == INTEGER or t.tokens[token+1][1] == FLOAT) and (anstype == INTEGER or anstype == FLOAT):
				if float(t.tokens[token+1][0]) < ans:
					ans = 1.0
				else:
					ans = 0.0
			anstype = FLOAT
			operation = None
		elif operation == "or":
			if anstype == FLOAT and (t.tokens[token+1][1] == INTEGER or t.tokens[token+1][1] == FLOAT):
				if float(t.tokens[token+1][0]) == 1.0 or ans == 1.0:
					ans = 1.0
				else:
					ans = 0.0
			else:
				ans = 0.0
			operation = None
		elif operation == "and":
			if anstype == FLOAT and (t.tokens[token+1][1] == INTEGER or t.tokens[token+1][1] == FLOAT):
				if float(t.tokens[token+1][0]) == 1.0 and ans == 1.0:
					ans = 1.0
				else:
					ans = 0.0
			else:
				ans = 0.0
			operation = None
		elif t.tokens[token][1] == STRING:
			if ans == None:
				ans = t.tokens[token][0]
			if anstype == None:
				anstype = STRING
			if operation == ADD:
				ans += t.tokens[token][0]
		elif t.tokens[token][1] == SEPERATOR:
			try:
				if ans - int(ans)==0 or ans == 0:
					anstype = INTEGER
					ans = int(ans)
			except:
				pass
			output.append((str(ans), anstype))
			ans = None
			anstype = None
			operation = None
	try:
		if ans - int(float(ans))==0 or ans == 0:
			anstype = INTEGER
			ans = int(ans)
	except:
		pass
	output.append((str(ans), anstype))

	return output,tokenized

#	---Window Functions---
def WindowEvents():
	global click, keys, exit
	if screen != False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = [event.pos[0], event.pos[1]]
			elif event.type == pygame.KEYDOWN:
				keys.append(event.key)
				keys = keys[-5:]
	elif screen == False and exit == True:
		exit = False

#	---Code Running Functions---

def Run_Line(line):
	global lines, highest
	line += " "
	parts = line.split(" ", 1)
	if line.strip() == "run":
		Run_File()
		return
	if line.strip() == "delete":
		lines = []
	if parts[0] in commands:
		try:
			simplified,tokenized = Interpret(parts[1])
			commands[parts[0]](simplified, parts[1], tokenized)
		except Exception as e:
			print str(linenum+1)+" "+line
			print e
			return True
	elif parts[0][0] in digits:
		if int(parts[0]) <= highest:
			lines[int(parts[0])] = parts[1]
		else:
			lines.extend([""]*(int(parts[0])-highest+1))
			lines[int(parts[0])] = parts[1]
	WindowEvents()
	#print arrays

def Run_File(file = None):
	global linenum, lines, highest, open_file, pygame
	if file != None:
		f = open(file, "r")
		lines = f.readlines()
		f.close()
	linenum = 0
	err = None
	while (linenum < len(lines) or (type(lines) == dict and linenum <= highest)) and err != True:
		if type(lines) == dict and linenum not in lines:
			while linenum not in lines:
				linenum+=1
		if lines[linenum].strip() != "":
			err = Run_Line(lines[linenum].strip().replace("\n","")+" ")
		linenum+=1
	if pygame != False:
		pygame.quit()
	if open_file != None:
		open_file.close()

def Command_Line():
	global lines
	while True:
		inp = raw_input(">>> ")
		if inp == "end":
			if pygame != False:
				pygame.quit()
			return
		if inp == "delete":
			lines = []
		else:
			try:
				Run_Line(inp)
			except Exception as e:
				print(e)
#	---Line Operations---

def Next_Line():
	global linenum, lines
	if type(lines) == dict:
		while linenum not in lines and linenum <= highest:
			linenum += 1
	else:
		linenum+=1

def Prev_Line():
	global linenum, lines
	if type(lines) == dict:
		while linenum not in lines and linenum > 0:
			linenum -= 1
	else:
		linenum -= 1

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("1) Command Line")
		print("2) Run File")

		i = raw_input("Enter option (1 or 2): ")

		if i == "1":
			Command_Line()
		elif i == "2":
			Run_File(raw_input("enter file name: "))
	elif len(sys.argv) == 2:
		Run_File(sys.argv[1])
