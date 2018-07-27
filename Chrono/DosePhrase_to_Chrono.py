# coding=utf-8
import re
import string

from Chrono import chronoEntities


def buildChronoList(dosePhrases):
    chroList = []
    tracker = 1

    for phrase in dosePhrases:
        if " " in phrase.getText():
            words = phrase.getText().split(" ")
            ongoing = ""
            pos = 0
            multistart = -1
            start = phrase.getSpan()[0]
            n=0
            while n<len(words):
                if words[n]=="and" or words[n]=="or":
                    start = start + len(words[n])+1
                    n=n+1
                original = words[n]
                length = len(original)
                if("(" not in words[n] or ")" not in words[n]):
                    words[n] = re.sub(r'[!"\#$&()*+,\-:;\'<=>?@\[\\\]_`{|}~]', "", words[n])
                else:
                    words[n] = re.sub(r'[!"\#$&*+,\-:;\'<=>?@\[\\\]_.`{|}~]', "", words[n])
                try:

                    pattern = re.compile(r'^[0-9\.–]+')
                    number = pattern.match(words[n]).group(0)
                    temp = number
                    if(len(number) != 1):
                        temp = re.sub(r'^0+',"", temp)
                    temp = re.sub(r'[–]', "", temp)
                    if original[0] != words[n][0]:
                        start = start +1
                        length = length-1

                    if temp.replace(".","1",1).isdigit():
                        span = (start, start + len(number))
                        something = chronoEntities.ChronoDoseEntity("T"+str(tracker), "Dose", span, number)
                        chroList.append(something)
                        tracker = tracker + 1
                        if len(number)!=len(words[n]):
                            text = words[n][len(number):]
                            ongoing+=text
                            if (n != len(words) - 1):
                                ongoing += " "
                                if (multistart == -1):
                                    multistart = start+len(number)
                        else:
                            start = start + length + 1

                except:
                    ongoing +=words[n]

                    if(n!=len(words)-1):
                        ongoing += " "
                        if(multistart==-1):
                            multistart = start
                n=n+1
                pos = pos + 1
            if(multistart==-1):
                multistart = start
            ongoing = re.sub(r'\.$', "", ongoing)
            somethingelse = chronoEntities.ChronoDoseEntity("T"+str(tracker), "DoseUnits", (multistart,multistart + len(ongoing)), ongoing)
            tracker = tracker + 1
            chroList.append(somethingelse)

        else:
            i = 0
            text = phrase.getText()
            text.replace(".", "1", 1)
            text = re.sub(r'[!"\#$&()*+,\-.:;\'<=>?@\[\\\]^_`{|}~]', '', text)
            start = phrase.getSpan()[0]
            end = phrase.getSpan()[1]
            if(phrase.getText()[0] != text[0]):
                start = phrase.getSpan()[0]+1 #phrase.getSpan()[0]
                end = start +len(text) #phrase.getSpan()[1]
            try:
                while(i<len(text)):
                    int(text[i])
                    i=i+1

            except:
                dose = text[:i]
                unit = text[i:]
                something = chronoEntities.ChronoDoseEntity("T"+str(tracker), "Dose", (start, start+len(dose)), dose)
                tracker = tracker +1
                somethingelse = chronoEntities.ChronoDoseEntity("T"+str(tracker), "DoseUnits", (end-len(unit), end), unit)
                tracker = tracker + 1
                chroList.append(something)
                chroList.append(somethingelse)

    return chroList





