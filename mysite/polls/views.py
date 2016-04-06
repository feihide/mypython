from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import datetime
import time
import json
import logging

def index(request):
    cx = sqlite3.connect("/python/db/test.db")
    cu=cx.cursor()
    cu.execute("select * from fetch order by ctime desc" )
    r = cu.fetchall()
    out ='<table border=1>'
    for row in r:
        ltime=time.localtime(row[3])
        timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)

        out =out+'<tr><td>'+str(row[0])+'</td><td><a href="'+row[2]+'" target="_blank">'+row[1]+'</a></td><td>'+row[2]+'</td><td>'+ str(timeStr)+'</td></tr>'
    out =out+ '</table>'
    cx.close()
    return HttpResponse(out)

def apiGet(request):
    cx = sqlite3.connect("/python/db/test.db")
    offset = request.GET.get('offset','0');
    limit = request.GET.get('limit','10');
    cu=cx.cursor()
    cu.execute("select * from fetch order by ctime desc limit "+offset+","+limit)
    r = cu.fetchall()
    if 'callback' in request.GET:
        out = request.GET['callback']+"("+json.dumps(r)+")"
    else:
        out = r;
    cx.close()
    return HttpResponse(out)

def apiDel(request):
    #logger = logging.getLogger('mylogger')
    var = request.GET['id']
    if var:
        cx = sqlite3.connect("/python/db/test.db")
        cu=cx.cursor()

        cu.execute("delete  from fetch where id = "+var )
        r = cx.commit()
        cx.close()
    else:
        r = 'error'
    if 'callback'  in request.GET:
        out = request.GET['callback']+"("+json.dumps(r)+")"
    else:
        out = r;
    return HttpResponse(out)

def apiFavor(request):
    #logger = logging.getLogger('mylogger')
    var = request.GET['id']
    if var:
        cx = sqlite3.connect("/python/db/test.db")
        cu=cx.cursor()

        cu.execute("update fetch set favor =favor+1 where id = "+var )
        r = cx.commit()
        cx.close()
    else:
        r = 'error'
    if 'callback'  in request.GET:
        out = request.GET['callback']+"("+json.dumps(r)+")"
    else:
        out = r;
    return HttpResponse(out)

def apiOne(request):
    #logger = logging.getLogger('mylogger')
    var = request.GET['id']
    if var:
        cx = sqlite3.connect("/python/db/test.db")
        cu=cx.cursor()

        cu.execute("select * from fetch where id = "+var )
        r = cu.fetchone()
        cx.close()
    else:
        r = 'error'
    if 'callback' in request.GET:
        out = request.GET['callback']+"("+json.dumps(r)+")"
    else:
        out = r;
    return HttpResponse(out)
