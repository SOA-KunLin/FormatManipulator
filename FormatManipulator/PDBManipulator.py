# PDBManipulator

# Usage:
#	import sys
#	sys.path.append("/Directory/where/PDBManipulator.py/put/in")
#	from PDBManipulator import *
#  Or:
#	export PYTHONPATH=$PYTHONPATH:/Directory/where/PDBManipulator.py/put/in

###############################################################################

def readFile(filename):
    #===> Just read only.
    # return: a list of all lines of length 80 and without newline 
    #         in the input file

    f = open(filename)

    fileText = f.readlines()
    fileText = [line.strip() for line in fileText]
    fileText = [line + ' '*(80-len(line)) for line in fileText]

    f.close()

    return fileText



def selectLine(fileText, selectionString, selectedLinesID=[]):
    # return: a list of line ID which the lines pointed by fulfill the "selectionString"
    
    if selectedLinesID == []:
        selectedLinesID = range(0,len(fileText) )
    
    selectionList = selectionStringParser(selectionString)
    for i in range(0,len(selectionList)):
        selectedLinesID = selectKeyword(fileText, selectionList[i][0], \
                                                  selectionList[i][1], \
                                                  selectionList[i][2], \
                                                  selectedLinesID )

    return selectedLinesID


def extract(pdbText,index,position_range):
    # pdbText: fileText
    # index: selectedLinesID
    extract=[]
    list_position_range = position_range.split('-')
    if len(list_position_range)!=1:
        initial_position = int(list_position_range[0])-1
        final_position = int(list_position_range[1])
    else:
        initial_position = int(list_position_range[0])-1
        final_position = initial_position+1
    
    for i in range(0,len(index)):
        j=index[i]
        extract.append(pdbText[j][initial_position:final_position])
    
    return extract

def replace(pdbText,index,command,source):
	# pdbText: fileText
    # index: selectedLinesID
    command_list=command.split('-')
    if len(command_list)!=1:
        initial_position = int(command_list[0])-1
        final_position = int(command_list[1])
    else:
        initial_position = int(command_list[0])-1
        final_position = initial_position+1
    
    for i in range(0,len(index)):      
        
        pdbText[index[i]]=pdbText[index[i]][0:initial_position] + source[i] + pdbText[index[i]][final_position:]
    return pdbText

def replace_old(pdbText,index,extract,source):
    # pdbText: fileText
    # index: selectedLinesID
    if len(extract) != len(source):
        print 'The size between extration and source is not the same'
    for i in range(0,len(extract)):
        if len(extract[i])!=len(source[i]):
            print 'The size between extration and source is not the same,','Error number:',i+1
        
        pdbText[index[i]]= pdbText[index[i]].replace(extract[i],source[i])
        
            
    return pdbText


def insertion(pdbText,index,insertional_list,add_direction='down',position=0):
    length1 = -len(insertional_list)
    initial_pdbText=pdbText	
    if add_direction == 'down':
        position+=1 
    elif add_direction == 'up':
        position = -position
        
        
    
    
    for i in range(0,len(index)):
        length1+=len(insertional_list)
        for j in range(0,len(insertional_list)):
            pdbText.insert(index[i]+length1+j+position,insertional_list[j])
    
    modified_pdbText=pdbText
    pdbText=initial_pdbText		
        
    return modified_pdbText


def writeFile(OUTPUT, filename):
    f = open(filename,'w')
    
    OUTPUT = [line+'\n' for line in OUTPUT]
    f.writelines(OUTPUT)
    
    f.close()
        



################################# private #####################################
def selectionStringParser(command):       
    # instruction: The function accepts multiple selection criterions 
    #     that are all in a string seperated by ",".
    # return: A list of lists which are [initial_position,final_position,key],
    #     column ID(initial_position,final_position) are same as that you see
    #     in a text editor (+1 or -1 are not needed when entry).
    
    criterions = command.split(',')
    total_list=[]
    for criteria in criterions:
        equal_position=criteria.find('=')
        pos = criteria[0:equal_position].strip()
        key = criteria[equal_position+1:].strip()
        if pos.find('-')==-1:  # if only one column selected
            initial_position=int(pos[0:equal_position])-1
            final_position=initial_position+1            
        else:  # if multiple columns selected by using "-"
            dash_position=pos.find('-')
            initial_position=int(pos[0:dash_position])-1
            final_position=int(pos[dash_position+1:equal_position])
        if final_position-initial_position < len(key):
            # check column lenth longer than key
            print 'number:',i+1,'warning'
            
        total_list.append([initial_position,final_position,key])
        
    
    return total_list



def selectKeyword(pdbText,initial_position,final_position,key, index):
    # initial_postion should get from "column position" minus 1,
    # final_postion do not need change.
    b=[]

    for i in range(0,len(index)):
        j=index[i]
        
        e=pdbText[j][initial_position:final_position].strip()
        b.append(e)
    r=index
    index=[]
    for i in range(0,len(r)):
        if b[i]==key:
            k=r[i]
            index.append(k)
            
            
    return index



	

def extractColumnsOfPDBText(pdbText, selectedLineID, ColIDPairsList=[], CLEAR=True, odtype='str', DSV=0, DSV_Delimiter='-1', DSV_Column=-1):
	# pdbText:
	# selectedLineID: A list (list one or multiple(s) selected line IDs).
	# ColIDsPairsList: A list of lists which containing two elements that are the IDs of columns where selection started and ended, ex: [[StartColID1, EndColID1], [StartColID2, EndColID2]]. ColID starts from 1.
	# CLEAR: String is striped
	# odtype: Output data type
	
	if DSV == 0:
		try:
			for ColIDPair in ColIDPairsList:
				ColIDPair[0] = ColIDPair[0] - 1
		
			selectedTextColumn = []
			for lineID in selectedLineID:
				selectedLine = pdbText[lineID]
				selectedLineColumn = []
				for ColIDPair in ColIDPairsList:
					selectedLineColumn.append(selectedLine[ColIDPair[0]:ColIDPair[1]])
				selectedTextColumn.append(selectedLineColumn)
			
			if CLEAR:
				for Columns in selectedTextColumn:
					for i, ele in enumerate(Columns):
						Columns[i] = ele.strip()
						
			if odtype == 'str':
				pass
			elif odtype == 'int':
				for Columns in selectedTextColumn:
					for i, ele in enumerate(Columns):
						Columns[i] = int(ele)
			elif odtype == 'float':
				for Columns in selectedTextColumn:
					for i, ele in enumerate(Columns):
						Columns[i] = float(ele)
			
				
			return selectedTextColumn
				
		except:
			print('########### ERROR!! Some errors happened in "def extractColumnsOfPDBText(pdbText, RECORDNAME, selectedLineID, COLUMNNAME):"')
	
	elif DSV == 1:
		# DSV: enable DSV parser, 1 is open, 0 is close.
		# DSV_Delimiter: delimiter used to split strings.
		# DSV_Column: index of column after delimiter split, starts from 0.
		# Return:
		#	DSV_selectedColumn: words in the selected column.
		
		DSV_selectedColumn = []
		forList = selectedLineID[:]
		for lineID in forList:
			splist = pdbText[lineID].strip().split(DSV_Delimiter)
			DSV_selectedColumn.append(splist[DSV_Column])
		
		return DSV_selectedColumn
		
	
	
def replacePDBText(pdbText, selectedLineID, withELEMENT='=1', COLUMNNAME='', ColIDPairsList=[], DSV=0, DSV_Delimiter='-1', DSV_Column=-1, DSV_Word=''):
	# pdbText:
	# selectedLineID: A list (list one or multiple(s) selected line IDs).
	# withELEMENT: One value (number or string).
	# COLUMNNAME: B-VALUE, ATOMNO, ColIDPairs
	# ColIDPairsList: optional, activated when COLUMNNAME=ColIDPairs. A list of lists which containing two elements that are the IDs of columns where selection started and ended, ex: [[StartColID1, EndColID1], [StartColID2, EndColID2]]. ColID starts from 1.
	
	COLUMNNAME = COLUMNNAME.strip()
	if COLUMNNAME == 'B-VALUE':
		try:
			withELEMENT = float(withELEMENT)
			withELEMENT = '%6.2f' % (withELEMENT)
			for lineID in selectedLineID:
				pdbText[lineID] = pdbText[lineID][0:60] + withELEMENT + pdbText[lineID][66:]
	
			return pdbText
		except:
			print('########### ERROR!! "withELEMENT" should be a number when "COLUMNNAME" is "B-VALUE"')   
			
	elif COLUMNNAME == 'ATOMNO':
		try:
			withELEMENT = int(withELEMENT)
			withELEMENT = '%5d' % withELEMENT
			for lineID in selectedLineID:
				pdbText[lineID] = pdbText[lineID][ColIDPair[0]:ColIDPair[1]] + withELEMENT + pdbText[lineID][11:]
			
			return pdbText 
		except:
			print('########### ERROR!!')
	
	elif COLUMNNAME == 'ColIDPairs':
		try:
			withELEMENT = str(withELEMENT)
			for ColIDPair in ColIDPairsList:
				ColIDPair[0] = ColIDPair[0] - 1
				
			for lineID in selectedLineID:
				pdbText[lineID] = pdbText[lineID][0:ColIDPair[0]] + withELEMENT + pdbText[lineID][ColIDPair[1]:]
			
			return pdbText 
		except:
			print('########### ERROR!!')
			
	elif DSV == 1:
		# DSV: enable DSV parser, 1 is open, 0 is close.
		# DSV_Delimiter: delimiter used to split strings.
		# DSV_Column: index of column after delimiter split, starts from 0.
		# DSV_Word: word to replace the selected column.
		forList = selectedLineID[:]
		for lineID in forList:
			splist = pdbText[lineID].strip().split(DSV_Delimiter)
			splist[DSV_Column] = DSV_Word
			pdbText[lineID] = " ".join(splist)


			
def addPDBText(pdbText, withELEMENT, selectedLineID):
	# pdbText:
	# withELEMENT: A list (list one or multiple(s) added lines). Format of lines should meet the requirements of "PDB Format".
	# selectedLineID: A list (list one or multiple(s) selected line IDs before which "withELEMENT" is added).
	#
	# Key Words of "withELEMENT": 'TER', 'END', 'MODEL', 'ENDMDL'
	withELEMENT_FORMAT = {  'TER': ['TER   ' + ' '*(80-len('TER   '))],
							'END': ['END   ' + ' '*(80-len('END   '))],
							'MODEL': ['MODEL ' + ' '*4 + '%4d' + ' '*(80-len('MODEL ')-8)],
							'ENDMDL': ['ENDMDL' + ' '*(80-len('ENDMDL'))]
						 }
	if withELEMENT == 'TER' :
		withELEMENT = withELEMENT_FORMAT['TER']
	else:
		withELEMENT
	
	withELEMENT.reverse()
	selectedLineID.sort()
	while len(selectedLineID) != 0:
		lineID = selectedLineID.pop()
		for ELEMENT in withELEMENT:
			pdbText.insert(lineID, ELEMENT)
	
	# readNMR(pdbText)
	
	return pdbText
	
	# def lastMODELNO():
	
	
def writePDB(OUTPUT, output_filename):
	f_pdb = open(output_filename,'w')
	
	OUTPUT = [line+'\n' for line in OUTPUT]
	f_pdb.writelines(OUTPUT)
	
	f_pdb.close()
		
		
def readTxt(text_filename):
	# Just read.
	f_text = open(text_filename)

	textText = f_text.readlines()
	textText = [line.strip() for line in textText]
	
	f_text.close()
	
	return textText
