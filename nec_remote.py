from ir_receiver import IR_RX
class NEC_ABC(IR_RX):
  def __init__(self,pin,extended,callback,*args):
    super().__init__(pin,callback,*args)
    print([pin,extended,callback])
    self._extended=extended
    self._addr=0
  def decode(self):
    self._cb_pin()
    try:
      decoded=[]
      if len(self._times)<35 or len(self._times)>40:raise RuntimeError(self.OVERRUN)
      elif self._times[0]<4000 or self._times[1]<3000:raise RuntimeError(self.BADSTART)
      for i in range(len(self._times)):
        if self.is_around(self._times[i],39000,offset=500):decoded.append('repeat')
        elif self.is_around(self._times[i],1687):decoded.append(1)
        elif self.is_around(self._times[i],562):decoded.append(0)
        elif self._times[i]>3000:decoded.append(self._times[i])
        else:decoded.append(None)
      print('decoded: '+str(decoded))
      if 'repeat' not in decoded:raise RuntimeError(self.BADREP)
      else:
        frameData=decoded[2:34]
        data=self.binToHex(frameData)
        if None in frameData:raise RuntimeError(self.BADDATA)
        dataBin=(frameData[:8],frameData[8:16],frameData[16:24],frameData[24:32])
        dataInt=(self.binToHex(dataBin[0]),self.binToHex(dataBin[1]),self.binToHex(dataBin[2]),self.binToHex(dataBin[3]))
        print(dataInt)
        addr=dataInt[1]
        if addr is not ((dataInt[0]>>8)^0xff)&0xff:raise RuntimeError(self.BADADDR)          
        cmd=dataInt[2]
        if cmd+dataInt[3] is not 0xff:raise RuntimeError(self.BADDATA)   
    except RuntimeError as e:
      print('Error:'+str(e))
      cmd=e.args[0]
      addr=self._addr if cmd==self.REPEAT else 0
      data=0
    self.do_callback(data,addr,cmd,self.REPEAT)
  def binToHex(self,binary):
    binary_string=""
    for e in binary:binary_string+=str(e)
    return int(binary_string,2)
  def is_around(self,value,ref,offset=200):
    ecart_type=value-ref
    if abs(ecart_type)<offset:return True
    else:return False
class NEC_8(NEC_ABC):
  def __init__(self,pin,callback,*args):super().__init__(pin,False,callback,*args)
class NEC_16(NEC_ABC):
  def __init__(self,pin,callback,*args):super().__init__(pin,True,callback,*args)