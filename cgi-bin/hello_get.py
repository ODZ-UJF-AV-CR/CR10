#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

#import matplotlib
#matplotlib.use('Agg')
#import pylab

import matplotlib.pyplot as plt
matplotlib.use('Agg')
import pylab
import pandas as pd  # data parsing library

#pylab.plot([1,2], [3,4], linestyle='-')
#pylab.savefig('ble.png')

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
xfrom = form.getvalue('from')
xto  = form.getvalue('to')


FD = '2005-8-1'

days_view = 20

df3 = pd.read_csv('../data/LSradiation.csv', sep=',', header=0, parse_dates='time')
df3['time'] = pd.to_datetime(df3['time'])
df3 = df3.set_index('time')
df3 = df3.sort_index()

df2 = pd.read_csv('../data/radiation_avg.csv', sep=',', header=0, parse_dates='time' )
df2['date'] = pd.to_datetime(df2['date'])
df2 = df2.set_index('date')
df2['H'] = df2['H'].astype(float)
df2['HH'] = df2['HH'].astype(float) * 5 + 40

df2['lat'] = df2['lat'] / 20
df2['alt'] = (df2['alt'] - 30000) / 4000

        
datetime.timedelta(days=1)
from_time = str(pd.to_datetime(FD) + datetime.timedelta(days=-days_view))
to_time = str(pd.to_datetime(FD) + datetime.timedelta(days=days_view))

df2[from_time: to_time].plot(figsize=(100,10),lw='2')
df3[from_time: to_time]['FD'] = df3[from_time: to_time]['FD'].sub(90)
df3[from_time: to_time]['FD'].plot(figsize=(100, 10))
plt.title('FD ' + FD)  

#plt.savefig('ble.png')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Graph</title>"
print "</head>"
print "<body>"
print "<h2>from %s to %s</h2>" % (xfrom, xto)

print '<form action="/cgi-bin/hello_get.py" method="get">'
print 'From: <input type="text" name="from"><br />'
print 'To: <input type="text" name="to" />'
print '<input type="submit" value="Submit" />'
print '</form>'

print '<p>Graph: <br>'
print '<img src="../ble.png">'

print "</body>"
print "</html>"



