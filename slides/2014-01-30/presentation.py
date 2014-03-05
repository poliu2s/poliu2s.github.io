import sys
import urllib
import json
import time
import numpy
import cmath
import math
import heapq

def funnel(n, numbers):
  if n == 0: return []
  heap = numbers[:n]
  heapq.heapify(heap)
  for k in numbers[n:]:
    if heap[0] < k:
      heapq.heapreplace(heap, k)
  return heap





# Configure what data to grab from Graphite/Bucky
str_dashboard_data = 'stats.dashboard.message.sent'
str_from = '-7d'
str_to = '-0d'
str_interval = '5min'


# Alter these values based on your configuration
total_days = 21
pts_per_day = 86400


# Formulate request URL and fire off
url = 'http://bucky.hootsuitemedia.com/render?target=aliasByNode(hitcount(' + str_dashboard_data + ',%22' + str_interval  + '%22),1)&from=' + str_from + '&until=' + str_to  + '&format=json'
result = json.load(urllib.urlopen(url))
time_now = time.time()
raw_list = list(result[0]['datapoints'])




# In the event of server outages, filter Bucky/Graphite response and remove null values
filtered_list = []
for i in range( len(raw_list) ):
  if raw_list[i][0] != None:
    filtered_list.append(raw_list[i][0])



deriv1 = []
for i in range(0, len(filtered_list)-1):
  # if ( filtered_list[i] == None or filtered_list[i+1] == None ):
  deriv1.append(filtered_list[i+1] - filtered_list[i])


deriv2 = []
for i in range(0, len(deriv1)-1):
  deriv2.append(deriv1[i+1] - deriv1[i])


# Calculate the FFT freq spectrum
np_raw = numpy.array(raw_list)
fournier_complex = numpy.fft.fft(filtered_list)
fournier_mag = []
for i in range(1, len(fournier_complex)):
  fournier_mag.append( cmath.polar(fournier_complex[i])  )






hz = []
for i in range(1, len(fournier_complex)):
  hz.append( (60.0 * len(fournier_complex)) / i / 86400 )



#For reconstruction
# sig_recon = []
# for i in range(1, len(fournier_complex)):
#   sig_recon.append(fournier_mag[7*1440][0]*(numpy.cos(2*3.1415*i/(7*1440)) + 1j*numpy.sin(2*3.1415*i/(7 * 1440))).real)


top_fourier = funnel(15, fournier_mag)
top_ffiltered = []
for i in range(0, len(fournier_mag)):
  for j in range(0, len(top_fourier)):
    if (top_fourier[j] == fournier_mag[i]) or (i < 1):
      top_ffiltered.append(fournier_complex[j])
      break 

  if len(top_ffiltered) == i:
    top_ffiltered.append(complex(0.0, 0.0))

filtered_ifft = numpy.fft.ifft(top_ffiltered)

interval = 7.0/len(filtered_ifft)
sum = 0
increment = []
for i in range(0, len(filtered_ifft)):
  sum = sum + interval 
  increment.append(sum)




filtered_list.pop()

# Prepare data for R
filtered_data = (', '.join( str(e) for e in filtered_list ) )
deriv1_data = (', '.join( str(e) for e in deriv1 ) )
deriv2_data = (', '.join( str(e) for e in deriv2 ) )
fournier_data = (', '.join( str( e[0] ) for e in fournier_mag  ))
hz_data = (', '.join( str(e) for e in hz ) )
# recon_data = (', '.join( str(e) for e in sig_recon ) )
ifft_data = (', '.join( str(1.1* e.real) for e in filtered_ifft))
int_data = (', '.join( str(e) for e in increment ) )

# For Debugging
# print '=============Raw:======================================================'
# print filtered_data
# print '==========================Deriv1:======================================'
# print deriv1_data
# print '==========================Deriv2:======================================'
# print deriv2_data
# print '==========================Fournier====================================='
# print fournier_data
# print '==========================Hertz========================================'
# print hz_data
# print '==========================Recon========================================'
# print recon_data

#for i in range(0, len(fournier_mag) ):
#  sys.stdout.write( str(fournier_mag[i][0]) )
#  if i != len(fournier_mag)-1:
#    sys.stdout.write(', ')


#for i in range(0, len(fournier_complex)):
#  sys.stdout.write( str(fournier_complex[i]) + ', ' )

print "\n\n"


#Write the R file for plotting/visualization
f = open('graph.R', 'w')
f.write('raw_data <- c(' + filtered_data + ')\n' ) 
f.write('plot(raw_data, type="o", col="blue")\n' )
f.write('dev.new() \n')


f.write('deriv1_data <- c(' + deriv1_data + ')\n' )
f.write('plot(deriv1_data, type="o", col="red")\n' )
f.write('dev.new() \n')

f.write('deriv2_data <- c(' + deriv2_data + ')\n' )
f.write('plot(deriv2_data, type="o", col="green")\n' )
f.write('dev.new() \n')

f.write('fournier_mag <- c(' + fournier_data + ')\n' )
f.write('hz_data <- c(' + hz_data + ')\n' )
f.write('plot(hz_data, fournier_mag, type="o", col="purple") ')
f.write('dev.new() \n')

# f.write('recon_data <- c(' + recon_data + ')\n' )
# f.write('plot(recon_data, type="o", col="yellow") ')
# f.write('dev.new() \n')

f.write('filtered_ifft <- c(' + ifft_data + ')\n' )
f.write('int_data <- c(' + int_data + ')\n' )
f.write('plot(int_data, filtered_ifft, type="o", col="green")\n')
f.write('lines(int_data, raw_data, type="o", col="blue") \n')


f.close()

