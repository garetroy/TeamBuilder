'''
@author Garett Roberts
created: Sun Apr 15 12:51:00 PDT 2017

Algorithms creates a set of teams for the Team Builder.
It takes creates a random set of teams and weights them.

'''

from random import randrange
from student import Student
from team import Team

class AlgorithmManager():
    '''
    A algorithm manager for handling the team building
    '''

    def __init__(self,k=4,d=4,n=4):
        '''
            Initializes manager with the filter map, which maps the student
            prefrences to the corresponding functions to calculate the weights
            of the teams.

            @param:
                filter_dictionary: filterID's that map to functions

        '''

        self.__filter_dictionary = {"Meeting Times":(lambda s1,s2: 10)}
        self.k                   = k
        self.d                   = d
        self.n                   = n

    '''
        Start Getters and Setters
    ''' 
    def getFilterDictionary(self):
        return self.__filter_dictionary

    def setFilterDictionary(self,fd):
        self.__filter_dictionary = fd

    def addFilter(self,filterin):
        '''
            Adds filters into the filter dictionary

            @param:
                filterin(string,function)
        '''
        self.__filter_dicitonary.append(filterin)

    '''
        End Getters and Setters
    '''

    def initTeamSet(self,students):
        '''
            Creates a TeamSet given a list of students
            Creates weights for each team
            
            @param:
                students([Student]) - a list of students

            @returns:
                [Team] - A set of teams  
        '''
        studentlist = [i for i in students] 
        team_set    = []
        team_in     = Team()
        for s in range(len(studentlist)):
            randnum = randrange(0,len(studentlist))
            student = studentlist.pop(randnum)
            team_in.insertStudent(student)
            if(team_in.getMaxSize() == team_in.getTeamSize()):
                self.weightCalc(team_in)
                team_set.append(team_in)
                team_in = Team()

        return team_set

    def weightCalc(self,team_in):
        '''
            Creates a weight for the team and sets the teams weight

            @param:
                team_in(Team) - A team
        '''
        team_in.setRating(0)
        for i in range(team_in.getTeamSize()):
            for j in range(i+1,team_in.getTeamSize()):
                team_in.setRating(team_in.getRating() + self.getWeight(team_in.getMemberByIndex(i),team_in.getMemberByIndex(j)))
    
    def getWeight(self, student1, student2):
        '''
            Creates a weight between two students
    
            @param:
                student1, student2 (Student) - Student
        '''
        total = 0
        for f in student1.getPrefs():
            total += self.getFilterDictionary()[f](student1,student2)  
        return total

    def swapMembers(self,teams):
        return 0

    def deviation(self,teams):
        max_idx = 0
        min_idx = 0

        for i in range(len(teams)):
            if teams[i].getRating() > teams[max_idx].getRating():
                max_idx = i
            if teams[i].getRating() < teams[min_idx].getRating():
                min_idx = i

        dev = teams[max_idx].getRating() - teams[min_idx].getRating()
        return dev

    def runMain(self,students):
        grouping_list = []

        for _ in range(self.k):
            grouping_list.append(self.initTeamSet(students))

        for _ in range(self.d):
            for _ in range(self.k):
                teams = grouping_list.pop()
                variants = []
                for _ in range(self.n):
                    variants.append(self.swapMembers(teams))

                min_dev = 100
                min_idx = 0
                for m in range(0):
                    dev = self.deviation(teams[m])
                    
                    if dev < min_dev:
                        min_dev = dev
                        min_idx = m

                grouping_list.append(variants[min_idx])

        min_dev = 100
        min_idx = 0
        for i in range(self.k):
            dev = self.deviation(grouping_list[i])
            if dev < min_dev:
                min_dev = dev
                min_idx = i
        
        return grouping_list[min_idx]
