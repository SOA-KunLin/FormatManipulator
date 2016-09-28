# PDBformatManager

# Usage:
#	import sys
#	sys.path.append("/Directory/where/MyCode.py/put/in")
#	from MyCode import *
#  Or:
#	export PYTHONPATH=$PYTHONPATH:/Directory/where/MyCode.py/put/in

def readPDB(pdb_filename):
	#===> Just only read.
	f_pdb = open(pdb_filename)

	pdbText = f_pdb.readlines()
	pdbText = [line.strip() for line in pdbText]
	pdbText = [line + ' '*(80-len(line)) for line in pdbText]
	
	f_pdb.close()
	
	# readNMR(pdbText):
	
	return pdbText
	
# def readNMR(pdbText):
		# Return two dict with "ModelID" as keys and "selectedLineID" as keys seperately.
	
	
def selectPDBText(pdbText, RECORDNAME='', CHAIN='', RESIDUENO='', ATOMNAME='', DSV=0, DSV_Delimiter='-1', DSV_Column=-1, DSV_Word=''):
	selectedLineID = range(len(pdbText))
	
	# if len(MODEL) != 0:
	
	if len(RECORDNAME) != 0:
		RECORDNAME = RECORDNAME.strip()
		# try : whether RECORDNAME in RECORDNAME dict
		RECORDNAME = RECORDNAME + ' '*(6-len(RECORDNAME))
		forList = selectedLineID[:]
		for lineID in forList:
			if pdbText[lineID][0:6] != RECORDNAME:
				selectedLineID.remove(lineID)
	
	if len(CHAIN) != 0:
		CHAIN = CHAIN.strip()
		CHAIN = CHAIN + ' '*(1-len(CHAIN))
		forList = selectedLineID[:]
		for lineID in forList:
			if pdbText[lineID][21] != CHAIN:
				selectedLineID.remove(lineID)
	
	if len(RESIDUENO) != 0:
		RESIDUENO = RESIDUENO.strip()
		RESIDUENO = ' '*(4-len(RESIDUENO)) + RESIDUENO
		forList = selectedLineID[:]
		for lineID in forList:
			if pdbText[lineID][22:26] != RESIDUENO:
				selectedLineID.remove(lineID)
	
	if len(ATOMNAME) != 0:
		ATOMNAME_Format = { 'N': ' N  ',
							'CA': ' CA ',
							'C': ' C  ',
							'O': ' O  '
						  }
		ATOMNAME = ATOMNAME.strip()
		ATOMNAME = ATOMNAME_Format[ATOMNAME]
		forList = selectedLineID[:]
		for lineID in forList:
			if pdbText[lineID][12:16] != ATOMNAME:
				selectedLineID.remove(lineID)
				
	if DSV == 1:
		#DSV=0, DSV_Delimiter='-1', DSV_Column=-1, DSV_Word=''
		# DSV_Column: index starts from 0
		forList = selectedLineID[:]
		for lineID in forList:
			splist = pdbText[lineID].strip().split(DSV_Delimiter)
			if splist[DSV_Column] != DSV_Word:
				selectedLineID.remove(lineID)
	
	
	return selectedLineID

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
