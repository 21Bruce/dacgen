import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as fft
import argparse

parser = argparse.ArgumentParser(
        prog='DAC Sinusoid Output Simulator',
        description='Easily simulate the output of a DAC sampled sinusoid w/ plotting and PWL capabilities'
        )

parser.add_argument("-f", "--frequency", help="specify the frequency of the sinusoid in Hz. Default is 1000", dest="freq", default=1000, type=int)
parser.add_argument("-n", "--ncycle", help="specify the number of cycles of the sinusoid. Default is 10", dest="ncycles", default=10, type=int)
parser.add_argument("-a", "--amplitude", help="specify the amplitude of the sinusoid. Default is 2.5", dest="amp", default=2.5, type=int)
parser.add_argument("-dc", "--dcoff", dest="dc", help="specify the dc offset of the sinusoid. Default is 0", default=0, type=int)
parser.add_argument("-spc", "--samplepercycle", help="specify the samples per cycle of the sinusoid. Default is 200", dest="spc", default=200, type=int)
parser.add_argument("-p", "--plot", dest="plot", help="specify whether to plot the sinusoidal signal and its FFT", action="store_true")
parser.add_argument("-fi", "--file", dest="file", help="specify whether to save the sinusoidal signal to a PWL file", action="store_true")

args = parser.parse_args()

# frequency 
freq = float(args.freq) 
# number of cycles 
ncycles = float(args.ncycles) 
# amplitude
amp = float(args.amp) 
# dc offset
dc = float(args.dc) 
#sample per cycle
spc = float(args.spc) 

########## CONFIG ##########

samples = amp * np.sin((2.0*np.pi/spc) * np.linspace(0,spc-1, num=int(spc))) + np.ones(int(spc))*dc

# resolution
res = 50.0 

# period
T = 1.0/float(freq)

# duration 
duration = T * ncycles

# amount of steps in output 
steps = int(spc * ncycles)

time = np.linspace(start=0, stop=duration, num=int(res*steps))

dac = np.zeros(len(time))

Fs = (res*steps)/duration 

L = []
for i in range(0, len(dac), 1):
    dac[i] = samples[int(i/res) % int(spc)]
  	L.append(str(time[i]) + " " + str(dac[i]) + "\n")

if args.plot:
    fig = plt.figure(figsize=(1, 2))
    axs = fig.subplot_mosaic([["signal", "magnitude"]
                              ])
    
    axs["signal"].set_title("Signal")
    axs["signal"].plot(time, dac, color='C0')
    axs["signal"].set_xlabel("Time (s)")
    axs["signal"].set_ylabel("Amplitude")
    
    axs["magnitude"].set_title("Magnitude Spectrum")
    axs["magnitude"].magnitude_spectrum(dac, Fs=Fs, color='C1')
    axs["magnitude"].set_xlim([-1, 10*spc*freq])
                              
    plt.show()

if args.file:
    file1 = open("dac_pwl" + str(int(freq)) + ".txt", "w")
    file1.writelines(L)
    file1.close()
