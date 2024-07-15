import neat
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import math


total_kcovered_points = 0
total_covered_points = 0

# sensor class
class Sensor:
    def __init__(self, x, y, sensing_range, com_range):
        self.x = x
        self.y = y
        self.sensing_range = sensing_range
        self.com_range = com_range
        self.active = True

    # moves sensor to its position + dx and dy
    def move(self, dx, dy):
        # change sensors location 
        self.x += dx
        self.y += dy

    # determines if a point is in sensors sensing range
    def is_point_covered(self, px, py):
        distance = ((self.x - px)**2 + (self.y - py)**2)**0.5
        return distance <= self.sensing_range

    # determines if a sensor is in sensors communication range
    def is_neighbor(self, other_sensor_x, other_sensor_y):
        distance = ((self.x - other_sensor_x)**2 + (self.y - other_sensor_y)**2)**0.5
        return distance <= self.com_range


#environment class
class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        self.sensor_list = []


    # adds sensor to environment
    def add_sensor(self, sensor, k):
        global total_covered_points
        global total_kcovered_points

        # increment the value of the grid cells within a sensors sensing range
        for i in range(int(max(0, sensor.y - sensor.sensing_range)), int(min(self.height, sensor.y + sensor.sensing_range))):
            for j in range(int(max(0, sensor.x - sensor.sensing_range)), int(min(self.width, sensor.x + sensor.sensing_range))):
                if sensor.is_point_covered(j, i):

                    # if point is now k-covered
                    if self.grid[i][j] == k-1:
                        total_kcovered_points += 1
                        self.grid[i][j] += 1
                    
                    # if point is now 1 covered
                    elif self.grid[i][j] == 0:
                        total_covered_points += 1
                        self.grid[i][j] += 1
                    
                    # if point is k-covered don't add anything, but if its anything else add to the point
                    elif self.grid[i][j] != k:
                        self.grid[i][j] += 1
                        


# calculates connectivity. Divides number of connected 
# components by the number of active sensors to calculate
# a connectivity score. Best score is when active sensors
# = # of connected sensors, which will be 1.0
def calculate_connectivity_score(sensors, com_range):
    num_active_sensors = 0
    active_sensors = []

    for sensor in sensors:
        if sensor.active:
            active_sensors.append(sensor)
            num_active_sensors += 1
    
    if num_active_sensors == 0:
        return 0
    
    # build graph
    graph = {sensor: [] for sensor in active_sensors}
    
    for i in range(num_active_sensors):
        for j in range(i + 1, num_active_sensors):
            sensor = active_sensors[i]
            other_sensor = active_sensors[j]
            # find distance between two sensors
            distance = math.sqrt((sensor.x - other_sensor.x)**2 + (sensor.y - other_sensor.y)**2)
            # if in eachothers communication range connect them
            if distance <= com_range:
                graph[sensor].append(other_sensor)
                graph[other_sensor].append(sensor)
    
    visited = {sensor: False for sensor in active_sensors}
    
    # DFS
    def dfs(sensor):
        stack = [sensor]
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
    
    # run DFS
    dfs(active_sensors[0])
    
    connected_sensors = sum(1 for sensor in active_sensors if visited[sensor])
    connectivity_score = connected_sensors / num_active_sensors
    
    return connectivity_score


def eval_genomes(initial_sol, k):
    global total_covered_points
    global total_kcovered_points

    best_fitness = float('-inf')
    num_generations = 300


    best_scenario = initial_sol


    # itereate through all solutions 
    for gen in range(num_generations):

        for genome in range(27):
            # reset coverage scores
            total_kcovered_points = 0
            total_covered_points = 0
            
            print(genome)
            # copy the universal best solution to an environment for the neural network
            environment = Environment(best_scenario.height, best_scenario.width)
            for sensor in best_scenario.sensor_list:
                new_sensor = Sensor(sensor.x, sensor.y, sensor.sensing_range, sensor.com_range)
                new_sensor.active = sensor.active
                environment.sensor_list.append(new_sensor)

            # mutate
            random_sensors = [random.randint(0, len(best_scenario.sensor_list)-1), random.randint(0, len(best_scenario.sensor_list)-1), random.randint(0, len(best_scenario.sensor_list)-1)]
            for sensor in random_sensors:
                mutated_sensor = environment.sensor_list[sensor]
                mutated_sensor.active = not mutated_sensor.active
            
            # do changes to current environment
            for sensor in environment.sensor_list:
                if sensor.active:
                    environment.add_sensor(sensor, k)

            # compare fitness of current to best current
            genome_fitness = calculate_fitness(environment.sensor_list, environment)

            if genome_fitness > best_fitness:
                best_fitness = genome_fitness
                best_scenario = environment
    

        # reset grid for next round
        best_scenario.grid = np.zeros((best_scenario.height, best_scenario.width))

        for sensor in best_scenario.sensor_list:
            if sensor.active:
                print(sensor.x, sensor.y)


# caclulates fitness of scenarios after 
# neural network made changes to them
def calculate_fitness(sensors, environment):
    global total_covered_points
    global total_kcovered_points


    active_sensors = 0
    inactive_sensors = 0

    
    connectivity_score = calculate_connectivity_score(sensors, sensors[0].com_range)

    k_coverage_rate = total_kcovered_points / (environment.height * environment.width)
    coverage_rate = total_covered_points / (environment.height * environment.width)


    for sensor in sensors:
        if not sensor.active:
            inactive_sensors += 1
        else:
            active_sensors +=1
    
    inactivity = inactive_sensors / len(sensors)

    if connectivity_score == 1.0:
        connectivity_score *= 100
    if k_coverage_rate == 1.0:
        k_coverage_rate *= 100
    if coverage_rate == 1.0:
        coverage_rate *= 100

    fitness_score = (
        connectivity_score * 0.33 +
        k_coverage_rate * 0.35 +
        coverage_rate * 0.31 +
        inactivity * 1
    )

    print(connectivity_score, k_coverage_rate, coverage_rate, active_sensors, fitness_score)
    return fitness_score


def main():
    global total_covered_points
    global total_kcovered_points

    num_generations = 300

    k = 2
    scenario_dimensions = (50, 50)
    sensor_positions = []
    initalized_fitness = 0

    while initalized_fitness < 99:
        initialized_environment = Environment(scenario_dimensions[0], scenario_dimensions[1])
        sensor_positions = []
        total_covered_points = 0
        total_kcovered_points = 0

        for _ in range(100):
            x = random.randint(0, initialized_environment.width)
            y = random.randint(0, initialized_environment.height)

            if (x,y) in sensor_positions:
                while (x,y) in sensor_positions:
                    x = random.randint(0, initialized_environment.width)
                    y = random.randint(0, initialized_environment.height)
                sensor_positions.append((x,y))
                sensing_range = 10
                com_range = 20
                new_sensor = Sensor(x, y, sensing_range, com_range)
                initialized_environment.add_sensor(new_sensor, k)
                initialized_environment.sensor_list.append(new_sensor)

            else:
                sensor_positions.append((x,y))
                sensing_range = 10
                com_range = 20
                new_sensor = Sensor(x, y, sensing_range, com_range)
                initialized_environment.add_sensor(new_sensor, k)
                initialized_environment.sensor_list.append(new_sensor)

        initalized_fitness = calculate_fitness(initialized_environment.sensor_list, initialized_environment)


    eval_genomes(initialized_environment, 2)

main()