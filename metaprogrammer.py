import metaparser, metagenerator
import sys

print metagenerator.programs([metaparser.parse(line) for line in sys.stdin.readlines()])
