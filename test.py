from datetime import datetime
  
# datetime in string format for may 25 1999
input = '2021/05/25'
  
dt = datetime.now().strftime("%Y%m%d-%H%M%S")
print(dt)
  
