import random
import matplotlib.pyplot as plt
import numpy as np
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
        self.active_sensor_count = 0
        self.active_sensor_list = []


    # adds sensor to environment
    def add_sensor(self, sensor, k):
        global total_covered_points
        global total_kcovered_points
        self.active_sensor_count += 1
        self.active_sensor_list.append(sensor)

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

    best_scenario = initial_sol
    best_fitness = calculate_fitness(initial_sol.sensor_list, initial_sol)

    mutationRepeatLimit = 1
    mutation_rate = 0.05
    gen_count = 0
    
    # itereate through all solutions
    while mutation_rate > 0: 
        gen_count += 1

        for solution in range(10*math.ceil((math.log(len(best_scenario.sensor_list))))):
            total_kcovered_points = 0
            total_covered_points = 0
        
            # copy the universal best solution to an environment
            environment = Environment(best_scenario.height, best_scenario.width)
            for sensor in best_scenario.sensor_list:
                new_sensor = Sensor(sensor.x, sensor.y, sensor.sensing_range, sensor.com_range)
                new_sensor.active = sensor.active
                environment.sensor_list.append(new_sensor)
                if new_sensor.active:
                    environment.active_sensor_list.append(new_sensor)


            # mutate
            mutate_sensors(environment, mutation_rate)

            # do changes to current environment
            for sensor in environment.sensor_list:
                if sensor.active:
                    environment.add_sensor(sensor, k)

            # compare fitness of current to best
            genome_fitness = calculate_fitness(environment.sensor_list, environment)

            if genome_fitness > best_fitness:
                best_fitness = genome_fitness
                best_scenario = environment

        if gen_count % mutationRepeatLimit == 0:
            mutation_rate = (math.ceil((mutation_rate - 0.01) * 100))/100

        # reset grid for next round
        best_scenario.grid = np.zeros((best_scenario.height, best_scenario.width))

    print("active sensors and gen count", best_scenario.active_sensor_count, gen_count)
    return best_scenario


def mutate_sensors(environment, mutation_rate):
    # number of sensors that will be mutated
    number_mutations = math.ceil(len(environment.sensor_list) * mutation_rate)
    # threshold of on sensors
    threshold = number_mutations / 2 - 1 if number_mutations % 2 == 0 else math.floor(number_mutations / 2)
    
    random.shuffle(environment.sensor_list)
    
    num_turned_on = 0
    
    for selected_sensor in range(number_mutations):
        if num_turned_on < threshold:
            sensor = environment.sensor_list[selected_sensor]
        else:
            # select sensor from active list if at threshold
            if environment.active_sensor_list:
                sensor = environment.active_sensor_list[random.randint(0, len(environment.active_sensor_list) - 1)]
            else:
                break

        # mutate
        sensor.active = not sensor.active
        
        # if sensor turned ON
        if sensor.active:
            environment.active_sensor_list.append(sensor)
            num_turned_on += 1

        # if sensor turned OFF
        else:
            if sensor in environment.active_sensor_list:
                environment.active_sensor_list.remove(sensor)

    return environment.sensor_list


# caclulates fitness of scenarios after 
def calculate_fitness(sensors, environment):
    global total_covered_points
    global total_kcovered_points

    connectivity_score = calculate_connectivity_score(sensors, sensors[0].com_range)
    k_coverage_rate = total_kcovered_points / (environment.height * environment.width)
    coverage_rate = total_covered_points / (environment.height * environment.width)

    inactivity = (len(sensors) - environment.active_sensor_count) / len(sensors)

    if connectivity_score == 1.0:
        connectivity_score *= 100
    if k_coverage_rate == 1.0:
        k_coverage_rate *= 100
    if coverage_rate == 1.0:
        coverage_rate *= 100

    fitness_score = (
        connectivity_score * 0.33 +
        k_coverage_rate * 0.39 +
        coverage_rate * 0.27 +
        inactivity * 1
    )

    print(connectivity_score, k_coverage_rate, coverage_rate, environment.active_sensor_count, fitness_score)
    return fitness_score


def main(k, num_sensors, sensing_range, com_range, scenario_dimensions):
    global total_covered_points
    global total_kcovered_points

    # k = 4
    # num_sensors = 100
    # sensing_range = 10
    # com_range = 20
    # scenario_dimensions = (50, 50)

    sensor_positions = []
    initalized_fitness = 0

    while initalized_fitness < 99:
        initialized_environment = Environment(scenario_dimensions[0], scenario_dimensions[1])
        sensor_positions = []
        total_covered_points = 0
        total_kcovered_points = 0

        for _ in range(num_sensors):
            x = random.randint(0, initialized_environment.width)
            y = random.randint(0, initialized_environment.height)

            if (x,y) in sensor_positions:
                while (x,y) in sensor_positions:
                    x = random.randint(0, initialized_environment.width)
                    y = random.randint(0, initialized_environment.height)
                sensor_positions.append((x,y))
                new_sensor = Sensor(x, y, sensing_range, com_range)
                initialized_environment.add_sensor(new_sensor, k)
                initialized_environment.sensor_list.append(new_sensor)

            else:
                sensor_positions.append((x,y))
                new_sensor = Sensor(x, y, sensing_range, com_range)
                initialized_environment.add_sensor(new_sensor, k)
                initialized_environment.sensor_list.append(new_sensor)

        initalized_fitness = calculate_fitness(initialized_environment.sensor_list, initialized_environment)

    return eval_genomes(initialized_environment, k).active_sensor_count

# test1_2 = (str(main(2, 100, 10, 20, (50,50))) + "+" + str(main(2, 100, 10, 20, (50,50)))
# + "+" + str(main(2, 100, 10, 20, (50,50))) + "+" + str(main(2, 100, 10, 20, (50,50))) 
# + "+" + str(main(2, 100, 10, 20, (50,50))) + "+" + str(main(2, 100, 10, 20, (50,50))) 
# + "+" + str(main(2, 100, 10, 20, (50,50))) + "+" + str(main(2, 100, 10, 20, (50,50))) 
# + "+" + str(main(2, 100, 10, 20, (50,50))) + "+" + str(main(2, 100, 10, 20, (50,50))))

# test1_3 = (str(main(3, 100, 10, 20, (50,50))) + "+" + str(main(3, 100, 10, 20, (50,50)))
# + "+" + str(main(3, 100, 10, 20, (50,50))) + "+" + str(main(3, 100, 10, 20, (50,50))) 
# + "+" + str(main(3, 100, 10, 20, (50,50))) + "+" + str(main(3, 100, 10, 20, (50,50))) 
# + "+" + str(main(3, 100, 10, 20, (50,50))) + "+" + str(main(3, 100, 10, 20, (50,50))) 
# + "+" + str(main(3, 100, 10, 20, (50,50))) + "+" + str(main(3, 100, 10, 20, (50,50))))

# test1_4 = (str(main(4, 100, 10, 20, (50,50))) + "+" + str(main(4, 100, 10, 20, (50,50)))
# + "+" + str(main(4, 100, 10, 20, (50,50))) + "+" + str(main(4, 100, 10, 20, (50,50))) 
# + "+" + str(main(4, 100, 10, 20, (50,50))) + "+" + str(main(4, 100, 10, 20, (50,50))) 
# + "+" + str(main(4, 100, 10, 20, (50,50))) + "+" + str(main(4, 100, 10, 20, (50,50))) 
# + "+" + str(main(4, 100, 10, 20, (50,50))) + "+" + str(main(4, 100, 10, 20, (50,50))))

# test2_2 = (str(main(2, 300, 15, 30, (100,100))) + "+" + str(main(2, 300, 15, 30, (100,100)))
# + "+" + str(main(2, 300, 15, 30, (100,100))) + "+" + str(main(2, 300, 15, 30, (100,100))) 
# + "+" + str(main(2, 300, 15, 30, (100,100))) + "+" + str(main(2, 300, 15, 30, (100,100))) 
# + "+" + str(main(2, 300, 15, 30, (100,100))) + "+" + str(main(2, 300, 15, 30, (100,100))) 
# + "+" + str(main(2, 300, 15, 30, (100,100))) + "+" + str(main(2, 300, 15, 30, (100,100))))

# test2_3 = (str(main(3, 300, 15, 30, (100,100))) + "+" + str(main(3, 300, 15, 30, (100,100)))
# + "+" + str(main(3, 300, 15, 30, (100,100))) + "+" + str(main(3, 300, 15, 30, (100,100))) 
# + "+" + str(main(3, 300, 15, 30, (100,100))) + "+" + str(main(3, 300, 15, 30, (100,100))) 
# + "+" + str(main(3, 300, 15, 30, (100,100))) + "+" + str(main(3, 300, 15, 30, (100,100))) 
# + "+" + str(main(3, 300, 15, 30, (100,100))) + "+" + str(main(3, 300, 15, 30, (100,100))))

# test2_4 = (str(main(4, 300, 15, 30, (100,100))) + "+" + str(main(4, 300, 15, 30, (100,100)))
# + "+" + str(main(4, 300, 15, 30, (100,100))) + "+" + str(main(4, 300, 15, 30, (100,100))) 
# + "+" + str(main(4, 300, 15, 30, (100,100))) + "+" + str(main(4, 300, 15, 30, (100,100))) 
# + "+" + str(main(4, 300, 15, 30, (100,100))) + "+" + str(main(4, 300, 15, 30, (100,100))) 
# + "+" + str(main(4, 300, 15, 30, (100,100))) + "+" + str(main(4, 300, 15, 30, (100,100))))

# test3_2 = (str(main(2, 500, 20, 40, (150,150))) + "+" + str(main(2, 500, 20, 40, (150,150)))
# + "+" + str(main(2, 500, 20, 40, (150,150))) + "+" + str(main(2, 500, 20, 40, (150,150))) 
# + "+" + str(main(2, 500, 20, 40, (150,150))) + "+" + str(main(2, 500, 20, 40, (150,150))) 
# + "+" + str(main(2, 500, 20, 40, (150,150))) + "+" + str(main(2, 500, 20, 40, (150,150))) 
# + "+" + str(main(2, 500, 20, 40, (150,150))) + "+" + str(main(2, 500, 20, 40, (150,150))))

# test3_3 = (str(main(3, 500, 20, 40, (150,150))) + "+" + str(main(3, 500, 20, 40, (150,150)))
# + "+" + str(main(3, 500, 20, 40, (150,150))) + "+" + str(main(3, 500, 20, 40, (150,150))) 
# + "+" + str(main(3, 500, 20, 40, (150,150))) + "+" + str(main(3, 500, 20, 40, (150,150))) 
# + "+" + str(main(3, 500, 20, 40, (150,150))) + "+" + str(main(3, 500, 20, 40, (150,150))) 
# + "+" + str(main(3, 500, 20, 40, (150,150))) + "+" + str(main(3, 500, 20, 40, (150,150))))

# test3_4 = (str(main(4, 500, 20, 40, (150,150))) + "+" + str(main(4, 500, 20, 40, (150,150)))
# + "+" + str(main(4, 500, 20, 40, (150,150))) + "+" + str(main(4, 500, 20, 40, (150,150))) 
# + "+" + str(main(4, 500, 20, 40, (150,150))) + "+" + str(main(4, 500, 20, 40, (150,150))) 
# + "+" + str(main(4, 500, 20, 40, (150,150))) + "+" + str(main(4, 500, 20, 40, (150,150))) 
# + "+" + str(main(4, 500, 20, 40, (150,150))) + "+" + str(main(4, 500, 20, 40, (150,150))))

# test4_20 = "+".join(str(main(3, 300, 20, 40, (100, 100))) for _ in range(10))
# test4_30 = "+".join(str(main(3, 300, 30, 60, (100, 100))) for _ in range(10))
# test4_40 = "+".join(str(main(3, 300, 40, 80, (100, 100))) for _ in range(10))
# test4_50 = "+".join(str(main(3, 300, 50, 100, (100, 100))) for _ in range(10))
# test4_60 = "+".join(str(main(3, 300, 60, 120, (100, 100))) for _ in range(10))

test1_2 = "+".join(str(main(2, 100, 10, 20, (50, 50))) for _ in range(10))


print(test1_2)
