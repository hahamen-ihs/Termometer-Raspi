import sys
from matplotlib import pyplot
from time import sleep
import Tkinter
import datetime
import time
import spidev, time

spi = spidev.SpiDev()
spi.open(0, 0)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

def saat_tombol_mulai():
    while True:
        if flag.get():
            sleep(0.001)
            reading = analog_read(0)
            suhu = reading * 3.3 *100/ 1024
            outf = open("data_suhu.txt", "ab")
            outf.write("%f\n" % (suhu))
            print suhu
            pData.append(float(suhu))
            pyplot.ylim([0, 50])
            del pData[0]
            l1.set_xdata([i for i in xrange(25)])
            l1.set_ydata(pData)  # update data
            pyplot.title("GRAFIK DATA SENSOR SUHU LM35 BERBASIS ADC MCP3008")
            pyplot.xlabel("Waktu (s)")
            pyplot.ylabel("Suhu (Celcius)")
            pyplot.savefig('grafik_suhu.png',format='png')
            pyplot.draw()  # update plot
            top.update()
        else:
            flag.set(True)
            break


def saat_tombol_pause():
    flag.set(False)


def saat_tombol_keluar():
    print "Keluar"
    saat_tombol_pause()
    pyplot.close(fig)
    top.quit()
    top.destroy()
    print "Selesai"
    sys.exit()

# Judul GUI Tkinter 
top = Tkinter.Tk()
top.title("GUI Python Kontrol")

# Membuat flag agar dapat bekerja dengan while loop
flag = Tkinter.BooleanVar(top)
flag.set(True)

pyplot.ion()
pData = [0.0] * 25
fig = pyplot.figure()
ax1 = pyplot.axes()
l1, = pyplot.plot(pData)
pyplot.ylim([0, 50])

# GUI Mulai terhubung dengan fungsi saat tombol mulai
tombol_mulai = Tkinter.Button(top,
                             text="Mulai",
                             command=saat_tombol_mulai)
tombol_mulai.grid(column=1, row=2)

# GUI Pause terhubung dengan fungsi saat tombol pause
tombol_pause = Tkinter.Button(top,
                             text="Pause",
                             command=saat_tombol_pause)
tombol_pause.grid(column=2, row=2)

# GUI Keluar terhubung dengan fungsi saat tombol keluar
tombol_keluar = Tkinter.Button(top,
                            text="Keluar",
                            command=saat_tombol_keluar)
tombol_keluar.grid(column=3, row=2)

top.mainloop()

