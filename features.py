
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

	def __repr__(self):
		return str(self.featureList)

class Feature():

	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __repr__(self):
		return self.name+" "+str(self.value)