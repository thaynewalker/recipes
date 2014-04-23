#!/usr/bin/python

import os
import cgi
import cgitb
cgitb.enable()
import json
import sys

data = {
"measurements": {}, #ex: {cup: {type: vol}}
"categories": [], #ex: [fruit,veggie,seasoning]
"ingredients": {}, #ex: {olive: {category:vegetable}}
"recipes": {} #ex: {pancakes: {ingredients:[{name:flour,desc:sifted,amount:1,measurement:cup},{}],instructions:"whip it"}
}

def loadfromfile():
  global data
  fp = open("recipes.json","r")
  data = json.loads(fp.read())
  fp.close()
  
def synctofile():
  global data
  fp = open("recipes.json","w")
  fp.write(json.dumps(data))
  fp.close()

if __name__ == "__main__":
  print "Content-type: text/json\n"
  form = cgi.FieldStorage()
  cmd = 'get' #put/del
  if 'cmd' in form:
    cmd = form['cmd'].value
  tgt = 'categories'
  if 'tgt' in form:
    tgt = form['tgt'].value
  val = None
  if 'val' in form:
    val = json.loads(form['val'].value)

  if tgt != 'all' and tgt not in data.keys():
    print "Error no target %s\n"%tgt
    sys.exit(0)

  if val is not None and type(val) is not type(data[tgt]):
    print "Error value types do not match, you put %s, but need %s\n"%(type(val),type(data[tgt]))
    sys.exit(0)
    

  loadfromfile()

  if cmd == 'put':
    if type(data[tgt]) is dict:
      for j in val.keys():
        data[tgt][j] = val[j]
    elif type(data[tgt]) is list:
      for j in val:
        if j not in data[tgt]:
          data[tgt].append(j)
    synctofile()

  elif cmd == 'del':
    if type(data[tgt]) is dict:
      for f in val.keys():
        if f in data[tgt].keys():
          del data[tgt][f]
    elif type(data[tgt]) is list:
      for f in val:
        data[tgt].remove(f)
    synctofile()

  if tgt == 'all':
    print json.dumps(data)
  else:
    print json.dumps(data[tgt])

        
