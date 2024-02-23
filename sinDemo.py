import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as anim
from TL import System
from TL import TransmissionLine
from TL import GeneratorJunction
from TL import ResistiveJunction
from TL import GeneratorJunction
from TL import SinusoidalGenerator


#tline constants
length = 5 #length in meters
Vp = 1 #2/3 speed of light in meters per second
z0 = 50

#generator constants
amplitude = 1
frequency = 1
phase = 0
Rg = 100 #match at load




#load constants
Rl = 100

#timing constants
frame_rate = 1/45
dt = 0.001
#dt = (length / Vp) / 100 #the tline will be made by 100 segments
t_end = 20
time_dilation = 1
#time_dilation = (length / Vp) / 7 #will make the time from one end to other 7 seconds

print(time_dilation)
print(dt)


tline1 = TransmissionLine(length = length, Vp = Vp, Z0 = z0, dt = dt)
generator = SinusoidalGenerator(RG = Rg, Z0 = tline1.get_Z0(), frequency = frequency, amplitude = amplitude, phase = phase)
load = ResistiveJunction(RL = Rl, Z0 = tline1.get_Z0())
structure = {tline1: ((generator, 1), (load, 1))} #store structure in form:


system = System(structure = structure, dt = dt / 2, time_dilation = time_dilation)


fig, ax = plt.subplots(figsize = (7, 5))
wave, = ax.plot(tline1.get_x_axis(), tline1.get_line_voltage(), "-", color = "C3", lw = 2)
#wave_plus, = ax.plot(tline1.get_x_axis(), tline1.get_v_plus(), "-", color = "C2", lw = 2)
#wave_minus, = ax.plot(tline1.get_x_axis(), tline1.get_v_minus(), "-", color = "C1", lw = 2)


ax.set_yticks((-2, -1, -0.5, 0, 0.5, 1, 2))
ax.grid(True)
ax.set_title(f"Total voltage on Tline\n(1 second real time = {1/time_dilation} seconds simulation time)")

def update(t):
    system.tick_system_time_dependent()
    wave.set_ydata(tline1.get_line_voltage())
    #wave_plus.set_ydata(tline1.get_v_plus())
    #wave_minus.set_ydata(tline1.get_v_minus())
    #return (wave, wave_plus, wave_minus)
    return(wave,)

ani = anim.FuncAnimation(fig, update, 
                            frames = int(t_end / frame_rate),
                            interval = int(frame_rate * 1000), blit = True)

plt.show()