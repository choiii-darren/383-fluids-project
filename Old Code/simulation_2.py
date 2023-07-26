import math
from scipy.optimize import fsolve

# CONSTANTS
g = 9.81  #[ms-2]
dynamic_viscosity_of_water = 0.0010016  #[Pa*s]
density_of_water = 997  #[kg/m^3]

# PROBLEM CONSTANTS
water_height_remaining = 0.08 #[m]
tube_start_height_below_water_end = 0.02 #[m]
container_length = 0.32 #[m]
container_width = 0.26 #[m]
sin_theta = float(1/150)  # Ratio
tube_diameter = 0.00794  #[m]
tube_roughness = 0.0000015  #[m]
container_area = container_length * container_width
tube_area = math.pi * (1/4) * tube_diameter ** 2

def head_loss(velocity, tube_length):
  if velocity == 0:
    return 0
  return (friction(velocity) * tube_length * velocity **2) / (tube_diameter * 2 * g)
  
def reynolds(velocity):
  return (density_of_water * velocity * tube_diameter) / dynamic_viscosity_of_water

def friction(velocity):
  reynolds_num = reynolds(velocity)
  if (reynolds_num <= 2300):
    return 64/reynolds_num
  else:
    return (1/(-1.8 * math.log10(((6.9)/reynolds_num) + (((tube_roughness/tube_diameter)/3.7)**1.11))))**2
    
    # return 0.11 * (tube_roughness/tube_diameter + 68/reynolds_num)**(0.25)
  
    # def colebrook(friction, reynolds_num=reynolds_num):
    #   return -2 * math.log10(((tube_roughness/tube_diameter)/3.7) + (2.51/(reynolds_num * math.sqrt(friction)))) - (1/math.sqrt(friction))
    # return fsolve(colebrook, 0.02)


def simulation(tube_length):
    time = 0  # Seconds elapsed from when we started draining
    time_step = 0.01  # (s)
    height = water_height_remaining + tube_start_height_below_water_end + tube_length*sin_theta
    end_height = height - water_height_remaining
    previous_exit_velocity = math.sqrt(2*g*height)
    while (height > end_height):
        def velocity(velocity):
          major_head_loss = head_loss(velocity, tube_length)
          minor_head_loss = (0.5 * velocity**2) / (2 * g)
          if major_head_loss + minor_head_loss> height:
            return 10000 # Will indicate that this is not the root

          return math.sqrt((2*g*(height - major_head_loss - minor_head_loss))) - velocity
        
        exit_velocity = fsolve(velocity, previous_exit_velocity)
        tank_loss_velocity = (tube_area/container_area) * exit_velocity
        height_loss = tank_loss_velocity * time_step

        #Setup next step
        height -= height_loss
        time += time_step
        previous_exit_velocity = exit_velocity

    return time

result_10cm = simulation(0.1)
print(
    f"LENGTH: 10 cm -> {result_10cm:.2f} seconds ({int(result_10cm//60)}:{round(result_10cm % 60):02}) -> ??")

result_20cm = simulation(0.2)
actual_20 = 199
print(
    f"LENGTH: 20 cm -> {result_20cm:.2f} seconds ({int(result_20cm//60)}:{round(result_20cm % 60):02}) -> 3:19")

result_30cm = simulation(0.3)
actual_30 = 214
print(
    f"LENGTH: 30 cm -> {result_30cm:.2f} seconds ({int(result_30cm//60)}:{round(result_30cm % 60):02}) -> 3:34")

result_40cm = simulation(0.4)
actual_40 = 266
print(
    f"LENGTH: 40 cm -> {result_40cm:.2f} seconds ({int(result_40cm//60)}:{round(result_40cm % 60):02}) -> 4:26")

result_60cm = simulation(0.6)
actual_60 = 288
print(
    f"LENGTH: 60 cm -> {result_60cm:.2f} seconds ({int(result_60cm//60)}:{round(result_60cm % 60):02}) -> 4:48")
print("Total Error: ", abs(result_20cm-actual_20) + abs(result_30cm-actual_30) + abs(result_40cm-actual_40) + abs(result_60cm-actual_60))