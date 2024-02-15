import machine
class IR_RX():
  REPEAT=-1
  BADSTART=-2
  BADBLOCK=-3
  BADREP=-4
  OVERRUN=-5
  BADDATA=-6
  BADADDR=-7
  def __init__(self,pin,callback,*args):
    self._pin=pin
    self.callback=callback
    self.args=args
    self._errf=lambda _ : None
    self._times=[]
    self.cb=self.decode
    print([self._pin,self.callback,self.args,self._errf,self._times,self.cb])
  def _cb_pin(self):
    print("IR Remote control: waiting command ... \n")
    self._pin.set_pull(self._pin.NO_PULL)
    d0=-1
    while d0<0:d0=machine.time_pulse_us(self._pin,1,10000)
    self._times=[d0]
    for i in range(1,100):
      di=machine.time_pulse_us(self._pin,1,100000)
      if di>0:self._times.append(di)
      else:break
    print('durations: '+str(self._times))
  def do_callback(self,cmd,addr,ext,thresh=0):
    if cmd >= thresh:self.callback(cmd,addr,ext,*self.args)
    else:self._errf(cmd)
  def error_function(self,func):self._errf=func