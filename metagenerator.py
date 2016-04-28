def declarations(declaration):
	if len(declaration[2][0]) > 1:
		string = '%s _%s[%s];\n' %(
			declaration[3][0],
			declaration[0],
			']['.join([
				str(int(ranges[2]) - int(ranges[1]) + 1)
					for ranges in declaration[2]
						if len(ranges) > 1
			])
		)
		string += '%s __%s(void) {\n' %(
			declaration[3][0],
			declaration[0]
		)
		count = 1
		for nested in range(len(declaration[2])):
			if len(declaration[2][nested]) > 1:
				string += '%sfor(int %s = 0; %s < %s; ++%s)\n' %(
					'\t' + '\t' * nested,
					declaration[1][nested],
					declaration[1][nested],
					str(int(declaration[2][nested][2]) - int(declaration[2][nested][1]) + 1),
					declaration[1][nested]
				)
				count += 1
		string += '%s_%s[%s] = %s;\n\treturn %s;\n}\n%s ___%s = __%s();\n' %(
			'\t' * count,
			declaration[0],
			']['.join([
				datatypes
					for datatypes, ranges in zip(declaration[1], declaration[2])
						if len(ranges) > 1
			]),
			declaration[3][1],
			declaration[3][1],
			declaration[3][0],
			declaration[0],
			declaration[0]
		)
		string += '%s %s(%s) {\n\tif(_%s[%s] != %s)\n\t\treturn _%s[%s];\n' %(
			declaration[3][0],
			declaration[0],
			', '.join([
				ranges[0] + ' ' + datatypes
					for ranges, datatypes in zip(declaration[2], declaration[1])
			]),
			declaration[0],
			']['.join([
				datatypes
					for datatypes, ranges in zip(declaration[1], declaration[2])
						if len(ranges) > 1
			]),
			declaration[3][1],
			declaration[0],
			']['.join([
				datatypes
					for datatypes, ranges in zip(declaration[1], declaration[2])
						if len(ranges) > 1
			])
		)
	else:
		string = '%s %s(%s) {\n' %(
			declaration[3][0],
			declaration[0],
			','.join([
				ranges[0] + ' ' + datatypes
					for ranges, datatypes in zip(declaration[2], declaration[1])
			])
		)
	return string

def definitions(definition, declaration):
	if len(declaration[2][0]) > 1:
		string = '_%s[%s] = %s;\nreturn _%s[%s];\n' %(
			declaration[0],
			']['.join([
				datatypes
					for datatypes, ranges in zip(declaration[1], declaration[2])
						if len(ranges) > 1
			]),
			definition[0].strip(),
			declaration[0],
			']['.join([
				datatypes
					for datatypes, ranges in zip(declaration[1], declaration[2])
						if len(ranges) > 1
			])
		)
	else:
		string = 'return %s;\n' %(definition[0].strip())
	return string

def iterations(iteration):
	string = 'for(int %s = %s; %s %s %s; %s %s= %s) {\n' %(
		iteration[0],
		iteration[1].strip(),
		iteration[0],
		'<=' if iteration[3] == '+' else '>=',
		iteration[2].strip(),
		iteration[0],
		iteration[3],
		'1' if len(iteration) == 4 else iteration[4]
	)
	return string

def inquisitions(inquisition):
	string = 'if(%s) {\n' %(
		inquisition[0]
	)
	return string

def statements(statement):
	string = '%s;\n' %(';\n'.join([line.strip() for line in statement[0].split(';') if line.strip()]))
	return string

def blanks(blank):
	string = '}\n'
	return string

def programs(program):
	scope = list()
	metaprogram = str()
	declaration = None
	for line in program:
		if line[0][0] == 'blanks':
			while scope:
				scope.pop()
				metaprogram += '\t' * len(scope) + '\t' + blanks(None)
			metaprogram += '\t' * len(scope) + blanks(None)
			declaration = None
			continue
		i = 0
		while i < len(scope) and i < len(line):
			if scope[i] != line[i]:
				break
			i += 1
		for j in range(i, len(scope)):
			scope.pop()
			metaprogram += '\t' * len(scope) + '\t' + blanks(None)
		for j in range(i, len(line)):
			if line[j][0] == 'declarations':
				metaprogram += declarations(line[j][2])
				declaration = line[j][2]
			if line[j][0] == 'definitions':
				metaprogram += ('\n').join(['\t' * len(scope) + '\t' + string for string in definitions(line[j][2], declaration).split('\n') if string]) + '\n'
			if line[j][0] == 'iterations':
				scope.append(line[j])
				metaprogram += '\t' * len(scope) + iterations(line[j][2])
			if line[j][0] == 'statements':
				if j == len(line) - 1:
					metaprogram += '\t' * len(scope) + '\t' + statements(line[j][2])
				else:
					scope.append(line[j])
					metaprogram += '\t' * len(scope) + inquisitions(line[j][2])
	return metaprogram
