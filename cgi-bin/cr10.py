#!/usr/bin/python

# CT10 measurements graph generator

'''debug CGI
print "Content-Type: text/plain"
print
import sys
sys.stderr = sys.stdout
#'''

# Import modules for CGI handling 
import cgi, cgitb 

import matplotlib               
matplotlib.use('Agg')           # virtual frame buffer
import matplotlib.pyplot as plt # plotting library
#import pylab
import pandas as pd             # data parsing library
import datetime as datetime     # time conversion and calculation

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
FD = form.getvalue('FD')
days = form.getvalue('days')

#FD = '2005-8-1' # it is a default FD

days_view = int(days)

df3 = pd.read_csv('./data/LSradiation.csv', sep=',', header=0, parse_dates='time')  # load FD data
df3['time'] = pd.to_datetime(df3['time'])
df3 = df3.set_index('time')
df3 = df3.sort_index()

df2 = pd.read_csv('./data/radiation_avg.csv', sep=',', header=0, parse_dates='time' ) # load Liulin data
df2['date'] = pd.to_datetime(df2['date'])
df2 = df2.set_index('date')
df2['H'] = df2['H'].astype(float)
df2['HH'] = df2['HH'].astype(float) * 3 + 20

df2['lat'] = df2['lat'] / 20 - 10
df2['alt'] = df2['alt'] / 3048 - 20

datetime.timedelta(days=1)
from_time = str(pd.to_datetime(FD) + datetime.timedelta(days=-days_view))
to_time = str(pd.to_datetime(FD) + datetime.timedelta(days=days_view))

df2[from_time: to_time].plot(figsize=(12,7),lw='1') 
df3[from_time: to_time]['FD'] = df3[from_time: to_time]['FD'].sub(90) # normalize FD data
df3[from_time: to_time]['FD'].plot(figsize=(12,7),lw='1', label='FD LS') 
plt.title('FD ' + FD)  

plt.axvline(x=pd.to_datetime(FD), color='grey', ls='--') # plot dashed vertical line in tne FD time


plt.savefig('./ble.png')

# HTML code
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Graph</title>"
print "</head>"
print "<body>"
#print "<h2>from %s to %s</h2>" % (FD, days)
print '<form action="/cgi-bin/cr10.py" method="get">'
print 'FD: <input type="text" name="FD" value=%s>  &nbsp; &nbsp; Days+-: <input type="text" name="days" value=%s />' % (FD, days)
print '<input type="submit" value="Submit" />'
print '</form>'

print '<img src="../ble.png">'

print "</body>"
print "</html>"

