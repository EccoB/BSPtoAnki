import json
import csv
import genanki
import requests
import os
from urllib.parse import urlparse
from html.parser import HTMLParser
h = HTMLParser()


import random


#------------- Parsing Input --------------------
import argparse

parser = argparse.ArgumentParser(description='Take a JSON Input File with questions from bootsfuehrerschein-portal.de '
                                             'and convert it to an Anki-deck')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
parser.add_argument('outfile', nargs='?')


args = parser.parse_args()
print("----")
file = args.infile
outfile = args.outfile


#### Static ####
#filename="jsonFragen.txt"
#file =open(filename,"r")

#-----------------------------------------------




raw=file.read()
questions=json.loads(raw)
#print(questions)
#exit(0)
#for question in questions:
#    print(question)




##---------------------------- Anki specific -------------
my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{Answer}}',
    },
  ])


my_deck = genanki.Deck(
  2059400110,
  'BSPFull')

my_note = genanki.Note(
  model=my_model,
  fields=['Frage', 'Antwort', 'imageFrage','imageAntwort'])

my_note2 = genanki.Note(
  model=my_model,
  fields=['Frage', 'Antwort<img src="BSP_Q_157.png">', '<img src="BSP_Q_157.png">','<img src="BSP_Q_157.png">']) # Funktioniert so



#Creating a Package Example:
#my_deck.add_note(my_note)
#my_deck.add_note(my_note2)
#my_package = genanki.Package(my_deck)
#mediafiles=['media/BSP_Q_157.png']
#my_package.media_files=mediafiles

#my_package.write_to_file('output.apkg')
#exit(0)

##----------------------

mediafiles=[]
downloadFiles=False # If we already downloaded all Images, we can skip to download


with open("csvexampleFull.csv",'w',newline='') as csvfile:
    csvw=csv.writer(csvfile,delimiter=";")
    for question in questions:
        #--------- Download media files -----------------------
        #Example: https://bootsfuehrerschein-portal.de/fragendatenbank_images/FK2012_BASIS_A_038.png
        imf=""  # ImageName for Question
        ima=""  # ImageName for Answer
        if question["image_frage"] !='':
            url =question["image_frage"]
            a = urlparse(url)
            imf=os.path.basename(a.path)
            mediafiles.append('media/' + imf)

            if downloadFiles:
                imaget = requests.get(url)
                open('media/'+imf, 'wb').write(imaget.content)


        if question["image_antwort"] !='':
            url =question["image_antwort"]
            a = urlparse(url)
            ima=os.path.basename(a.path)
            mediafiles.append('media/' + ima)
            if downloadFiles:
                imaget = requests.get(url)
                open('media/'+ima, 'wb').write(imaget.content)



        #------------------
        print(question)
        vorderseite=""
        vorderseite += "<h2>"+question["id"]+" -- "+question["kapitel"] +"</h2>\n"
        if imf !="":
            vorderseite += '<img style="display: block; margin-left: auto;margin-right: auto;max-width: 75%;"  src="'+imf+'">'
        vorderseite +='<p>'+ question["question"]+'</p>\n'


        q1=h.unescape(question["answer_1"])
        q2=h.unescape(question["answer_2"])
        q3=h.unescape(question["answer_3"])
        q4 = h.unescape(question["answer_4"])

        quests=[q1,q2,q3,q4]
        random.shuffle(quests)



        #vorderseite = vorderseite + "[ ]  " +quests[0].replace("**","")+'\n'
        #vorderseite = vorderseite + "[ ]  "+ quests[1].replace("**","") + '\n'
        #vorderseite = vorderseite + "[ ]  "+ quests[2].replace("**","") + '\n'

        rueckseite="<h2>"+question["id"]+" -- "+question["kapitel"]+'</h2>\n';
        rueckseite +="<p><ul>"
        vorderseite +="<p><ul>"
        for i in range(4):
            if len(quests[i])>0:
                if(quests[i].find("**")>=0):
                    rueckseite += "<li>[x]  "
                else:
                    rueckseite += "<li>[ ]  "
                rueckseite += quests[i].replace("**","")+'</li>\n'
                vorderseite += "<li>[ ]  " +quests[i].replace("**","")+'</li>\n'
        vorderseite +="</ul></p>"
        rueckseite +="</ul></p>"

        rueckseite += "\n</p>" + question["beschreibung"]+"/<p>"
        if ima !="":
            rueckseite += '<img style="display: block; margin-left: auto;margin-right: auto;max-width: 75%;"  src="'+ima+'">'

        print(vorderseite)
        print(rueckseite)

        #------ Creating the Anki node ----------
        my_note = genanki.Note(
            model=my_model,
            fields=[vorderseite, rueckseite])
        my_deck.add_note(my_note)


        #csvw.writerow([vorderseite,rueckseite])
    #---- Create thw whole AnkiDeck
    my_package = genanki.Package(my_deck)
    my_package.media_files=mediafiles
    #my_package.write_to_file('BSPFullImages.apkg')
    my_package.write_to_file(outfile)

exit(0)
