import math
from scipy.optimize import fsolve
import warnings

#ignores warnings
warnings.filterwarnings("ignore")

# WORLD CONSTANTS
g = 9.81 #[m/s^2]
dynamic_viscosity_of_water = 0.0010016 #[Pa*s]
density_of_water = 997 #[kg/m^3]

# PROBLEM CONSTANTS
start_height = 0.08 #[m]
distance_to_tube = 0.02 #[m]
container_length = 0.32 #[m]
container_width = 0.13 #[m]
container_area = container_length * container_width
sin_theta = float(1/150) #[]
original_diameter = 0.00794  #[m]
original_tube_area = (math.pi * (1/4) * original_diameter ** 2) #[m^2]

# T-JUNCTION CONVERTED PROBLEM
tube1_area = original_tube_area / 2 #[m^2]
tube1_diameter = math.sqrt((tube1_area * 4) / math.pi) #[m]
tube2_diameter = 0.0111125 #[m]
tube2_area = (math.pi * (1/4) * tube2_diameter ** 2)
tube2_length = 0.04 #[m]

# CHOSEN VALUES
tube_roughness = 0.0000025 #[m]
time_step = 0.01


def second_tube_velocity(tube1_velocity, tube1_area=tube1_area, tube2_area=tube2_area):
  return (tube1_area / tube2_area) * tube1_velocity

def major_head_loss(velocity, tube_length, tube_diameter=tube1_diameter):
  if velocity == 0:
    return 0
  return (friction(velocity, tube_diameter) * tube_length * velocity **2) / (tube_diameter * 2 * g)

def minor_head_loss(velocity, k):
  return (k * velocity ** 2) / (2 * g)

def sudden_expansion_head_loss(tube_velocity, tube1_diameter=tube1_diameter, tube2_diameter=tube2_diameter):
  return ((tube_velocity**2)/(2*g))*(1 - (tube1_diameter/tube2_diameter))

def reynolds(velocity, tube_diameter=tube1_diameter):
  return (density_of_water * velocity * tube_diameter) / dynamic_viscosity_of_water

def friction(velocity, tube_diameter=tube1_diameter):
  reynolds_num = reynolds(velocity, tube_diameter)
  if (reynolds_num <= 2300):
    return 64/reynolds_num
  else:
    return (1/(-1.8 * math.log10(((6.9)/reynolds_num) + (((tube_roughness/tube_diameter)/3.7)**1.11))))**2

    # return 0.11 * (tube_roughness/original_diameter + 68/reynolds_num)**(0.25)

    # def colebrook(friction, reynolds_num=reynolds_num):
    #   return -2 * math.log10(((tube_roughness/original_diameter)/3.7) + (2.51/(reynolds_num * math.sqrt(friction)))) - (1/math.sqrt(friction))
    # return fsolve(colebrook, 0.02)

def simulation(tube1_length):
    time = 0  # Seconds elapsed from when we started draining
    height = start_height + distance_to_tube + tube1_length*sin_theta
    end_height = height - start_height
    previous_exit_velocity = math.sqrt(2*g*height)
    while (height > end_height):
        def velocity(tube1_velocity):
          tube2_velocity = second_tube_velocity(tube1_velocity)
          major_head_loss_1 = major_head_loss(tube1_velocity, tube1_length, tube1_diameter) #First we experience tube 1 friction
          minor_head_loss_1 = minor_head_loss(tube1_velocity,0.5)                           #Then we experience tube 1 minor loss
          bend_head_loss = minor_head_loss(tube1_velocity, 1.1)                             #Then I take a right angle turn
          expansion_head_loss = sudden_expansion_head_loss(tube1_velocity)                  #Then I suddenly enter a large pipe
          major_head_loss_2 = major_head_loss(tube2_velocity, tube2_length, tube2_diameter) #Then I experience tube 2 friction
          minor_head_loss_2 = minor_head_loss(tube2_velocity,0.5)                           #Then I experience tube 2 minor loss
          
          try:
            return math.sqrt((2*g*(height - (major_head_loss_1 + minor_head_loss_1 + major_head_loss_2 + minor_head_loss_2 + bend_head_loss + expansion_head_loss)))) - tube1_velocity
          except:
            #fsolve approximates values for the velocity which can lead to math domain errors
            #the below indicates that the answer is incorrect to fsolve
            return 10000
        
        tube1_exit_velocity = fsolve(velocity, previous_exit_velocity) #Solve the velocity in tube1, using the previous velocity as a starting guess
        tank_loss_velocity = (tube1_area/container_area) * tube1_exit_velocity
        height_loss = tank_loss_velocity * time_step

        #Setup next step
        height -= height_loss
        time += time_step
        previous_exit_velocity = tube1_exit_velocity

    return time

result_20cm = simulation(0.2)
print(
    f"LENGTH: 20 cm -> {result_20cm:.2f} seconds ({int(result_20cm//60)}:{round(result_20cm % 60):02}) -> Real Life (w/o T Junction): 3:19")

result_40cm = simulation(0.4)
print(
    f"LENGTH: 40 cm -> {result_40cm:.2f} seconds ({int(result_40cm//60)}:{round(result_40cm % 60):02}) -> Real Life (w/o T Junction): 4:26")
