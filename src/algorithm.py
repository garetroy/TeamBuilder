'''
@author Garett Roberts
created: Sun Apr 15 12:51:00 PDT 2017

Algorithms creates a set of teams for the Team Builder.
It takes creates a random set of teams and weights them.

Modifications:

Alister Maguire, Sat Apr 22 10:18:00 PDT 2017 
Added filters to the algorithm. Changed the 
weightCalc to account for the normalization. 
Fixed a bug in the main algorithm. Experimented
with changing k, d, and n values. 

Alister Maguire, Sun Apr 23 12:54:54 PDT 2017
extended initTeamSet to handle students that
don't fit nicely into the group sizes. 

'''

from random import randrange
from student import Student
from team import Team
from filters import *
import sys

class AlgorithmManager():
    '''
    A algorithm manager for handling the team building
    '''

    def __init__(self, team_size=3, k=10,d=20,n=25):
        '''
            Initializes manager with the filter map, which maps the student
            prefrences to the corresponding functions to calculate the weights
            of the teams.

            @param:
                filter_dictionary: filterID's that map to functions

        '''
        #TODO: we need to change from hardcoding to dynamic here. 
        self.__filter_dictionary = { "Schedule" : scheduleFilter,
                                     "Languages": languageFilter,
                                     "Teammates": teammateFilter }
        self.__team_size         = team_size
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
        #TODO: there may be a better way to handle minimum team size
        team_in     = Team(self.__team_size, self.__team_size + 1)
        for s in range(len(studentlist)):
            #TODO: this is very inefficient; let's do better
            randnum = randrange(0,len(studentlist))
            student = studentlist.pop(randnum)
            team_in.insertStudent(student)
            if(team_in.getMinSize() == team_in.getTeamSize()):
                self.weightCalc(team_in)
                team_set.append(team_in)
                team_in = Team(self.__team_size, self.__team_size + 1)

        t_max     = team_in.getMaxSize()
        num_extra = team_in.getTeamSize()
        if num_extra < t_max:
            if num_extra > len(team_set):
                print(""""ERROR: there are too many excess students for the team
                          sizes you have chosen for this class size. Try 
                          re-thinking team sizes""")
                sys.exit(0)
            leftovers = team_in.getMemberList()
            idx = 0
            while leftovers:
                team_set[idx].insertStudent(leftovers.pop())    
                idx = (idx + 1) if (idx < t_max) else 0

        return team_set

    def weightCalc(self,team_in):
        '''
            Creates a weight for the team and sets the teams weight

            @param:
                team_in(Team) - A team
        '''
        team_in.setRating(0)
        size   = team_in.getTeamSize()
        weight = 0.0
        for i in range(size):
            for j in range(i+1, size):
                weight += self.getWeight(team_in.getMemberByIndex(i),team_in.getMemberByIndex(j))

        #Normalize the weights
        weight = weight / float(self.__team_size)
        team_in.setRating(weight)
    
    def getWeight(self, student1, student2):
        '''
            Creates a weight between two students
    
            @param:
                student1, student2 (Student) - Student
            
            @returns:
                total (int) - the rating of two students
        '''
        total = 0.0
        for f in student1.getPrefs():
            total += self.getFilterDictionary()[f](student1,student2)  
        return total

    def swapMembers(self,teams):
        '''
            Swaps members within teams and re-calculates ratings

            @param:
                teams: [Team] - a list of teams
            
            @returns:
                teams: [Team] - swapped teams
        '''
        size = len(teams)

        if(size == 1):
            return teams

        #need to create new teams to move members around
        new_teams = []
        for i in range(size):
            new_t = Team()
            new_t.deepCopy(teams[i])
            new_teams.append(new_t)
            
        for i in range(size):
            swp_idx = i
            while swp_idx == i:
                swp_idx = randrange(size)
                
            s1 = new_teams[i].getMemberList().pop()
            s2 = new_teams[swp_idx].getMemberList().pop()

            new_teams[i].insertStudent(s2)
            new_teams[swp_idx].insertStudent(s1)

            self.weightCalc(new_teams[i])
            self.weightCalc(new_teams[swp_idx])

        return new_teams

    def deviation(self,teams):
        '''
            Finds the deviation for each of the teams

            @params:
                teams: [Team]
            
            @returns:
                dev (int) - Deviation of list
        '''
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
        '''
            Creates k different sets of teams, then finds the teams and swaps them around
            until we get an "evened" out team set
        
            @params:
                students [Student] - a list of all the students
        '''
        grouping_list = []

        for _ in range(self.k):
            grouping_list.append(self.initTeamSet(students))

        for _ in range(self.d):
            for _ in range(self.k):
                variants = []
                teams = grouping_list.pop()
                variants.append(teams)
                for _ in range(self.n - 1):
                    variants.append(self.swapMembers(teams))

                min_dev = 100
                min_idx = 0
                for m in range(self.n - 1):
                    dev = self.deviation(variants[m]) 
                 
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
