import shutil
import subprocess
import string
import fileinput

class Rating(object):

	def __init__(self, scheme, mapnum, timestamp):
		self.scheme = scheme
		self.timestamp = timestamp
		self.mapnum = mapnum

	def getscheme(self):
		return (self.scheme)

	def gettime(self):
		return (self.timestamp)

	def getmapnum(self):
		return(self.mapnum)

class Compare(object):

	def __init__ (self):
		self.maps = [] #list of map file names
		self.schemas = [] #list of schemas
		self.path = [] #path to folder
		self.ratings = []

	def getinput(self, nmaps, nschema):
		self.path = raw_input("Input file path")
		i = 0
		while i < nmaps:
			temp = raw_input("Input map name (do not include file type)")
			self.maps.append(temp)
			i = i + 1

		i = 0
		while i < nschema:
			temp = raw_input("Input schema name (do not include file type)")
			self.schemas.append(temp)
			i = i + 1

	def runall(self):
		#run schemas on maps
		for map in self.maps:
			temp = map + ".dsc"
			for scheme in self.schemas:
				shutil.copyfile(temp, "mapcopy.dsc") #copy file, rename to "mapcopy.dsc"    			

				filedata = None
				with open('mapcopy.dsc', 'r') as file:
					filedata = file.read()

				filedata = filedata.replace('SchemaDemo', scheme) #replace "SchemaDemo" with scheme in file

				with open('mapcopy.dsc', 'w') as file:
					file.write(filedata)	

				f = open("demo", 'w')
				f.write("java TBSim.TBSim mapcopy.dsc")
				f.close()

        		bashCommand = "./demo"
				print(bashCommand)
				
				f = open(map + scheme + ".txt", 'w+')
				proc =subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True) #run as subprocess
				f.write(proc.stdout.read()) #write output in text file


	def getratings(self):
		#makes list of Rating objects with (scheme, map, time)
		mapnum = 0
		for map in self.maps:
			for scheme in self.schemas:
				f = open(map+scheme+".txt", 'r')
				content = f.readlines()
				for line in content:
					if line[0] == "/" and line[1] == "t":
						a,b=line.split(",")
						rating = Rating(scheme, mapnum, b)
						self.ratings.append(rating)
			mapnum = mapnum + 1

	def sortratings(self, ratinglist):
		#sort into lists of ratings for each map and bubblesort them
		mapnum=0
		index = 0
		for map in self.maps:
			mapratings = []
			for scheme in self.schemas:
				if ratinglist[index].getmapnum() == mapnum:
					mapratings.append(ratinglist[index])
				index = index + 1
			print ("Map " , mapnum , ":")
			self.bubblesort(mapratings)
			mapnum = mapnum + 1

	def bubblesort(self, ratinglist):
		#bubblesorting ratings
  		for passnum in range(len(ratinglist)-1,0,-1):
        		for i in range(passnum):
            			if ratinglist[i].gettime() > ratinglist[i+1].gettime():
                			temp = ratinglist[i]
                			ratinglist[i] = ratinglist[i+1]
                			ratinglist[i+1] = temp
        	j = 0
        	while j < len(ratinglist):
        		print(ratinglist[j].getscheme() + " with time " + ratinglist[j].gettime())
        		j = j + 1


c = Compare()
c.getinput(2, 2)
print("got input")
c.runall()
print("ran all")
c.getratings()
print("got ratings")
c.sortratings(c.ratings)
print("ratings sorted")

