import string

import Chrono.utils
from Chrono import chronoEntities as chrono


## Takes in a TimePhraseEntity and identifies if it should be annotated as a Frequency entity
# @author Amy Olex
# @param s The TimePhraseEntity to parse
# @param chrono_id The current chrono_id to increment as new chronoEntities are added to list.
# @param chrono_list The list of Chrono objects we currently have.  Will add to these.
# @return chronoList, chronoID Returns the expanded chronoList and the incremented chronoID.

def buildFrequency(s, chrono_id, chrono_list):
    boo, val, startSpan, endSpan = hasFrequency(s)




####
# END_MODULE
####

## Takes in a single text string and identifies if it has any Frequency phrases
# @author Amy Olex
# @param tpentity The TimePhrase entity object being parsed
# @return Outputs 4 values: Boolean Flag, Value text, start index, end index
def hasFrequency(tpentity):
    text_lower = tpentity.getText().lower()

    text_norm = text_lower.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    text_list = text_norm.split(" ")


####
# END_MODULE
####