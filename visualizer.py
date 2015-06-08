#!/usr/bin/python
from message import *
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import numpy as np

DEBUG = False

messages = []

splitHeader       = "<div class=\"message\"><div class=\"message_header\">"
splitSpan         = "</span>"
replaceUser       = "<span class=\"user\">"
replaceMeta       = "<span class=\"meta\">"
replaceText       = "</div></div><p>"
replaceParagraph  = "</p>"

years = {}


def main():

  if(len(sys.argv) > 2):
    messageName = sys.argv[1]
    fbName = sys.argv[2].split(',')
    print fbName
  else:
    print "Please provide the file with the messages from your Facebook account as an argument. \nIf you have downloaded your profile archive it should be located in the folder \"html\" called \"messages.htm\"."
    print "The second argument should be your user name on Facebook."
    sys.exit()

  if messageName is not None:
    with open(messageName, 'r') as mFile:
      messageString = mFile.read()

    # split for message_header
    messageArray = messageString.split(splitHeader)[1:]
    print "Amount of found messages: " + str(len(messageArray))
    print "----------"
    print

    # iterate through all messages
    for tmpMessage in messageArray:
      tmpMessageSplit = tmpMessage.split(splitSpan)
      # split for user name
      userName = tmpMessageSplit[0].replace(replaceUser, '')
      if DEBUG:
        print userName
      # split for meta information
      metaData = (tmpMessageSplit[1].replace(replaceMeta, '')).split(' UTC')
      metaData = datetime.datetime.strptime(metaData[0], "%A, %B %d, %Y at %I:%M%p" ) + datetime.timedelta(hours=int(metaData[1]))
      if DEBUG:
        print metaData
      # split for text
      textData = tmpMessageSplit[2].replace(replaceText, '').replace(replaceParagraph, '')
      if DEBUG:
        print textData

      messages.append(Message(userName, metaData, textData))
      if DEBUG:
        break

    # iterate over all messages and increase the year counter
    amountLetters_in = 0
    amountLetters_out = 0
    for tmp in messages:
      tmpYear = str(tmp.date.year) + "_" + str(tmp.date.month)
      # create key
      if str(tmpYear) + "_in" not in years.keys():
        years[str(tmpYear) + "_in"] = 0
        years[str(tmpYear) + "_out"] = 0
      if tmp.name in fbName:
        direction = "_out"
        amountLetters_out = amountLetters_out + len(tmp.text)
      else:
        direction = "_in"
        amountLetters_in = amountLetters_in + len(tmp.text)
      years[str(tmpYear) + direction] = years[str(tmpYear) + direction] + 1
      
    # print results
    keylist = years.keys()
    keylist.sort()
    for key in keylist:
      print "%s: %s" % (key, years[key])
    print amountLetters_in
    print amountLetters_out
    print "Parsed " + str(len(messages)) + " messages" 

  values_in = []
  values_out = []
  dates_in = []
  dates_out = []

  keylist = years.keys()
  keylist.sort()
  for key in keylist:
    if "_in" in key:
      tmpKey = key.replace("_in", '')
      values_in.append(years[key])
      dates_in.append(datetime.datetime.strptime(tmpKey, '%Y_%m').date())
    else:
      tmpKey = key.replace("_out", '')
      values_out.append(years[key])
      dates_out.append(datetime.datetime.strptime(tmpKey, '%Y_%m').date())

  if DEBUG:
    print dates_in
    print values_in
    print dates_out
    print values_out

  plt.figure(figsize=(20,10))
  ax = plt.subplot(111)
  w = 15
  x = date2num(dates_out)

  ax.bar(x-w, values_in,width=w,color='b',align='center', label='incoming messages')
  ax.bar(x, values_out,width=w,color='g',align='center', label='outgoing messages')
  ax.xaxis_date()
  ax.autoscale(tight=True)
  ax.grid(True)

  locs, labels = plt.xticks()
  plt.setp(labels, rotation=90)
  plt.xlabel('Month')
  plt.ylabel('Messages')
  plt.title('Facebook messages (' + str(len(messages)) + ' in total)')
  plt.legend(loc=2)
  plt.show()

main()