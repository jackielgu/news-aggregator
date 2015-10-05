import indicoio
indicoio.config.api_key = "246290703649a7500961ea78369dbce8"
size = 6;
clusters = 2;

##returns connection weight of two sentence dictionaries
def compareKeywords(first, second):
	pairscore = 0;
	satscore = 0;
	keyList1 = first.keys()
	keyList2 = second.keys()
	for x in range(0,len(first)):
		for y in range(0,len(second)):
			if keyList1[x] == keyList2[y]:
				pairscore += first[keyList1[x]] * second[keyList2[y]]
				satscore += 1.0/8
				#print str(x) + " " + str(y) + " " + "pairscore: " + str(pairscore)
				#print str(x) + " " + str(y) + " " + "satscore: " + str(satscore)
	return pairscore*satscore
def compareTags(first, second):
	tagscore = 0;
	keyList1 = first.keys()
	keyList2 = second.keys()
	for x in range(0,len(first)):
		for y in range(0,len(second)):
			if keyList1[x] == keyList2[y]:
				tagscore += first[keyList1[x]] * second[keyList2[y]]
				#print str(x) + " " + str(y) + " " + "tagscore: " + str(tagscore)
	return tagscore
def compareEntities(first,second):
	entityscore = 1;
	keyList1 = first.keys()
	keyList2 = second.keys()
	for x in range(0,len(first)):
		for y in range(0,len(second)):
			if keyList1[x] == keyList2[y]:
				if x != y:
					entityscore += .6
					#print str(x) + " " + str(y) + " " + "entityscore: " + str(entityscore)
	return entityscore

fd = open("NYT.txt","r")
string1 = fd.read()
#fd = open("BBC.txt", "r")
#string1 += fd.read()
string1 = string1.replace("\xe2\x80\x9c", "\"")
string1 = string1.replace("\xe2\x80\x9d", "\"")
string1 = string1.replace("\xe2\x80\x99", "\'")
keywordList = []
tagList = []
entityList = []

myList = string1.split("\n", size)

for x in range (0,size):
	keywordList.append(indicoio.keywords(myList[x], top_n=10, independent=True))
	tagList.append(indicoio.text_tags(myList[x], threshold=.05))
	entityList.append(indicoio.named_entities(myList[x]))
	#print indicoio.text_tags(myList[x], threshold=.1)
	#print indicoio.keywords(myList[x], top_n=6, independent=True)

## build 2-d array of weights
matrix = [[0 for x in range(size)] for x in range(size)]

for x in range (0,size):
	for y in range (0,size):
		matrix[x][y] = 1000 * compareKeywords(keywordList[x],keywordList[y]) * compareTags(tagList[x],tagList[y]) *  compareEntities(entityList[x],entityList[y])
		#print str(x) + " " + str(y) + " " + str(matrix[x][y])

def best(n, matrix):
    choose = []
 
    for rep in range(0, n):
        #print matrix
        best = 0
        which = 0
        for i in range(0, len(matrix)):
            time = 0
            for j in range(0, len(matrix[i])):
                time += matrix[i][j]
            if time > best:
                best = time
                which = i
 
        #print which
        choose.append(which)
 
        matrix[which] = []
        for i in range(0, len(matrix)):
            matrix[which].append(0)
            matrix[i].pop(which)
 
    return choose

output = best(clusters, matrix)

for x in range(0, clusters):
	print(myList[output[x]])

def bias(phrase):
	biasDict = indicoio.political("phrase")
	biasKeys = biasDict.keys()
	for x in range(0, 4):
		biasList[x] = biasDict[biasKeys[x]]

