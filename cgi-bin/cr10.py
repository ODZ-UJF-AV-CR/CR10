#!/usr/bin/python

# CT10 measurements WEB access

'''debug CGI
print "Content-Type: text/plain"
print
import sys
sys.stderr = sys.stdout
#'''

#!!!activate_this = '/home/aircraft/aircraft/bin/activate_this.py'  # activate virtualenv
#!!!execfile(activate_this, dict(__file__=activate_this))

# Import modules for CGI handling 
import cgi, cgitb 

import matplotlib               
matplotlib.use('Agg')           # virtual frame buffer
import matplotlib.pyplot as plt # plotting library
import pandas as pd             # data parsing library
import datetime as datetime     # time conversion and calculation
import linecache # direct read from file

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
    
# Get data from fields
FD = form.getvalue('FD')
days = form.getvalue('days')
action = form.getvalue('action')

#FD = '2005-8-1' # it is a default FD


try:
    days_view = int(days)

    datetime.timedelta(days=1)
    from_time = str(pd.to_datetime(FD) + datetime.timedelta(days=-days_view))
    to_time = str(pd.to_datetime(FD) + datetime.timedelta(days=days_view))

    df3 = pd.read_csv('~aircraft/public_html/data/LSradiation.csv', sep=',', header=0, parse_dates='time')  # load FD data
    df3['time'] = pd.to_datetime(df3['time'])
    df3 = df3.set_index('time')
    df3 = df3.sort_index()

    df2 = pd.read_csv('~aircraft/public_html/data/radiation_avg.csv', sep=',', header=0, parse_dates='time' ) # load Liulin data
    df2['date'] = pd.to_datetime(df2['date'])
    df2 = df2.set_index('date')
    df2['c'] = df2['count'] / (3.1/100) # Normalize to %
    df2 = df2.loc[df2['c']<110]

    #df2['lat'] = df2['lat'] / 20 - 10
    #df2['alt'] = df2['alt'] / 3048 - 20 # feets to meters plus some shift


    #df2[from_time: to_time].plot(figsize=(12,8),fontsize=10) 
    df2[from_time: to_time]['c'].plot(figsize=(12,7),lw='1', marker='o', markersize=4, label='Aircraft',zorder=2) 
    #df3.loc[from_time: to_time,'FD'] = df3[from_time: to_time]['FD'].sub(90) # normalize FD data
    df3[from_time: to_time]['FD'].plot(lw='1',  color='gray', label='Ground', zorder=1)
    plt.ylabel('[%]',fontsize=10) # Y axis label
    plt.xlabel('UT') # X axis label
    plt.title(FD)  # print central time

    plt.axvline(x=pd.to_datetime(FD), color='gray', ls='--') # plot dashed vertical line at the FD time

    plt.legend(fontsize=10)

    plt.tight_layout()  # reduce margins
    plt.savefig('/home/aircraft/public_html/data/ble.png')  # save plot to file

    if action == 'Download':
        filename = '/home/aircraft/public_html/data/AllRunSort.txt'

        df = pd.read_csv(filename,delimiter=',', header=0, usecols=['date']) 
        df = df.set_index('date')

        days_view = int(days)

        datetime.timedelta(days=1)
        from_time = str(pd.to_datetime(FD) + datetime.timedelta(days=-days_view))
        to_time = str(pd.to_datetime(FD) + datetime.timedelta(days=days_view))


        # copy selected data to file 
        starting_line_number = df[:from_time].shape[0]+2
        number_of_lines      = df[from_time:to_time].shape[0]
        # print starting_line_number, number_of_lines
        copy = open('/home/aircraft/public_html/data/cr10_selection.csv', 'w')
        preamble = open('/home/aircraft/public_html/data/preamble.txt', 'r')
        for line in preamble:
            copy.write(line)

        for line_num in range(starting_line_number, starting_line_number+number_of_lines):
            copy.write(linecache.getline(filename,line_num))
        copy.close()
except:
    import shutil
    shutil.copy2('/home/aircraft/public_html/style/nodata.png','/home/aircraft/public_html/data/ble.png')
    pass


# --------------------- HTML code --------------------------
print 'Content-type:text/html\r\n\r\n'
print '<html>'
print '<head>'
print '<title>CR10</title>'
print '<link rel="stylesheet" type="text/css" href="../style/aircraft.css">'
print '<link rel="shortcut icon" type="image/x-icon" href="../style/favicon.ico" />'

if action == 'Download':
    print '<meta http-equiv="refresh" content="0; url=http://cr10.odz.ujf.cas.cz/data/cr10_selection.csv?forcedownload=1"/>'

print '</head>'
print '<body>'

print "<h1>CR10 database</h1>"
print '<form action="cr10.cgi" method="get">'
print 'Day: <input type="text" name="FD" value=%s>  &nbsp; &nbsp; Window +-: <input type="text" name="days" value=%s /> days &nbsp; &nbsp; ' % (FD, days)
print '<input type="submit" name="action" value="Submit" />'
print '<br>'
print '<br>'

print '<img src="../data/ble.png?%s">' % str(datetime.datetime.now())  # hack for refresh the picture
print '<p>When using these data, please read this <a href="../license.html">info</a>.</p>'

print '<input type="submit" name="action" value="Download" />'
print '</form>'

print '</body>'
print '</html>'

