from features import Features

class Instances():

	def __init__(self, conllStruct):
		self.instance_list = []
		self.posSet = set()
		self.depSet = set()
		self.dictPos = {}
		self.dictDep = {}

		for sentence in conllStruct.sentences:
			iSent = Instance(sentence)
			self.instance_list.append(iSent)
			for token in sentence:
				self.posSet.add(token.pos)
				self.depSet.add(token.deprel)

		for idx, pos in enumerate(self.posSet):
			self.dictPos[pos] = idx
		for idx, dep in enumerate(self.depSet):
			self.dictDep[dep] = idx

		for inst in self.instance_list:
			inst.dictDep = self.dictDep
			inst.dictPos = self.dictPos
			inst.computeAtomicFeatures()

		self.padBigramFeatures()
		self.padTrigramFeatures()
		self.getFeatureVectors()

	def getFeatureVectors(self):
		for instance in self.instance_list:
			instance.getFeatureVectors()


	def padBigramFeatures(self):
		maxNumBigrams = -1
		for inst in self.instance_list:
			for node in inst.node_list:
				numBigrams = len(node.bigramFeatures)
				if numBigrams > maxNumBigrams:
					maxNumBigrams = numBigrams

		for inst in self.instance_list:
			inst.padBigramFeatures(maxNumBigrams)

	def padTrigramFeatures(self):
		maxNumTrigrams = -1
		for inst in self.instance_list:
			for node in inst.node_list:
				numTrigrams = len(node.trigramFeatures)
				if numTrigrams > maxNumTrigrams:
					maxNumTrigrams = numTrigrams

		for inst in self.instance_list:
			inst.padTrigramFeatures(maxNumTrigrams)
	
	def __iter__(self):
		return iter(self.instance_list)

class Instance():

	def __init__(self, conllSentence):
		self.sentence = conllSentence
		self.node_list = []
		self.root = None
		self.globalFeatures = None
		self.dictPos = {}
		self.dictDep = {}

		for token in conllSentence:
			if token.head == "0":
				self.root = token

			iNode = Node(token)
			self.node_list.append(iNode)

		self.computeGlobalFeatures()
		self.computeBigramFeatures()
		self.computeTrigramFeatures()


	def getFeatureVectors(self):
		for idx, node in enumerate(self.node_list):
			nodeVector = []
			nodeVector.extend(self.globalFeatures.getFeatureVector())
			nodeVector.extend(node.atomicFeatures.getFeatureVector())
			for bigramF in node.bigramFeatures:
				nodeVector.extend(bigramF.getFeatureVector())
			for trigramF in node.trigramFeatures:
				nodeVector.extend(trigramF.getFeatureVector())

	def computeBigramFeatures(self):
		for parent in self.node_list:
			children = self.getChildren(parent)
			bigrams = []
			for child in children:
				iFeatures = Features()
				labelw1 = parent.conllLine.deprel
				iFeatures.addFeature("labelw1",labelw1)

				labelhead = parent.conllLine.deprel
				iFeatures.addFeature("labelhead",labelhead)

				labelw2 = child.conllLine.deprel
				iFeatures.addFeature("labelw2",labelw2)

				lemmaw1 = parent.conllLine.lemma
				iFeatures.addFeature("lemmaw1",lemmaw1)

				lemmaw2 = child.conllLine.lemma
				iFeatures.addFeature("lemmaw2",lemmaw2)

				posw1 = parent.conllLine.pos
				iFeatures.addFeature("posw1",posw1)

				posw2 = child.conllLine.pos
				iFeatures.addFeature("posw2",posw2)

				num_childrenw1 = len(children)
				iFeatures.addFeature("num-childrenw1",num_childrenw1)

				childrenw2 = self.getChildren(child)
				num_childrenw2 = len(childrenw2)
				iFeatures.addFeature("num-childrenw2",num_childrenw2)

				poshead = parent.conllLine.pos
				iFeatures.addFeature("poshead",poshead)

				poschild = child.conllLine.pos
				iFeatures.addFeature("poschild",poschild)

				parent.bigramFeatures.append(iFeatures)


	def computeTrigramFeatures(self):
		for parent in self.node_list:
			children = self.getChildren(parent)
			for child in children:
				grandChildren = self.getChildren(child)
				for grandChild in grandChildren:
					iFeatures = Features()

					#HEAD(w1,w2,w3) ??
					lemmaw1 = parent.conllLine.lemma
					iFeatures.addFeature("lemmaw1",lemmaw1)

					lemmaw2 = child.conllLine.lemma
					iFeatures.addFeature("lemmaw2",lemmaw2)

					lemmaw3 = grandChild.conllLine.lemma
					iFeatures.addFeature("lemmaw3",lemmaw3)

					posw1 = parent.conllLine.pos
					iFeatures.addFeature("posw1",posw1)

					posw2 = child.conllLine.pos
					iFeatures.addFeature("posw2",posw2)

					posw3 = grandChild.conllLine.pos
					iFeatures.addFeature("posw3",posw3)

					labelw1 = parent.conllLine.deprel
					iFeatures.addFeature("labelw1",labelw1)

					labelw2 = child.conllLine.deprel
					iFeatures.addFeature("labelw2",labelw2)

					labelw3 = grandChild.conllLine.deprel
					iFeatures.addFeature("labelw3",labelw3)
					parent.trigramFeatures.append(iFeatures)



	def computeGlobalFeatures(self):
		iFeatures = Features()
		
		labelw1 = self.node_list[0].conllLine.deprel
		iFeatures.addFeature("labelw1",labelw1)

		labelwn_1 = self.node_list[-2].conllLine.deprel
		iFeatures.addFeature("labelwn_1",labelwn_1)

		lemmaRoot = self.root.lemma
		iFeatures.addFeature("lemmaRoot",lemmaRoot)

		lemmaw1 = self.node_list[0].conllLine.lemma
		iFeatures.addFeature("lemmaw1",lemmaw1)

		lemmawn_1 = self.node_list[-2].conllLine.lemma
		iFeatures.addFeature("lemmawn_1",lemmawn_1)

		posw1 = self.node_list[0].conllLine.pos
		iFeatures.addFeature("posw1",posw1)

		posw2 = self.node_list[1].conllLine.pos
		iFeatures.addFeature("posw2",posw2)

		posw3 = self.node_list[2].conllLine.pos
		iFeatures.addFeature("posw3",posw3)

		poswn_1 = self.node_list[-2].conllLine.pos
		iFeatures.addFeature("poswn_1",poswn_1)

		poswn_2 = self.node_list[-3].conllLine.pos
		iFeatures.addFeature("poswn_2",poswn_2)

		poswn_3 = self.node_list[-4].conllLine.pos
		iFeatures.addFeature("poswn_3",poswn_3)

		question = 0
		for node in self.node_list:
			if "?" in node.conllLine.form:
				question = 1
				break

		iFeatures.addFeature("question",question)

		self.globalFeatures = iFeatures

	def computeAtomicFeatures(self):
		for node in self.node_list:
			iFeatures = Features()

			lemma = node.conllLine.lemma
			iFeatures.addFeature("lemma",lemma)

			label = node.conllLine.deprel
			iFeatures.addFeature("label",label)
			pos = node.conllLine.pos
			iFeatures.addFeature("pos",pos)

			children = self.getChildren(node)
			grandChildren = self.getGrandChildren(children)

			num_children = len(children)
			iFeatures.addFeature("num-children",num_children)

			num_grandChildren = len(grandChildren)
			iFeatures.addFeature("num-grandchildren",num_grandChildren)

			labels_children = []
			pos_children = []
			for child in children:
				labels_children.append(child.conllLine.deprel)
				pos_children.append(child.conllLine.pos)

			# [numberNmods, numberPmods, .... totalNumberOfDeps] same with pos
			lenPos = len(self.dictPos)
			lenDep = len(self.dictDep)
			i=0
			j=0
			posVector = []
			depVector = []
			while i<lenPos:
				posVector.append(0)
				i+=1
			while j<lenDep:
				depVector.append(0)
				j+=1

			for labelChild in labels_children:
				position = self.dictDep[labelChild]
				depVector[position]+=1

			for posChild in pos_children:
				position = self.dictPos[posChild]
				posVector[position]+=1

			iFeatures.addFeature("labels-children",depVector)
			iFeatures.addFeature("pos-children",posVector)
			node.atomicFeatures = iFeatures

	def padBigramFeatures(self, maxNumBigrams):
		for node in self.node_list:
			node.padBigramFeatures(maxNumBigrams)

	def padTrigramFeatures(self, maxNumTrigrams):
		for node in self.node_list:
			node.padTrigramFeatures(maxNumTrigrams)

	def getChildren(self, parent):
		children = []
		for node in self.node_list:
			if node.conllLine.head == parent.conllLine.id:
				children.append(node)

		return children

	def getGrandChildren(self,parents):
		grandChildren = []
		for parent in parents:
			grandChildren.extend(self.getChildren(parent))

		return grandChildren
		

	def __iter__(self):
		return iter(self.node_list)


class Node():

	def __init__(self, conllToken):
		self.conllLine = conllToken
		self.atomicFeatures = None
		self.bigramFeatures = []
		self.trigramFeatures = []
		self.featureVector = []

	def padBigramFeatures(self, maxNumBigrams):
		lenBigrams = len(self.bigramFeatures)
		while lenBigrams < maxNumBigrams:
			iFeatures = Features()
			iFeatures.addFeature("labelw1",-1)
			iFeatures.addFeature("labelhead",-1)
			iFeatures.addFeature("labelw2",-1)
			iFeatures.addFeature("lemmaw1",-1)
			iFeatures.addFeature("lemmaw2",-1)
			iFeatures.addFeature("posw1",-1)
			iFeatures.addFeature("posw2",-1)
			iFeatures.addFeature("num-childrenw1",-1)
			iFeatures.addFeature("num-childrenw2",-1)
			iFeatures.addFeature("poshead",-1)
			iFeatures.addFeature("poschild",-1)
			self.bigramFeatures.append(iFeatures)
			lenBigrams+=1

	def padTrigramFeatures(self, maxNumTrigrams):
		lenTrigrams = len(self.trigramFeatures)
		while lenTrigrams < maxNumTrigrams:
			iFeatures = Features()
			iFeatures.addFeature("lemmaw1",-1)
			iFeatures.addFeature("lemmaw2",-1)
			iFeatures.addFeature("lemmaw3",-1)
			iFeatures.addFeature("posw1",-1)
			iFeatures.addFeature("posw2",-1)
			iFeatures.addFeature("posw3",-1)
			iFeatures.addFeature("labelw1",-1)
			iFeatures.addFeature("labelw2",-1)
			iFeatures.addFeature("labelw3",-1)
			self.trigramFeatures.append(iFeatures)
			lenTrigrams+=1

	def __repr__(self):
		return "==============\nAtomFeats\n"+str(self.atomicFeatures) + "\n\nBigramFeats\n" + str(self.bigramFeatures) + "\n\nTrigramFeats\n" + str(self.trigramFeatures)+"\n==============\n\n"
	

