import random
from collections import defaultdict
import numpy as np
import operator
from sklearn.metrics import confusion_matrix, classification_report
fp=open('wine.data','r')
lables=[]
datadict={}
lists=fp.readlines()

print len(lists)
for line in lists:
	line=line.strip()
	data=line.split(",")
	features=tuple(map(float, line.split(',')[1:]))
	lables.append(data[0])
	datadict[features]=data[0]

features=datadict.keys()
random.seed(123)
random.shuffle(features)
def euclediandistance(x,c):
	d=np.array(x)-np.array(c)
	return np.sqrt(np.dot(d,d))
def assign(centers):
	new_centers=defaultdict(list)
	for cx in centers:
		for x in centers[cx]:
			best = min(centers, key=lambda c: euclediandistance(x,c))
			new_centers[best]+=[x]
	return new_centers
def mean(features):
	return tuple(np.mean(features,axis=0))
def update(centers):
	new_centers={}
	for c in centers:
		#newkey=mean(centers[c])
		minind=0
		mindist=99999999999999999999999999999999999
		features=centers[c]
		for i in features:
			dist=0
			for j in features:
				dist=dist+euclediandistance(i,j)
			if dist<mindist:
				minind=i
				mindist=dist
		newkey=minind
		new_centers[newkey]=centers[c]
	return new_centers



def kmeans(features,k,Evolutions=200):
 
	#print "hello"
	centers={}
	length=len(features)
	part=length/3
	features1=features[0:part]
	features2=features[part:2*part]
	features3=features[2*part:]
	centers[features[0]]=features1
	centers[features[part]]=features2
	centers[features[2*part]]=features3
	#print centers
	for i in range(Evolutions):
		#print i,"hello"
		new_centers=assign(centers)
		new_centers=update(new_centers)
		if centers==new_centers:
			break
		else:
			centers=new_centers
	return centers

def counter(clus):
	count=defaultdict(int)
	for x in clus:
		count[x]+=1
	return dict(count)


clusters=kmeans(features,3)


dictcl={}
dictlabel={}
i=0
for c in clusters:
	dictcl[i]=counter([datadict[x] for x in clusters[c]])
	key=max(dictcl[i].iteritems(), key=operator.itemgetter(1))[0]
	dictlabel[key]=counter([datadict[x] for x in clusters[c]])
	i=i+1
print dictlabel

#######################External Measures####################################
outputLables=[]
for i in dictlabel:
	outputLables.append(i)
#print outputLables

TrueValue=datadict
PredValue={}

i=0
for c in clusters:
	for f in clusters[c]:
		PredValue[f]=outputLables[i]

	i=i+1
Tr=[]
Pr=[]
for ft in TrueValue:
	Tr.append(TrueValue[ft])
	Pr.append(PredValue[ft])
#for i in range(len(Tr)): print Tr[i],Pr[i]






sets=set(lables)
sets=list(sets)
ll=len(sets)
print ll;
CM=[[0 for x in range(ll)] for x in range(ll)]

for i in dictlabel:
	for j in range(len(sets)):
		if sets[j] in dictlabel[i]:
			i1=sets.index(sets[j])
			i2=sets.index(i)
			CM[i1][i2]+=dictlabel[i][sets[j]]
		else:
			i1=sets.index(sets[j])
			i2=sets.index(i)
			CM[i1][i2]+=0
print CM

correctvalues=0;
wrongvalues=0;
for i in range(ll):
    for j in range(ll):
         if i==j:
            correctvalues+=CM[i][j]
	 else:
            wrongvalues+=CM[i][j]
Accuracy=(correctvalues*100)//(correctvalues+wrongvalues)
print "Accuracy =", Accuracy,"%"

print(classification_report(Tr, Pr))
#print features







#########################INTERNAL MEASURE ####################################
S=[]
i=0
centroids=[]
maxdist=[]
for c in clusters:
	centroids.append(c)
	sumd=0
	d=0
	l=len(clusters[c])
	for f in clusters[c]:
		sumd+=euclediandistance(f,c)
		if d<euclediandistance(f,c):
			d=euclediandistance(f,c)
 	ss=sumd/(1.0*l)
	S.append(ss)
	maxdist.append(d)
Mdist=[]
for i in centroids:
	tempj=[]
	for j in centroids:		
		tempj.append(euclediandistance(i,j))
	Mdist.append(tempj)
#print Mdist
dunnindex=0
x=[]
for i in range(len(S)):
	for j in range(len(S)):
		if i<j:
			d=Mdist[i][j]/max(maxdist)
			x.append(d)
dunnindex=min(x)
Rdist=[]
for i in range(len(S)):
	tempj=[]
	for j in range(len(S)):		
		num=S[i]+S[j]
		denom=Mdist[i][j]
		if denom==0 or i >=j:
			tempj.append(0)
		else:
			tempj.append(num/(1.0*denom))
	Rdist.append(tempj)
#print Rdist

D=[]
for i in Rdist:
	D.append(max(i))

DBvalue=sum(D)/(1.0*len(D))

print DBvalue
print dunnindex
