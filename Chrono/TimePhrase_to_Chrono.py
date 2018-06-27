import string

from Chrono import chronoEntities


def buildChronoList(dosePhrases):
    chroList = []
    tracker = 1
    for phrase in dosePhrases:
        words = phrase.getText().split(" ")
        start, end = phrase.getSpan()
        ongoing = ""
        for n in range(0,len(words)):
            temp = words[n].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).strip()
            if temp.replace(".","1",1).isdigit():
                span = (start, start + len(words[n]))
                something = chronoEntities.ChronoEntity(tracker, "Dose", span, words[n])
                chroList.append(something)
                start = start + len(words[n])+1
                tracker = tracker + 1
            else:
                ongoing +=words[n]
                if(n!=len(words)-1):
                    ongoing += " "

        somethingelse = chronoEntities.ChronoEntity(tracker, "DoseUnits", (start,start + len(ongoing)), ongoing)
        tracker = tracker + 1
        chroList.append(somethingelse)
    return chroList





