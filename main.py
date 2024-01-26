from sklearn.datasets import load_iris
import random
import numpy as np
from numpy.linalg import norm

x , y = load_iris(return_X_y = True)

print(x)

class Cromozom:
    def __init__(self, gen, clusstring):
        self.gen = gen
        self.clusstring = clusstring

    
    def Mutatie(self):
        sizeGen = len(self.gen)
        i = random.randint(0, sizeGen - 1)
        self.gen[i] = random.randint(1, self.clusstring)
    
    def CrossOver(self, gen2):
        randomPosition = random.randint(1, len(self.gen))
        newGen = []

        for i in range(0, randomPosition):
            newGen.append(self.gen[i])
        for i in range(randomPosition, len(self.gen)):
            newGen.append(gen2.gen[i])

        newGen2 = []

        for i in range(0, randomPosition):
            newGen2.append(gen2.gen[i])
        for i in range(randomPosition, len(self.gen)):
            newGen2.append(self.gen[i])
        
        return Cromozom(newGen, self.clusstring), Cromozom(newGen2, self.clusstring)
    
    def __str__(self) -> str:
        return str(self.gen)
    

    def fitness(self, data):
        fitness = 0
        for i in range(1, self.clusstring + 1):
            sum1 = 0
            sum2 = 0
            sum3 = 0
            sum4 = 0
            num = 0
            for j in range(0, len(self.gen)):
                if self.gen[j] == i:
                    num += 1
                    sum1 += data[j][0]
                    sum2 += data[j][1]
                    sum3 += data[j][2]
                    sum4 += data[j][3]
            center = [sum1 / num, sum2 / num, sum3 / num, sum4 / num]
            centerGen = 0
            for j in range(0, len(self.gen)):
                if self.gen[j] == i:
                    centerGen += minDistance(center, data[j]) / num

            fitness += centerGen / self.clusstring

        return fitness

                        


def population(size, clusstring, genSize):
    pop = []
    for i in range(0, size):
        gen = []
        for j in range(0, genSize):
            gen.append(random.randint(1, clusstring + 1))
        pop.append(Cromozom(gen, clusstring))
    return pop

def minDistance(point1, point2):
    return 1 - np.dot(point1,point2)/(norm(point1)*norm(point2))

def pickWinners(population, k, data):
    populationWithFitness = [(cromozom, cromozom.fitness(data)) for cromozom in population]
    populationWithFitness.sort(key= lambda x:x[1], reverse = True)
    winners = []
    for i in range(0 , k):
        winners.append(populationWithFitness[i][0])
    print(populationWithFitness[0][1])
    return winners

def train(data, clusster, MutatieChance, k, size, genSize):
    people = population(size, clusster, genSize)
    print("people /n", people)
    while(True):
        for i in range(0, len(people)):
            if people[i] == None:
                people.remove(people[i])

        winners = pickWinners(people, k, data)
        for i in range(0 , size):
            for j in range(i, size):
                child1 , child2 = winners[i].CrossOver(winners[j])
                numChild1 = random.randint(0, 100)
                numChild2 = random.randint(0, 100)
                if numChild1 <= MutatieChance * 100:
                    child1.Mutatie()
                if numChild2 <= MutatieChance * 100:
                    child2.Mutatie()
                winners.append(child1)
                winners.append(child2)
        people = winners


train(x, 3, 0.3, 10, 10, 150)


