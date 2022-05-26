import GPIO.PCF8591 as ADC

class IR:
  def __init__(self, channel: int) -> None:
    self.ch = channel
    self.reads = [None]*6
  
  def filter(self) -> float:
    count = 0
    sum = 0
    max = 0
    reads = self.reads.copy()[0:6]
    for read in reads:
      if read != None and read > max:
        max = read

    reads.remove(max)

    for read in reads[0:6]:
      if read != None:
        sum += read
        count += 1
    
    print(reads)
    print(sum)
    print(count)
    if count == 0:
      return None
    
    return sum / count

    
  
  def read(self) -> float:
    read = ADC.read(self.ch)
    print(read)
    self.reads.insert(0, read)
    print(self.reads[0:6])
    
    return self.filter()
