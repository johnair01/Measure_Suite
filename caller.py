import visa
import csv
from pyvisa.ctwrapper.functions import gpib_control_ren
rm = visa.ResourceManager()
lib = rm.visalib

print(rm.list_resources())
ps = rm.open_resource("GPIB0::26::INSTR")
#v=keithley.ask("G0")
#fv = float(v[v.find("=")+1:v.find("E")])*10**float(v[v.find("E")+1:v.find("E")+4])


ps.write("smua.source.func=smua.OUTPUT_DCVOLTS")
ps.write("smua.source.leveli=0")
ps.write("smua.measure.nplc = 25")
ps.write("smua.source.output=smua.OUTPUT_ON")
ps.write(" currenta= smua.measure.i()")
ps.write("smub.source.output=smub.OUTPUT_OFF")
current = ps.ask("print(currenta)")
#voltage = ps.ask("print(voltageb)")
ps.write("smua.source.output=smua.OUTPUT_OFF")
#print (current)
#print (voltage)


with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'Current']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'Current': current})
    writer.writerow({'first_name': 'Lovely', 'Current': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'Current': 'Spam'})