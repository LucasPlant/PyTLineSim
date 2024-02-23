import time
from collections import deque
import numpy as np

"""
To DO:
    allow for multiple shifts in 0(1) via allowing the passage of lists
    optimize code
    allow for more accurate real values via time dialation ect
    allow importing json files for configurations


    vision for overall architecture
    1 file containing the t line and junction deffenitions and system
    another file that creates a structure and determines how it should be graphed 
        perhaps pass the system time into system and have it be agnostic to time 

"""

class Junction:

    def __init__():
        pass

    def receive_wave(self, tline_index, value_in):
        pass

    def send_wave(self, tline_index, sim_time):
        pass



class GeneratorJunction(Junction):

    def __init__(self, Vg, RG, Z0):
        self.voltage_source = Vg #voltage of source
        self.RG = RG #generator resistance
        self.Z0 = Z0

        self.gamma_g = (RG - Z0)/(RG + Z0)
        self.initial_wave = Vg * Z0 / (Z0 + RG)
        self.wave_in = 0

    def receive_wave(self, tline_index, value_in):
        self.wave_in = value_in

    def send_wave(self, tline_index, sim_time):
        return self.wave_in * self.gamma_g + self.initial_wave #make this support lists



class ResistiveJunction(Junction):
    
    def __init__(self, RL, Z0):
        self.RL = RL #load resistance
        self.Z0 = Z0

        self.gamma_g = (RL - Z0)/(RL + Z0)
        self.wave_in = 0

    def receive_wave(self, tline_index, value_in):
        self.wave_in = value_in

    def send_wave(self, tline_index, sim_time):
        return self.wave_in * self.gamma_g


class TransmissionLine:
    
    def __init__(self, length, dt, Vp = None, Z0 = None): #add other arguments to implement other characteristics
        print("tline")
        propagation_delay = length / Vp
        size = int(propagation_delay / dt)
        self.v_plus = deque([0] * size)
        self.v_minus = deque([0] * size)
        self.total_voltage = [plus + minus for plus, minus in zip(self.v_plus, self.v_minus)]
        self.x_axis = np.linspace(0, length, size)
        self.Z0 = Z0

    def shift_v_plus(self): #maybe optimize by allowing multiple shifts
        return self.v_plus.pop()

    def shift_v_minus(self):
        return self.v_minus.popleft()

    def shift_in_v_plus(self, value_in: float):
        self.v_plus.appendleft(value_in)

    def shift_in_v_minus(self, value_in: float):
        self.v_minus.append(value_in)

    def get_x_axis(self):
        return self.x_axis

    def get_v_plus(self):
        return self.v_plus
    
    def get_v_minus(self):
        return self.v_minus
    
    def get_Z0(self):
        return self.Z0
    
    def get_line_voltage(self):
        self.total_voltage = [plus + minus for plus, minus in zip(self.v_plus, self.v_minus)]
        return self.total_voltage


class System:

    def __init__(self, structure, dt, time_dilation = 1): #for now tline will be hardcoded
        #tline -> ((left junction, number in junction), (end junction, number in junction))
        self.dt = dt
        self.time_dilation = time_dilation
        self.structure = structure
        self.start_time = time.time()
        self.total_ticks = 0

    def tick_system(self):
        #print("system ticked")
        #shift values out of tlines
        self.total_ticks += 1

        for Tline, junctions in self.structure.items():
            left, right = junctions
            left_junction, left_number = left
            right_junction, right_number = right
            right_junction.receive_wave(tline_index = right_number, value_in = Tline.shift_v_plus())
            left_junction.receive_wave(tline_index = left_number, value_in = Tline.shift_v_minus())

        #shift values into tlines
        for Tline, junctions in self.structure.items():
            left, right = junctions
            left_junction, left_number = left
            right_junction, right_number = right
            Tline.shift_in_v_plus(value_in = left_junction.send_wave(tline_index = left_number, sim_time = self.get_sim_time()))
            Tline.shift_in_v_minus(value_in = right_junction.send_wave(tline_index = right_number, sim_time = self.get_sim_time()))

    
    def tick_system_time_dependent(self):
        amount_to_tick = int((time.time() - self.start_time) * self.time_dilation / self.dt) - self.total_ticks
        for i in range(amount_to_tick):
            self.tick_system()

    def get_sim_time(self):
        return self.total_ticks * self.dt
