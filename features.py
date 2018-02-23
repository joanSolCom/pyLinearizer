
class Features():

	def __init__(self):
		self.featureList = []
		self.featureDict = {}

	def addFeature(self, name, value):
		self.featureList.append(Feature(name,value))
		self.featureDict[name] = value

	def getFeatureVector(self):
		vector = []
		for feat in self.featureList:
			if type(feat.value) is list:
				vector.extend(feat.value)
			else:
				vector.append(feat.value)
		
		return vector

	def padFeature(self,name,maxValue):
		for feat in self.featureList:
			if feat.name == name:
				listValues = feat.value
				numElems = len(listValues)
				
				if numElems< maxValue:
					while numElems < maxValue:
						listValues.append(-1)
						numElems+=1

				elif numElems > maxValue:
					raise ValueError("Some Padding poltergeist")

		listValues = self.featureDict[name]
		numElems = len(listValues)
				
		if numElems< maxValue:
			while numElems < maxValue:
				listValues.append(-1)
				numElems+=1

		elif numElems > maxValue:
			raise ValueError("Some Padding poltergeist")



	def __repr__(self):
		return str(self.featureList)

class Feature():

	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __repr__(self):
		return self.name+" "+str(self.value)