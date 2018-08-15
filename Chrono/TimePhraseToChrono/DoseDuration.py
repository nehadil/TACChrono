import re
import string
import numpy as np
from Chrono import chronoEntities as chrono, utils
from Chrono.TimePhraseToChrono.Modifier import hasModifier
from Chrono.utils import calculateSpan
from chronoML import ChronoKeras
from Chrono import temporalTest as tt


## Parses a TimePhrase entity's text field to determine if it contains a calendar interval or period phrase, then builds the associated chronoentity list
# @author Amy Olex
# @param s The TimePhrase entity to parse
# @param chronoID The current chronoID to increment as new chronoentities are added to list.
# @param chronoList The list of chrono objects we currently have.  Will add to these.
# @return chronoList, chronoID Returns the expanded chronoList and the incremented chronoID.
###### ISSUES: This method assumes the number is immediatly before the interval type. There is some concern about if the spans are going to be correct.  I do test for numbers written out as words, but this assumes the entire beginning of the string from TimePhrase represents the number.  If this is not the case the spans may be off.
###### More Issues: I created the training data incorrectly to remove the TimePhrase entity from consideration.  In order to classify from scratch we would need multiple classes: period, interval, everything else.  I only have a binary classifier here, so I need to narrow it down before trying to classify.
def buildDoseDuration(s, chrono_id, chrono_list, ref_list, classifier, feats):
    features = feats.copy()
    ref_Sspan, ref_Espan = s.getSpan()
    #print("In buildPeriodInterval(), TimePhrase Text: " + s.getText())
    bad = re.compile(r"^q\d|^Q\d")
    parts = s.getText().split()
    containsnum = False
    #various checks to ensure that this phrase is actually a dose duration
    if isDoseDuration(parts[0]):
        return chrono_list, chrono_id
    if "every" in s.getText().lower() or "time" in s.getText().lower() or "per" in s.getText().lower():
        return chrono_list, chrono_id
    if bad.match(s.getText()):
        return chrono_list, chrono_id
    if "/" in s.getText():
        return chrono_list, chrono_id
    if "[**" in s.getText() or "**]" in s.getText():
        return chrono_list, chrono_id
    if "ly" in s.getText():
        return chrono_list, chrono_id
    if "(" in s.getText() or ")" in s.getText():
        return chrono_list, chrono_id
    if "once" in s.getText().lower() or "twice" in s.getText().lower():
        return chrono_list, chrono_id
    if "past" in s.getText().lower() or "ago" in s.getText().lower():
        return chrono_list, chrono_id
    if "RANDOM" in s.getText():
        return chrono_list,chrono_id
    for part in parts:
        for ref in ref_list:
            if ref.getText().lower() == part.lower():
                if(ref.isNumeric()):
                    containsnum = True
                    break
                elif not tt.hasDoseDuration(ref.getText().lower()):
                    return chrono_list, chrono_id
    if containsnum ==False:
        return chrono_list, chrono_id

    boo, val, idxstart, idxend, plural = hasDoseDuration(s)
    if boo:
        abs_Sspan = ref_Sspan + idxstart
        abs_Espan = ref_Sspan + idxend

        # get index of overlapping reference token
        # ref_idx = -1
        # for i in range(0,len(ref_list)):
        #    if(utils.overlap(ref_list[i].getSpan(),(abs_Sspan,abs_Espan))):
        #        ref_idx = i
        #        break

        ref_idx = utils.getRefIdx(ref_list, abs_Sspan, abs_Espan)

        # extract ML features
        my_features = utils.extract_prediction_features(ref_list, ref_idx, feats.copy())

        # classify into period or interval
        if classifier[1] == "NN":
            my_class = ChronoKeras.keras_classify(classifier[0], np.array(list(my_features.values())))
            # print("Class: " + str(my_class) + " : Start: " + str(abs_Sspan) + " : End: "+ str(abs_Espan))
        elif classifier[1] in ("SVM", "RF"):
            feat_array = [int(i) for i in my_features.values()]
            my_class = classifier[0].predict([feat_array])[0]
        else:
            my_class = classifier[0].classify(my_features)
            # print("Class: " + str(my_class) + " : Start: " + str(abs_Sspan) + " : End: "+ str(abs_Espan))

        # if 1 then it is a period, if 0 then it is an interval
        if my_class == 1:
            my_entity = chrono.ChronoDoseDurationEntity(entityID=str(chrono_id) + "entity", start_span=abs_Sspan,
                                                        end_span=abs_Espan, dose_type=getDoseDurationValue(val),
                                                        number=None, text=s.getText())
            chrono_id = chrono_id + 1
            ### Check to see if this calendar interval has a "this" in front of it
            prior_tok = ref_list[ref_idx - 1].getText().lower()
            if prior_tok.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) == "this":
                # add a This entitiy and link it to the interval.
                start_span, end_span = re.search(prior_tok, "this").span(0)
                prior_start, prior_end = ref_list[ref_idx - 1].getSpan()

                chrono_this_entity = chrono.ChronoThisOperator(entityID=str(chrono_id) + "entity",
                                                               start_span=prior_start + start_span,
                                                               end_span=prior_start + end_span)
                chrono_id = chrono_id + 1
                chrono_this_entity.set_period(my_entity.get_id())
                chrono_list.append(chrono_this_entity)

            else:
                # check for a Last Word
                hasMod, mod_type, mod_start, mod_end = hasModifier(s)

                if (hasMod):
                    if mod_type == "Next":
                        chrono_list.append(chrono.ChronoNextOperator(entityID=str(chrono_id) + "entity",
                                                                     start_span=ref_Sspan + mod_start,
                                                                     end_span=ref_Sspan + mod_end,
                                                                     period=my_entity.get_id()))
                        chrono_id = chrono_id + 1

                    if mod_type == "Last":
                        chrono_list.append(chrono.ChronoLastOperator(entityID=str(chrono_id) + "entity",
                                                                     start_span=ref_Sspan + mod_start,
                                                                     end_span=ref_Sspan + mod_end,
                                                                     period=my_entity.get_id(),
                                                                     semantics="Interval-Not-Included"))
                        chrono_id = chrono_id + 1



        else:
            my_entity = chrono.ChronoDoseDurationEntity(entityID=str(chrono_id) + "entity", start_span=abs_Sspan,
                                                        end_span=abs_Espan, dose_type=val, number=None, text=s.getText())
            chrono_id = chrono_id + 1
            ### Check to see if this calendar interval has a "this" in front of it
            prior_tok = ref_list[ref_idx - 1].getText().lower()
            if prior_tok.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) == "this":
                # add a This entitiy and link it to the interval.
                start_span, end_span = re.search(prior_tok, "this").span(0)
                prior_start, prior_end = ref_list[ref_idx - 1].getSpan()

                chrono_this_entity = chrono.ChronoThisOperator(entityID=str(chrono_id) + "entity",
                                                               start_span=prior_start + start_span,
                                                               end_span=prior_start + end_span)
                chrono_id = chrono_id + 1
                chrono_this_entity.set_repeating_interval(my_entity.get_id())
                chrono_list.append(chrono_this_entity)
            else:
                # check for a Last Word
                hasMod, mod_type, mod_start, mod_end = hasModifier(s)
                if (hasMod):
                    if mod_type == "Next":
                        chrono_list.append(chrono.ChronoNextOperator(entityID=str(chrono_id) + "entity",
                                                                     start_span=ref_Sspan + mod_start,
                                                                     end_span=ref_Sspan + mod_end,
                                                                     repeating_interval=my_entity.get_id()))
                        chrono_id = chrono_id + 1

                    if mod_type == "Last":
                        chrono_list.append(chrono.ChronoLastOperator(entityID=str(chrono_id) + "entity",
                                                                     start_span=ref_Sspan + mod_start,
                                                                     end_span=ref_Sspan + mod_end,
                                                                     repeating_interval=my_entity.get_id(),
                                                                     semantics="Interval-Not-Included"))
                        chrono_id = chrono_id + 1

        # check to see if it has a number associated with it.  We assume the number comes before the interval string
        if idxstart > 0:
            substr = s.getText()[0:idxstart]
            m = re.search('([0-9]{1,2})', substr)
            if m is not None:
                num_val = m.group(0)
                abs_Sspan = ref_Sspan + m.span(0)[0]
                abs_Espan = ref_Sspan + m.span(0)[1]

                my_number_entity = chrono.ChronoNumber(entityID=str(chrono_id) + "entity", start_span=abs_Sspan,
                                                       end_span=abs_Espan, value=num_val)
                chrono_id = chrono_id + 1

                # add the number entity to the list
                chrono_list.append(my_number_entity)
                my_entity.set_number(my_number_entity.get_id())
            # else search for a text number
            else:
                texNumVal = utils.getNumberFromText(substr)
                if texNumVal is not None:
                    # create the number entity
                    my_number_entity = chrono.ChronoNumber(entityID=str(chrono_id) + "entity", start_span=ref_Sspan,
                                                           end_span=ref_Sspan + (idxstart - 1), value=texNumVal)
                    chrono_id = chrono_id + 1
                    # append to list
                    chrono_list.append(my_number_entity)
                    # link to interval entity
                    my_entity.set_number(my_number_entity.get_id())

        chrono_list.append(my_entity)
    else:
        boo2, val, idxstart, idxend, numstr = hasEmbeddedPeriodInterval(s)
        if(boo2):
            abs_Sspan = ref_Sspan + idxstart
            abs_Espan = ref_Sspan + idxend

            # get index of overlapping reference token
            ref_idx = -1
            for i in range(0,len(ref_list)):
                if(utils.overlap(ref_list[i].getSpan(),(abs_Sspan,abs_Espan))):
                    ref_idx = i
                    break

            # extract ML features
            my_features = utils.extract_prediction_features(ref_list, ref_idx, features)

            # classify into period or interval
            if(classifier[1] == "NN"):
                my_class = ChronoKeras.keras_classify(classifier[0], np.array(list(my_features.values())))
                #print("Class: " + str(my_class) + " : Start: " + str(abs_Sspan) + " : End: "+ str(abs_Espan))
            else:
                my_class = classifier[0].classify(my_features)
                #print("Class: " + str(my_class) + " : Start: " + str(abs_Sspan) + " : End: "+ str(abs_Espan))

             # if 1 then it is a period, if 0 then it is an interval
            if(my_class == 1):
                my_entity = chrono.ChronoDoseDurationEntity(entityID=str(chrono_id) + "entity", start_span=abs_Sspan, end_span=abs_Espan, dose_type=getDoseDurationValue(val), number=None, text=s.getText())
                chrono_id = chrono_id + 1
            else:
                my_entity = chrono.ChronoDoseDurationEntity(entityID=str(chrono_id) + "entity", start_span=abs_Sspan, end_span=abs_Espan, dose_type=val, number=None, text=s.getText())
                chrono_id = chrono_id + 1

            #Extract the number and identify the span of numstr

            substr = s.getText()[:idxstart] ## extract entire first part of TimePhrase phrase
            m = re.search('([0-9]{1,2})', substr) #search for an integer in the subphrase and extract it's coordinates
            if m is not None :
                num_val = m.group(0)
                abs_Sspan = ref_Sspan + m.span(0)[0]
                abs_Espan = ref_Sspan + m.span(0)[1]

                my_number_entity = chrono.ChronoNumber(entityID=str(chrono_id) + "entity", start_span=abs_Sspan, end_span=abs_Espan, value=num_val)
                chrono_id = chrono_id + 1

                #add the number entity to the list
                chrono_list.append(my_number_entity)
                #link to interval entity
                my_entity.set_number(my_number_entity.get_id())
            #else search for a text number
            else:
                texNumVal = utils.getNumberFromText(numstr)
                if texNumVal is not None:
                    m = re.search(numstr, substr) #search for the number string in the subphrase
                    if m is not None :
                        abs_Sspan = ref_Sspan + m.span(0)[0]
                        abs_Espan = ref_Sspan + m.span(0)[1]
                        #create the number entity
                        my_number_entity = chrono.ChronoNumber(entityID=str(chrono_id) + "entity", start_span=abs_Sspan, end_span=abs_Espan, value=texNumVal)
                        chrono_id = chrono_id + 1
                        #append to list
                        chrono_list.append(my_number_entity)
                        #link to interval entity
                        my_entity.set_number(my_number_entity.get_id())

            chrono_list.append(my_entity)

    return chrono_list, chrono_id

    # FIND terms that are always marked as calendar intervals!



## Takes in a TimePhrase entity and identifies if it has any period or calendar interval phrases like "week" or "days"
# @author Amy Olex
# @param tpentity The TimePhrase entity object being parsed
# @return Outputs 5 values: Boolean Flag, Value text, start index, end index, pluralBoolean
def hasDoseDuration(tpentity):
    # convert to all lower
    # text_lower = tpentity.getText().lower()
    text = tpentity.getText().lower()
    #print("In hasPeriodInterval text: ", text)

    reg = re.search("after$", text)  ##we don't want to annotate these specific types of mentions
    if reg:
        #print("Found date/time, returning FALSE")
        return False, None, None, None, None
    # remove all punctuation
    text_norm = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
    # convert to list
    text_list = text_norm.split(" ")
    #print("text list: " + str(text_list))

    # define my period lists
    terms = ["day", "week","hour",
             "days", "weeks", "months", "hours", "hrs"]  #, "date"]

    # figure out if any of the tokens in the text_list are also in the interval list
    intersect = list(set(text_list) & set(terms))

    #print("My intersection: " + str(intersect))

    # only proceed if the intersect list has a length of 1 or more.
    # For this method I'm assuming it will only be a length of 1, if it is not then we don't know what to do with it.
    if len(intersect) == 1:
        # test if the intersect list contains plural or singular period.

        this_term = list(set(intersect) & set(terms))[0]
        start_idx, end_idx = calculateSpan(text_norm, this_term)
        if this_term in ["day", "daily", "days"]:
            return True, "Day", start_idx, end_idx, False
        elif this_term in ["week", "weekly", "weeks"]:
            return True, "Week", start_idx, end_idx, False
        elif this_term in ["month", "monthly", "months"]:
            return True, "Month", start_idx, end_idx, False
        elif this_term in ["hour", "hourly", "hours", "hrs"]:

            return True, "Hour", start_idx, end_idx, False
        else:
            return False, None, None, None, None

    elif len(intersect) > 1:
        print("interesting:", intersect)
        this_term = list(
            set(intersect) & set(["daily", "weekly", "monthly", "yearly", "weeks", "days", "months", "years"]))

        if (this_term):
            if (len(this_term) == 1):
                this_term = this_term[0]
                start_idx, end_idx = calculateSpan(text_norm, this_term)

                if this_term in ["daily", "days"]:
                    #print("Returning a Daily")
                    return True, "Day", start_idx, end_idx, False
                elif this_term in ["weekly", "weeks"]:
                    return True, "Week", start_idx, end_idx, False
                elif this_term in ["monthly", "months"]:
                    return True, "Month", start_idx, end_idx, False
                elif this_term in ["yearly", "years"]:
                    return True, "Year", start_idx, end_idx, False
                else:
                    return False, None, None, None, None
            else:
                return False, None, None, None, None
        else:
            return False, None, None, None, None

    else:
        return False, None, None, None, None

## Takes in a TimePhrase entity and identifies if it has any calendar interval phrases like "week" or "days"
# @author Amy Olex
# @param tpentity The TimePhrase entity object being parsed
# @return Outputs 5 values: Boolean Flag, Value text, start index, end index, numeric string
# Note: this should be called after everything else is checked.  The numeric string will need to have it's span and value identified by the calling method.
def hasEmbeddedPeriodInterval(tpentity):
    # convert to all lower
    # text_lower = tpentity.getText().lower()
    text = tpentity.getText()
    # remove all punctuation
    text_norm = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    # convert to list
    text_list = text_norm.split(" ")

    # define my period/interval term lists
    terms = ["day", "week",
             "month",  "hour",
             "days", "weeks", "months", "hours", "hrs"] #, "date"]

    ## if the term does not exist by itself it may be a substring. Go through each word in the TimePhrase string and see if a substring matches.
    for t in text_list:
        for r in terms:
            ## see if r is a substring of t
            ## if yes and the substring is at the end, extract the first substring and test to see if it is a number.
            idx = t.find(r)
            if (idx > 0):
                # then the r term is not the first substring.  Extract and test.
                sub1 = t[:idx]
                sub2 = t[idx:]
                # sub1 should be a number
                if (isinstance(utils.getNumberFromText(sub1), (int))):
                    # if it is a number then test to figure out what sub2 is.
                    this_term = sub2
                    start_idx, end_idx = calculateSpan(text_norm, this_term)
                    if this_term in ["day", "daily", "days"]:
                        #print("ACK! Found an Embedded Day")
                        return True, "Day", start_idx, end_idx, sub1
                    elif this_term in ["week", "weekly", "weeks"]:
                        return True, "Week", start_idx, end_idx, sub1
                    elif this_term in ["month", "monthly", "months"]:
                        return True, "Month", start_idx, end_idx, sub1
                    elif this_term in ["hour", "hourly", "hours"]:
                        return True, "Hour", start_idx, end_idx, sub1

                else:
                    return False, None, None, None, None
    return False, None, None, None, None

def isDoseDuration(text):
    text = text.lower()
    text_norm = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
    terms = ["day", "week",
             "month", "hour",
             "days", "weeks", "months",  "hours",  "hrs"]

    if text_norm in terms:
        return True
    else:
        return False
    # convert to list


## Takes in a string that is a Calendar-Interval value and returns the associated Period value
# @author Amy Olex
# @param val The Calendar-Interval string
# @return The Period value string
def getDoseDurationValue(val):
    if val == "Day":
        return("Days")
    elif val == "Week":
        return("Weeks")
    elif val == "Month":
        return("Months")
    elif val == "Hour":
        return("Hours")
    else:
        return(val)