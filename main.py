'''
Created on 21 November 2017

@author: John Air
'''

import time
import sys
from PyQt4 import QtGui, QtCore
from measure_Suite import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
from Device_Comm import Keithley_230
from Device_Comm import Keithley_2636B
from pyqtgraph.ptime import START_TIME
from asyncio.tasks import sleep
import winsound


class Main(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnStart.clicked.connect(self.btnStart_Clicked)
        self.ui.Resume_Scan.clicked.connect(self.Resume_Scan_Clicked)
    #end init
    
    
    
    ########################################################################
	## This class is to measure all the relevant data (in either the dark or light)
	## all at once i.e. the output characteristics, the transfer characterisctics
	## for the linear and saturated regions for positive and negative and positive gate
	## voltages
	########################################################################
    
    
    def btnStart_Clicked(self):
        self.dp_out_plot = self.ui.Dark_Out_Pos_View
        self.dn_out_plot = self.ui.Dark_Out_Neg_View
        self.dp_probe_plot = self.ui.Dark_Probe_Pos_View
        self.dn_probe_plot = self.ui.Dark_Probe_Neg_View
        self.dp_trans_plot = self.ui.Dark_Trans_Pos_View
        self.dn_trans_plot = self.ui.Dark_Trans_Neg_View
       
        # create a plot for the time domain data
        #data_plot = self.win.addPlot(title="Ids vs Vgs")
        
        #Pos OutPut
        po_vg0 = 0
        po_vd0 = 0
        po_vdstep = .25
        po_vdf = 20
        po_vgf = 30
        po_vgstep = 10
        #Neg OutPut
        no_vg0 = 0
        no_vd0 = 0
        no_vdstep = .25
        no_vdf = -20
        no_vgf = -30
        no_vgstep = 10
        #Pos Trans
        pt_vg0 = -5
        pt_vgf = 30
        pt_vstep = 0.25           
        pt_vds_1 = 0.2
        pt_vds_2 = 0.5
        pt_vds_3 = 2.0	
        pt_vds_4 = 20
        #Neg Trans
        nt_vg0 = 5
        nt_vgf = -30
        nt_vstep = 0.25           
        nt_vds_1 = -0.2
        nt_vds_2 = -0.5
        nt_vds_3 = -2.0	
        nt_vds_4 = -20
        
        ##Initialize Plots
        #Dark_Positive OutPut Plot
        
        self.dp_out_plot.setXRange(po_vd0 , po_vdf)
        self.dp_out_plot.showGrid(True, True)
        self.dp_out_plot.addLegend()
        Process_Data_Out(po_vg0,po_vgf,po_vgstep,po_vd0,po_vdf,po_vdstep,self.dp_out_plot)
        
        #Dark_Negative OutPut Plot
        self.dn_out_plot.setXRange(no_vd0 , no_vdf)
        self.dn_out_plot.showGrid(True, True)
        self.dn_out_plot.addLegend()
        Process_Data_Out(no_vg0,no_vgf,no_vgstep,no_vd0,no_vdf,no_vdstep,self.dn_out_plot)
        
        #Dark_Positive Transfer and Probe Plot
        self.dp_trans_plot.setXRange(pt_vg0 , pt_vgf)
        self.dp_trans_plot.showGrid(True, True)
        self.dp_trans_plot.addLegend()
        self.dp_trans_plot = self.dp_trans_plot.plot(pen=(24, 215, 248))
       
        self.dp_probe_plot.setXRange(pt_vg0 , pt_vgf)
        self.dp_probe_plot.showGrid(True, True)
        self.dp_probe_plot.addLegend()
        self.dp_probe_plot = self.dp_probe_plot.plot(pen=(24, 215, 248))
        
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_1,self.dp_trans_plot, self.dp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_2,self.dp_trans_plot, self.dp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_3,self.dp_trans_plot, self.dp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_4,self.dp_trans_plot, self.dp_probe_plot)
        
        
        #Dark_Negative Transfer and Probe Plot
        self.dn_trans_plot.setXRange(nt_vg0 , nt_vgf)
        self.dn_trans_plot.showGrid(True, True)
        self.dn_trans_plot.addLegend()
       
        self.dn_probe_plot.setXRange(nt_vg0 , nt_vgf)
        self.dn_probe_plot.showGrid(True, True)
        self.dn_probe_plot.addLegend()
        
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_1,self.dn_trans_plot, self.dn_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_2,self.dn_trans_plot, self.dn_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_3,self.dn_trans_plot, self.dn_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_4,self.dn_trans_plot, self.dn_probe_plot)
        
        
        duration = 1000  # millisecond
        freq = 440  # Hz
        
        winsound.MessageBeep()
        time.sleep(5)
        winsound.Beep(freq, duration)
        
        
    def Resume_Scan_Clicked(self):
        self.lp_out_plot = self.ui.Light_Out_Pos_View
        self.ln_out_plot = self.ui.Light_Out_Neg_View
        self.lp_probe_plot = self.ui.Light_Probe_Pos_View
        self.ln_probe_plot = self.ui.Light_Probe_Neg_View
        self.lp_trans_plot = self.ui.Light_Trans_Pos_View
        self.ln_trans_plot = self.ui.Light_Trans_Neg_View
       
        # create a plot for the time domain data
        #data_plot = self.win.addPlot(title="Ids vs Vgs")
        
        #Pos OutPut
        po_vg0 = 0
        po_vd0 = 0
        po_vdstep = .25
        po_vdf = 20
        po_vgf = 30
        po_vgstep = 10
        #Neg OutPut
        no_vg0 = 0
        no_vd0 = 0
        no_vdstep = .25
        no_vdf = -20
        no_vgf = -30
        no_vgstep = 10
        #Pos Trans
        pt_vg0 = -5
        pt_vgf = 30
        pt_vstep = 0.25           
        pt_vds_1 = 0.2
        pt_vds_2 = 0.5
        pt_vds_3 = 2.0	
        pt_vds_4 = 20
        #Neg Trans
        nt_vg0 = 5
        nt_vgf = -30
        nt_vstep = 0.25           
        nt_vds_1 = -0.2
        nt_vds_2 = -0.5
        nt_vds_3 = -2.0	
        nt_vds_4 = -20
        
        ##Initialize Plots
        #Light_Positive OutPut Plot
        self.lp_out_plot.setXRange(po_vd0 , po_vdf)
        self.lp_out_plot.showGrid(True, True)
        self.lp_out_plot.addLegend()
        Process_Data_Out(po_vg0,po_vgf,po_vgstep,po_vd0,po_vdf,po_vdstep,self.lp_out_plot)
        
        #Dark_Negative OutPut Plot
        self.ln_out_plot.setXRange(no_vd0 , no_vdf)
        self.ln_out_plot.showGrid(True, True)
        self.ln_out_plot.addLegend()
        Process_Data_Out(no_vg0,no_vgf,no_vgstep,no_vd0,no_vdf,no_vdstep,self.ln_out_plot)
        
        #Dark_Positive Transfer and Probe Plot
        self.lp_trans_plot.setXRange(pt_vg0 , pt_vgf)
        self.lp_trans_plot.showGrid(True, True)
        self.lp_trans_plot.addLegend()
       
        self.lp_probe_plot.setXRange(pt_vg0 , pt_vgf)
        self.lp_probe_plot.showGrid(True, True)
        self.lp_probe_plot.addLegend()
        
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_1,self.lp_trans_plot, self.lp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_2,self.lp_trans_plot, self.lp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_3,self.lp_trans_plot, self.lp_probe_plot)
        Process_Data_Trans(pt_vg0,pt_vgf,pt_vstep,pt_vds_4,self.lp_trans_plot, self.lp_probe_plot)
        
        
        #Dark_Negative Transfer and Probe Plot
        self.ln_trans_plot.setXRange(nt_vg0 , nt_vgf)
        self.ln_trans_plot.showGrid(True, True)
        self.ln_trans_plot.addLegend()
        self.ln_trans_plot= self.ln_trans_plot.plot(pen=(24, 215, 248))
       
        self.ln_probe_plot.setXRange(nt_vg0 , nt_vgf)
        self.ln_probe_plot.showGrid(True, True)
        self.ln_probe_plot.addLegend()
        self.ln_probe_plot = self.ln_probe_plot.plot(pen=(24, 215, 248))
        
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_1,self.ln_trans_plot, self.ln_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_2,self.ln_trans_plot, self.ln_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_3,self.ln_trans_plot, self.ln_probe_plot)
        Process_Data_Trans(nt_vg0,nt_vgf,nt_vstep,nt_vds_4,self.ln_trans_plot, self.ln_probe_plot)   
        
     
        
class Rolling_Queue(object):
    def __init__(self):
        self.size = 4
        self.elements = []
    #end init
    
    
    def add(self, item):
        if self.is_full():
            self.elements.pop(0)
        self.elements.append(item)   
    # end def
    
    def get_std(self):
        if self.is_full():
            return np.std(self.elements)/np.mean(self.elements)
        return 5000
    # end def
    
    def is_full(self):
        return len(self.elements)>= self.size
    #end def
              
#end class

def Process_Data_Trans(vg0,vgf,vstep,vds,i_plt, vp_plt): #This is for taking Ids vs Vgs
     # Define Keithley instrument ports:
    k2636B = Keithley_2636B('GPIB0::26::INSTR')  # Voltage Source_1
    k230 = Keithley_230('GPIB0::2::INSTR') # Voltage Source_2
               
    I_Array = []
    Vgs_Array = []
    Vp_Array = []
    
    #Set  Drain voltage (SMUB)
    #Sweep gate voltage (k230) and measure Drain current (SMUB) and probe voltage (SMUB)
    #	 
    
    round_vds = round(vds,3)
    k2636B.standby_on("a")
    k2636B.standby_on("b")
    k2636B.set_current ("a", 0)
    k2636B.source_range("b","v",20)
    k2636B.set_voltage("b",vds)#Set  Drain voltage (SMUB)
   
    if vgf-vg0 > 0:
        vp_curve = vp_plt.plot( name="Transfer Characteristics " + str(vds) )
        i_curve = i_plt.plot( name="Transfer Characteristics " + str(vds) )
        while True:    
            round_vg0= round(vg0,3)
            k230.set_voltage(round_vg0) #Set  Gate voltage (k230)
            k230.operate()
            Vgs_Array.append(round_vg0)
            #time.sleep(.5)
            #current settling
            #i_temp = Rolling_Queue()
            #while i_temp.get_std() > 0.1:
            #    i_temp.add(k2636B.read_current("b"))
            I_new = k2636B.read_current("b")
            PV_new = k2636B.read_voltage("a")
            I_Array.append(I_new)
            Vp_Array.append(PV_new)
            #update graph
            i_curve.setData(Vgs_Array,I_Array)
            vp_curve.setData(Vgs_Array,Vp_Array)
            QtGui.QApplication.processEvents()
            vg0 = vg0+vstep
        
            if round_vg0 >= vgf: 
                k230.stand_by()
                k2636B.standby_off("a")
                k2636B.standby_off("b")
                break
        
        print (Vgs_Array)
        print (I_Array)
        print (Vp_Array)
    
        return [Vgs_Array,I_Array,Vp_Array]
    
    if vgf-vg0 < 0:
        vp_curve = vp_plt.plot( name="Transfer Characteristics " + str(vds) )
        i_curve = i_plt.plot( name="Transfer Characteristics " + str(vds) )
        while True:
            round_vg0= round(vg0,3)
            k230.set_voltage(round_vg0) #Set  Gate voltage (k230)
            k230.operate()
            Vgs_Array.append(round_vg0)
            time.sleep(.5)
            #current settling
            #i_temp = Rolling_Queue()
            #while i_temp.get_std() > 0.1:
            #    i_temp.add(k2636B.read_current("a"))
            I_new = k2636B.read_current("b")
            PV_new = k2636B.read_voltage("a")
            I_Array.append(I_new)
            Vp_Array.append(PV_new)
            #update graph
            i_curve.setData(Vgs_Array,I_Array)
            vp_curve.setData(Vgs_Array,Vp_Array)
            QtGui.QApplication.processEvents()
            vg0 = vg0-vstep
        
            if round_vg0 <= vgf: 
                k230.stand_by()
                k2636B.standby_off("a")
                k2636B.standby_off("b")
                break
        
        print (Vgs_Array)
        print (I_Array)
        print (Vp_Array)
    
        return [Vgs_Array,I_Array,Vp_Array]
# end def


def Process_Data_Out(vg0,vgf,vgstep,vd0,vdf,vdstep,v_plot): #This is for taking Ids vs Vgs
  # Define Keithley instrument ports:
    k2636B = Keithley_2636B('GPIB0::26::INSTR')  # Voltage Source_1
    k230 = Keithley_230('GPIB0::2::INSTR') # Voltage Source_2
    
    
    new_vd0 = vd0           
    I_Array = []
    Vds_Array = []
    
    
    if vdf > new_vd0:
        while True:
            v_curve = v_plot.plot( name="Transfer Characteristics " + str(vg0) )
            round_vg0 = round(vg0,3)
            k230.set_voltage(round_vg0) #Set  Gate voltage (k230)
            k230.operate()

            ramping_up = True
            while True:
                round_vd0= round(vd0,3)
                k2636B.standby_on("b")
                k2636B.source_range("b","v",20)
                k2636B.set_voltage("b",vd0)
             
                Vds_Array.append(round_vd0)
                #time.sleep(.5)
                #current settling
                #i_temp = Rolling_Queue()
                #while i_temp.get_std() > 1:
                #    i_temp.add(k2636B.read_current("b"))
                I_new = k2636B.read_current("b")
                I_Array.append(I_new)
                #update graph
                v_curve.setData(Vds_Array,I_Array)
                QtGui.QApplication.processEvents()
                if ramping_up:
                    vd0 = vd0+vdstep
                    if round_vd0 >= vdf: 
                        ramping_up = False
                else:
                    vd0 = vd0-vdstep
                    if round_vd0 <= new_vd0:
                        k2636B.standby_off("b")
                        break

            Vds_Array = []
            I_Array = []
            vd0 = new_vd0
            vg0 = vg0 +vgstep
            if round_vg0 >= vgf:
                k230.stand_by()
                break
    
        return [Vds_Array,I_Array]
    
    if vdf < new_vd0:
        while True:
            v_curve = v_plot.plot( name="Transfer Characteristics " + str(vg0) )
            round_vg0 = round(vg0,3)
            k230.set_voltage(round_vg0) #Set  Gate voltage (k230)
            k230.operate()

            ramping_down = True
            while True:
                round_vd0= round(vd0,3)
                k2636B.standby_on("b")
                k2636B.source_range("b","v",20)
                k2636B.set_voltage("b",vd0)
            	
                Vds_Array.append(round_vd0)
                #time.sleep(.5)
                #current settling
                #i_temp = Rolling_Queue()
                #while i_temp.get_std() > 1:
                #    i_temp.add(k2636B.read_current("b"))
                I_new = k2636B.read_current("b")
                I_Array.append(I_new)
                #update graph
                v_curve.setData(Vds_Array,I_Array)
                QtGui.QApplication.processEvents()
                if ramping_down:
                    vd0 = vd0-vdstep
                    if round_vd0 <= vdf: 
                        ramping_down = False
                else:
                    vd0 = vd0+vdstep
                    if round_vd0 >= new_vd0:
                        k2636B.standby_off("b")
                        break
                
            Vds_Array = []
            I_Array = []
            vd0 = new_vd0
            vg0 = vg0 -vgstep
            if round_vg0 <= vgf:
                k230.stand_by()
                break
        return [Vds_Array,I_Array]




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    example = Main()
    example.show()
    sys.exit(app.exec_())
