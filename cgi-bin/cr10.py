#!/usr/bin/python

# CT10 measurements graph generator

'''debug CGI
print "Content-Type: text/plain"
print
import sys
sys.stderr = sys.stdout
#'''

activate_this = '/home/aircraft/aircraft/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

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

df3 = pd.read_csv('~aircraft/public_html/CR10/data/LSradiation.csv', sep=',', header=0, parse_dates='time')  # load FD data
df3['time'] = pd.to_datetime(df3['time'])
df3 = df3.set_index('time')
df3 = df3.sort_index()

df2 = pd.read_csv('~aircraft/public_html/CR10/data/radiation_avg.csv', sep=',', header=0, parse_dates='time' ) # load Liulin data
df2['date'] = pd.to_datetime(df2['date'])
df2 = df2.set_index('date')
df2['DSi'] = df2['DSi'].astype(float)
df2['DSi_corr'] = df2['DSi_corr'].astype(float) * 3 + 20

df2['lat'] = df2['lat'] / 20 - 10
df2['alt'] = df2['alt'] / 3048 - 20 # feets to meters plus some shift

datetime.timedelta(days=1)
from_time = str(pd.to_datetime(FD) + datetime.timedelta(days=-days_view))
to_time = str(pd.to_datetime(FD) + datetime.timedelta(days=days_view))


df2[from_time: to_time].plot(figsize=(12,8),fontsize=10) 
#df2[from_time: to_time]['lat'].plot(figsize=(12,9),lw='1', label='latitude') 
df3[from_time: to_time]['FD'] = df3[from_time: to_time]['FD'].sub(90) # normalize FD data
df3[from_time: to_time]['FD'].plot(lw='1',  ls=':', label='NM LS')
plt.ylabel('[arbitrary unit]',fontsize=10) # Y axis label
plt.xlabel('UT') # X axis label
plt.title(FD)  # print central time

plt.axvline(x=pd.to_datetime(FD), color='grey', ls='--') # plot dashed vertical line at the FD time

plt.legend(fontsize=10)

plt.tight_layout()  # reduce margins
plt.savefig('/home/aircraft/public_html/CR10/data/ble.png')  # save plot to file

# HTML code
print 'Content-type:text/html\r\n\r\n'
print '<html>'
print '<head>'
print '<title>CR10</title>'
print '<link rel="stylesheet" type="text/css" href="../style/aircraft.css">'
print '<link rel="shortcut icon" type="image/x-icon" href="../style/favicon.ico" />'
print '</head>'
print '<body>'

print "<h1>CR10 database</h1>"
print '<form action="cr10.cgi" method="get">'
print 'Day: <input type="text" name="FD" value=%s>  &nbsp; &nbsp; Window +-: <input type="text" name="days" value=%s /> days &nbsp; &nbsp; ' % (FD, days)
print '<input type="submit" value="Submit" />'
print '</form>'

print '<img src="../data/ble.png">'
print '<p>When using these data, please read this <a href="../license.html">info</a>.</p>'

print '</body>'
print '</html>'

