##
#
# Written by Jared Paeschke, jpaeschk@uoregon.edu
# Course: CIS 422 Spring 2017
#
# This class is part of a team project to make a team formation automater &
# optimizer. Project members include Alister Maguire, Jared Paeschke, & 
# Garett Roberts.
# 
##

from student import Student
from day import Day

class Team:

	#constructor
	def __init__(self, minimum=3, maximum=4):
		self.__members = []
		self.__minsize = minimum
		self.__maxsize = maximum
		self.__rating = 0

	#getters
	def getMemberByIndex(self, i):
		if not isinstance(i,int):
			return None
		
		return self.__members[i];

	def getMinSize(self):
		return self.__minsize

	def getMaxSize(self):
		return self.__maxsize

	def getRating(self):
		return self.__rating
	#end getters

	#setters		
	def setMinSize(self, i):
		if not isinstance(i,int):
			return
		else:
			self.__minsize = i

	def setMaxSize(self, i):
		if not isinstance(i,int):
			return
		else:
			self.__maxsize = i

	def setRating(self, i):
		if not isinstance(i, int):
			return
		
		if i < 0 or i > 100:
			return
		else:
			self.__rating = i	
	#end setters
			
	#returns current number of team members
	def getTeamSize(self):
		return len(self.__members)

	#adds a Student to the team, only allows Student objects
	#if student is found in the list it is not added. returns
	#true or false depending on successful insert.
	def insertStudent(self, student):
		if len(self.__members) > self.getMaxSize():
			return False

		if type(student).__name__ != "Student":
			return False

		for i in range(len(self.__members)):
			if student == self.__members[i]:
				return False

		self.__members.append(student)
		return True

	#removes a student from the team. returns true
	#if action was successful, false otherwise.
	def remStudent(self, s):
		if type(s).__name__ != "Student":
			return False

		for i in range(len(self.__members)):
			if s == self.__members[i]:
				del self.__members[i]
				return True

		return False

	#purges the list of members on this team. also affects
	#anything that references to this value. (exampel:
	#cpy = self.__members; cpy will be purged too)
	def purgeMembers(self):
		del self.__members[:]

	#determines if two teams are equivalent
	def __eq__(self,other):
		if self.getTeamSize() != other.getTeamSize():
			return False

		for i in range(len(self.__members)):
			if self.__members[i] != other.__members[i]:
				return False
		return True

	#represents the team object as a string
	def __str__(self):
		output = ""
		for i in range(len(self.__members)):
			output += str(self.__members[i]) + "\n"

		return output[:-1]

#tester function the Team class, only runs when this module is main
def test_team():
	d1 = Day("Tuesday")
	d1.insertTime(10)
	d1.insertTime(13)

	d2 = Day("Wednesday")
	d2.insertTime(10)
	d2.insertTime(14)

	s1 = Student("Jared Paeschke","mahananaka@gmail.com")
	s1.insertDay(d1)
	s1.insertDay(d2)

	s2 = Student("Jared Paeschke","jpaeschk@uoregon.edu")
	s2.insertDay(d2)

	t = Team(3,4)
	print("t.insertStudent(s1): " + str(t.insertStudent(s1)))
	print("t.insertStudent(s1): " + str(t.insertStudent(s1)))
	print("t.insertStudent(s2): " + str(t.insertStudent(s2)))

	print(t)

if __name__ == "__main__":
	test_team()