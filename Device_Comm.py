import visa
from pylint.checkers.spelling import instr
#ResourceManager for visa instrument control
rm = visa.ResourceManager()

#############################################################
class Keithley_2636B:#Voltage Source
    #--------------------------------------------------------------------------
    def __init__(self, instr):
        self.ctrl = rm.open_resource(instr)
        self.ctrl.write("smua.measure.nplc = 1")
        self.ctrl.write("smub.measure.nplc = 1")
    #end init

#######################################################################################
########################           MEASURE SETTINGS        ############################
#######################################################################################    
   
    #Enable or disable autorange and for current or voltage
    def measure_autorange (self, smu, i_or_v, on_or_off):
    	self.ctrl.write("smu{}.measure.autorange{} = smu{}.AUTORANGE_{}".format(smu, i_or_v, smu, on_or_off))
    
    #end autorange
    
        	
    #Set current or voltage measurement Range	
    def measure_range (self, smu,i_or_v, val):
    	self.ctrl.write("smu{}.measure.range{} = {}".format(smu, i_or_v, val))
   
    #end measure_range
    	
    	
    def read_current(self, smu):
        self.ctrl.write("smu{}.source.output=smu{}.OUTPUT_ON".format(smu, smu))
        self.ctrl.write("current = smu{}.measure.i()".format(smu))
        string_A = self.ctrl.ask("print(current)")
        return float(string_A) #Convert to float

    #end def
    
    def read_voltage(self, smu):
        self.ctrl.write("smu{}.source.output=smu{}.OUTPUT_ON".format(smu, smu))
        self.ctrl.write("voltage = smu{}.measure.v()".format(smu))
        string_A = self.ctrl.ask("print(voltage)")
        return float(string_A)	#Convert to float

	#end def



#######################################################################################
########################           SOURCE SETTINGS        ############################
####################################################################################### 
	
	#Enable or disable autorange and for current or voltage
    def source_autorange (self, smu, i_or_v, on_or_off):
        self.ctrl.write("smu{}.source.autorange{} = smu{}.AUTORANGE_{}".format(smu, i_or_v, smu, on_or_off))
	
	#end autorange
	
			
	#Set current or voltage measurement Range	
    def source_range (self, smu,i_or_v, val):
        self.ctrl.write("smu{}.source.range{} = {}".format(smu, i_or_v, val))
   
	#end measure_range
		
		
    def set_current(self, smu, current):
        self.ctrl.write("smu{}.source.func=smu{}.OUTPUT_DCAMPS".format(smu, smu))
        self.ctrl.write("smu{}.source.leveli= {}".format(smu, current))

	#end def
	
    def set_voltage(self, smu, volt):
        self.ctrl.write("smu{}.source.func=smu{}.OUTPUT_DCVOLTS".format(smu, smu))
        self.ctrl.write("smu{}.source.levelv= {}".format(smu, volt))

	#end def
	
    def standby_on(self, smu):
        self.ctrl.write("smu{}.source.output=smu{}.OUTPUT_ON".format(smu, smu))
        
    def standby_off(self, smu):
        self.ctrl.write("smu{}.source.output=smu{}.OUTPUT_OFF".format(smu, smu))
        
        
class Keithley_230:#Voltage Source
    #--------------------------------------------------------------------------
    def __init__(self, instr):
        self.ctrl = rm.open_resource(instr)

    #end init
    

    #--------------------------------------------------------------------------
    def ilimit_set(self, ilimit_230):
        self.ctrl.write("I%nX" %ilimit_230) # Set current limit for Keithley 230
       
    #end def

    #--------------------------------------------------------------------------
    def set_voltage(self, vsource_230):
        self.ctrl.write("V{}X".format(vsource_230))# Set the Voltage Source parameters
    #end def
    #--------------------------------------------------------------------------
    def set_dwellTime(self, dwell_time):
        self.ctrl.write("W{}}X" .format(dwell_time))# Set the Voltage Source parameters
    #end def
    #--------------------------------------------------------------------------
    def operate(self):
        self.ctrl.write("F1X")
    #end def
    
    def stand_by(self):
        self.ctrl.write("F0X")
    #end def
  
###############################################################################
