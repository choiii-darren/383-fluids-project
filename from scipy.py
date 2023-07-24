import math
from scipy.optimize import fsolve

# CONSTANTS
g = 9.81  #[ms-2]
dynamic_viscosity_of_water = 0.0010016  #[Pas]
density_of_water = 997  #[kg/m^3]

# PROBLEM CONSTANTS
water_height_remaining = 0.08 #[m]
tube_start_height_below_water_end = 0.02 #[m]
container_length = 0.32 #[m]
container_width = 0.26 #[m]
sin_theta = float(1/150)  # Ratio
tube_diameter = 0.00794  #[m]
tube_roughness = 0.0000015  #[m]

def head_loss(velocity, tube_length):
  if velocity == 0:
    return 0
  return (friction(velocity) * tube_length * velocity * velocity) / (tube_diameter * 2 * g)
  
def reynolds(velocity):
  return (density_of_water * velocity * tube_diameter) / dynamic_viscosity_of_water

def friction(velocity):
  reynolds_num = reynolds(velocity)
  # print(reynolds_num)
  if (reynolds_num <= 2300):
    return 64/reynolds_num
  elif (2300 < reynolds_num <= 4000):
    return ((64/reynolds_num)+((1/(-1.8 * math.log10(((6.9)/reynolds_num) + (((tube_roughness/tube_diameter)/3.7)**1.11))))**2))/2
  else:
    return (1/(-1.8 * math.log10(((6.9)/reynolds_num) + (((tube_roughness/tube_diameter)/3.7)**1.11))))**2
    
    #return 0.11 * (tube_roughness/tube_diameter + 68/reynolds_num)**(0.25)
  
    # def colebrook(friction, reynolds_num=reynolds_num):
    #   return -2 * math.log10(((tube_roughness/tube_diameter)/3.7) + (2.51/(reynolds_num * math.sqrt(friction)))) - (1/math.sqrt(friction))
    # return fsolve(colebrook, 0)

def simulation(tube_length):
    time = 0  # Seconds elapsed from when we started draining
    time_step = 0.001  # (s)
    height = water_height_remaining + tube_start_height_below_water_end + tube_length*sin_theta
    end_height = height - water_height_remaining
    previous_exit_velocity = math.sqrt(2*g*height)*0.5
    #previous_tank_loss_velocity = 0
    while (height > end_height):
        # print(previous_exit_velocity)
        friction_head_loss = head_loss(previous_exit_velocity, tube_length)
        # print(friction_head_loss)
        minor_head_loss = 0 #(0.5 * previous_tank_loss_velocity * previous_tank_loss_velocity) / (2 * g)
        exit_velocity = (math.sqrt((2*g*(height - friction_head_loss - minor_head_loss)))) #if friction_head_loss < height else previous_exit_velocity*0.55
        container_area = container_length * container_width
        tube_area = math.pi * tube_diameter * tube_diameter * (1/4)
        tank_loss_velocity = (tube_area/container_area) * exit_velocity
        height_loss = tank_loss_velocity * time_step

        #Setup next step
        height -= height_loss
        time += time_step
        previous_exit_velocity = exit_velocity
        #previous_tank_loss_velocity = tank_loss_velocity
    return time


result_20cm = simulation(0.2)
print(
    f"LENGTH: 20 cm -> {result_20cm:.2f} seconds ({int(result_20cm//60)}:{round(result_20cm % 60):02})")

result_30cm = simulation(0.3)
print(
    f"LENGTH: 30 cm -> {result_30cm:.2f} seconds ({int(result_30cm//60)}:{round(result_30cm % 60):02})")

result_40cm = simulation(0.4)
print(
    f"LENGTH: 40 cm -> {result_40cm:.2f} seconds ({int(result_40cm//60)}:{round(result_40cm % 60):02})")

result_60cm = simulation(0.6)
print(
    f"LENGTH: 60 cm -> {result_60cm:.2f} seconds ({int(result_60cm//60)}:{round(result_60cm % 60):02})")
