import math
from scipy.optimize import fsolve

# WORLD CONSTANTS
g = 9.81 #[m/s^2]
dynamic_viscosity_of_water = 0.0010016 #[Pa*s]
density_of_water = 997 #[kg/m^3]

# PROBLEM CONSTANTS
start_height = 0.08 #[m]
distance_to_tube = 0.02 #[m]
container_length = 0.32 #[m]
container_width = 0.26 #[m]
container_area = container_length * container_width #[m^2]
sin_theta = float(1/150) #[]
tube1_diameter = 0.00794 #[m]
tube_area = math.pi * (1/4) * tube1_diameter ** 2 #[m^2]

# CHOSEN VALUES
tube_roughness = 0.0000025 #[m]
time_step = 0.01 #[s]


def major_head_loss(velocity, tube1_length, tube_diameter=tube1_diameter):
  if velocity == 0:
    return 0
  return (friction(velocity, tube_diameter) * tube1_length * velocity ** 2) / (tube_diameter * 2 * g)


def minor_head_loss(velocity, k):
  return (k * velocity ** 2) / (2 * g)

def reynolds(velocity, tube_diameter=tube1_diameter):
  return (density_of_water * velocity * tube_diameter) / dynamic_viscosity_of_water

def friction(velocity, tube_diameter=tube1_diameter):
  reynolds_num = reynolds(velocity, tube1_diameter)
  if (reynolds_num <= 2300):
    return 64/reynolds_num
  else:
    return (1/(-1.8 * math.log10(((6.9)/reynolds_num) + (((tube_roughness/tube1_diameter)/3.7)**1.11))))**2
    
    # return 0.11 * (tube_roughness/tube_diameter + 68/reynolds_num)**(0.25)
  
    # def colebrook(friction, reynolds_num=reynolds_num):
    #   return -2 * math.log10(((tube_roughness/tube_diameter)/3.7) + (2.51/(reynolds_num * math.sqrt(friction)))) - (1/math.sqrt(friction))
    # return fsolve(colebrook, 0.02)

def simulation(tube1_length):
    time = 0  #Seconds elapsed from when we started draining
    height = start_height + distance_to_tube + tube1_length*sin_theta
    end_height = height - start_height
    previous_exit_velocity = math.sqrt(2*g*height)
    while (height > end_height):
        def velocity(tube1_velocity):
          major_head_loss_1 = major_head_loss(tube1_velocity, tube1_length)
          minor_head_loss_1 = minor_head_loss(tube1_velocity, 0.5)

          try:
            return math.sqrt((2*g*(height - major_head_loss_1 - minor_head_loss_1))) - tube1_velocity
          except:
            #fsolve approximates values for the velocity which can lead to math domain errors
            #the below indicates that the answer is incorrect to fsolve
            return 10000

        tube1_exit_velocity = fsolve(velocity, previous_exit_velocity)
        tank_loss_velocity = (tube_area/container_area) * tube1_exit_velocity
        height_loss = tank_loss_velocity * time_step

        #Setup next step
        height -= height_loss
        time += time_step
        previous_exit_velocity = tube1_exit_velocity

    return time

result_10cm = simulation(0.1)
print(
    f"LENGTH: 10 cm -> {result_10cm:.2f} seconds ({int(result_10cm//60)}:{round(result_10cm % 60):02}) -> Real Life: ??")

result_20cm = simulation(0.2)
actual_20 = 199
print(
    f"LENGTH: 20 cm -> {result_20cm:.2f} seconds ({int(result_20cm//60)}:{round(result_20cm % 60):02}) -> Real Life: 3:19")

result_30cm = simulation(0.3)
actual_30 = 214
print(
    f"LENGTH: 30 cm -> {result_30cm:.2f} seconds ({int(result_30cm//60)}:{round(result_30cm % 60):02}) -> Real Life: 3:34")

result_40cm = simulation(0.4)
actual_40 = 266
print(
    f"LENGTH: 40 cm -> {result_40cm:.2f} seconds ({int(result_40cm//60)}:{round(result_40cm % 60):02}) -> Real Life: 4:26")

result_60cm = simulation(0.6)
actual_60 = 288
print(
    f"LENGTH: 60 cm -> {result_60cm:.2f} seconds ({int(result_60cm//60)}:{round(result_60cm % 60):02}) -> Real Life: 4:48")
print("Total Absolute Error: ", abs(result_20cm-actual_20) + abs(result_30cm-actual_30) + abs(result_40cm-actual_40) + abs(result_60cm-actual_60))