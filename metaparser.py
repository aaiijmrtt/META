import pyparsing

identifiers = pyparsing.Word(
	pyparsing.alphanums
)

integers = pyparsing.Combine(
	pyparsing.And([
		pyparsing.Optional(
			pyparsing.Or([
				pyparsing.Literal('+'),
				pyparsing.Literal('-')
			])
		),
		pyparsing.Word(
			pyparsing.nums
		)
	])
)

datatypes = pyparsing.Combine(
	pyparsing.And([
		pyparsing.Or([
			pyparsing.Literal('char'),
			pyparsing.Literal('int'),
			pyparsing.Literal('long'),
			pyparsing.Literal('double')
		]),
		pyparsing.ZeroOrMore(
			pyparsing.Literal('*')
		)
	])
)

domains = pyparsing.Group(
	pyparsing.And([
		datatypes,
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal('[').suppress(),
				pyparsing.Or([
					integers,
					identifiers
				]),
				pyparsing.ZeroOrMore(
					pyparsing.And([
						pyparsing.Literal(',').suppress(),
						pyparsing.Or([
							integers,
							identifiers
					])
					])
				),
				pyparsing.Literal(']').suppress()
			])
		)
	])
)

ranges = pyparsing.Group(
	pyparsing.And([
		datatypes,
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal('[').suppress(),
				integers,
				pyparsing.Literal(']').suppress(),
			])
		)
	])
)

statements = pyparsing.CharsNotIn('').setResultsName('statements')
expressions = pyparsing.CharsNotIn(',')#.setResultsName('expressions')

iterations = pyparsing.And([
	identifiers,
	pyparsing.Literal('[').suppress(),
	expressions,
	pyparsing.Literal(',').suppress(),
	expressions,
	pyparsing.Literal(',').suppress(),
	pyparsing.And([
		pyparsing.Or([
			pyparsing.Literal('+'),
			pyparsing.Literal('-')
		]),
		pyparsing.Optional(
			pyparsing.Or([
				integers,
				identifiers
			])
		)
	]),
	pyparsing.Literal(']').suppress()
]).setResultsName('iterations')

declarations = pyparsing.And([
	identifiers,
	pyparsing.Literal('(').suppress(),
	pyparsing.Group(
		pyparsing.And([
			identifiers,
			pyparsing.ZeroOrMore(
				pyparsing.And([
					pyparsing.Literal(',').suppress(),
					identifiers
				])
			)
		])
	),
	pyparsing.Literal(')').suppress(),
	pyparsing.Literal('=').suppress(),
	pyparsing.Group(
		pyparsing.OneOrMore(
			domains
		)
	),
	pyparsing.Literal(':').suppress(),
	ranges
]).setResultsName('declarations')

definitions = pyparsing.And([
	pyparsing.Literal('=').suppress(),
	statements
]).setResultsName('definitions')

blanks = pyparsing.And([
	pyparsing.LineStart().suppress(),
	pyparsing.LineEnd().suppress()
]).setResultsName('blanks')

programs = pyparsing.Or([
	declarations,
	definitions,
	iterations,
	statements,
	blanks
])

def parse(string):
	results = list()
	for source in string.split('::'):
		source = source.strip()
		result = programs.parseString(source)
		for typename in ['declarations', 'definitions', 'iterations', 'statements', 'blanks']:
			if typename in result:
				results.append((typename, source, result.asList()))
				break
	return [result for result in reversed(results)]
