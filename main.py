from conll import ConllStruct
from instances import Instances

def train():
	pathTraining = "/home/joan/Escritorio/linearization-master/linearizer/CoNLL2009-ST-English-tiny.txt"
	rawConll = open(pathTraining,"r").read()
	iConll = ConllStruct(rawConll)
	iInstTraining = Instances(iConll)

def test():
	pass

def eval():
	pass

train()