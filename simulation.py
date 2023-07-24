import math

# CONSTANTS
g = 9.81  # Acceleration due to gravity (m/s^2)
dynamic_viscosity_of_water = 0.0010016 # MORE USED (Pascal*seconds @ 20°C)
kinematic_viscosity_of_water = 0.000001 # (m^2 per second)
density_of_water = 997 # (kg/m^3)

# PROBLEM CONSTANTS
water_height_remaining = 0.08  # Height of the water level remaining in the container (m)
tube_start_height_below_water_end = 0.02 # How much farther below the final water level does the tube start (m)
container_surface_area = 0.32 * 0.26 # When looking at the box from above (m^2)
theta = math.asin(1/150) # Radians
sin_theta = float(1/150) # Ratio 
tube_diameter = 0.00794 # Diameter of the tube (m)
tube_radius = 0.00397 # Radius of the tube (m)

# ESTIMATED VALUES
tube_roughness = 0.00001524
# friction_factor_estimate = 0.02 # UNUSED

def reynolds(velocity):
    return (density_of_water * tube_diameter * velocity)/dynamic_viscosity_of_water


def friction_factor(reynolds_num):
    # If turbulent
    if reynolds_num >= 4000:
        darcy = 0.0055 * (1 + (20000 * (tube_roughness/tube_diameter) + (1000000/reynolds_num))**(1/3))
        return darcy
    # If laminar use below
    return 64/reynolds_num

# SIMULATION 2 MUCH BETTER AND MORE SCIENTIFIC
def simulation(tube_length, water_height):
    # Make percentage_tube_filled = 1 if we assume the tube is full of water when we start (valve has been open for a while)
    percentage_tube_filled = 0

    time = 0 # Seconds elapsed from when we started draining
    time_step = 0.01 #(s)
    previous_velocity = 0.0001 #(m/s)
    while water_height > 0:
        tube_exit_height = water_height + tube_start_height_below_water_end + (sin_theta * tube_length * percentage_tube_filled)
        
        friction = friction_factor(reynolds(previous_velocity))
        # loss_factor = tube_diameter / (tube_diameter + (friction*tube_length))
        head_loss = (tube_length * (previous_velocity**2) * friction) / (2*g*tube_diameter)
        # water_exit_velocity = math.sqrt(2*g*tube_exit_height*loss_factor) # Formula obtained from Bernoulli
        water_exit_velocity = math.sqrt(2*g*(tube_exit_height - head_loss))

        water_exit_travel_distance = water_exit_velocity * time_step
        water_exit_volume = water_exit_travel_distance * math.pi * (tube_radius**2)
        height_removed_from_container = water_exit_volume/container_surface_area

        water_height -= height_removed_from_container
        time += time_step
        if percentage_tube_filled < 1:
            percentage_tube_filled += (water_exit_travel_distance * (1-sin_theta))/tube_length
        if percentage_tube_filled > 1:
            percentage_tube_filled = 1
        previous_velocity = water_exit_velocity

    return time

result_20cm = simulation(0.2, water_height_remaining)
print(f"LENGTH: 20 cm -> {result_20cm:.2f} seconds ({int(result_20cm//60)}:{round(result_20cm % 60)})")

result_30cm = simulation(0.3, water_height_remaining)
print(f"LENGTH: 30 cm -> {result_30cm:.2f} seconds ({int(result_30cm//60)}:{round(result_30cm % 60)})")

result_40cm = simulation(0.4, water_height_remaining)
print(f"LENGTH: 40 cm -> {result_40cm:.2f} seconds ({int(result_40cm//60)}:{round(result_40cm % 60)})")

result_60cm = simulation(0.6, water_height_remaining)
print(f"LENGTH: 60 cm -> {result_60cm:.2f} seconds ({int(result_60cm//60)}:{round(result_60cm % 60)})")