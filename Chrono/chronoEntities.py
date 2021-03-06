# Copyright (c) 2018
# Amy L. Olex, Virginia Commonwealth University
# alolex at vcu.edu
#
# Luke Maffey, Virginia Commonwealth University
# maffeyl at vcu.edu
#
# Nicholas Morton,  Virginia Commonwealth University
# nmorton at vcu.edu
#
# Bridget T. McInnes, Virginia Commonwealth University
# btmcinnes at vcu.edu
#
# This file is part of Chrono
#
# Chrono is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Chrono is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chrono; if not, write to
#
# The Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.


## Class definitions for all TimeNorm entities - Intervals, Periods,
# Repeating-Intervals, and Operators.
# ---------------------------------------------------------------------------------------------------------
# Date: 9/19/17
#
# Programmer Name: Luke Maffey
#

## Superclass for all entities
#
# Entities are either an Interval, Period, Repeating-Interval, or Operator
# @param entityID Assigned ID number
# @param start_span The location of the first character
# @param end_span The location of the last character
# @param type The type of the entity
# @param parent_type The parent type of the entity
class ChronoEntity:

    ## The constructor
    def __init__(self, entityID, start_span, end_span, type, parent_type):
        self.entityID = entityID
        self.start_span = start_span
        self.end_span = end_span
        self.type = type
        self.parent_type = parent_type

    ## Tells python how to convert a ChronoEntity to a string
    def __str__(self):
        return self.entityID + " " + self.type

    ## Compares two ChronoEntities (ex. entity1 == entity2)
    # @return Return True if they have the same span and type, false otherwise
    def __eq__(self, other):
        return self.start_span == other.start_span and self.end_span == other.end_span and self.type == other.type

    ## Hashes an entity based on the span and type
    # @return Return true if hashes are the same
    def __hash__(self):
        return hash(self.start_span) ^ hash(self.end_span) ^ hash(self.type)

    ## Sets the entity's id
    # @param entityID The ID to set it to
    def set_id(self, entityID):
        self.entityID = entityID

    ## Returns the entity's id
    # @return The entity's id
    def get_id(self):
        return self.entityID

    ## Sets the entity's start span
    # @param start_span Where in the text the entity starts
    def set_start_span(self, start_span):
        self.start_span = start_span

    ## Returns the entity's start span
    # @return Returns where the entity starts in the text
    def get_start_span(self):
        return self.start_span

    ## Sets the entity's end span
    # @param start_span Where in the text the entity ends
    def set_end_span(self, end_span):
        self.end_span = end_span

    ## Returns the entity's end span
    # @return Returns where the entity ends in the text
    def get_end_span(self):
        return self.end_span

    ## Sets the entity's type
    # @param type The type of entity
    def set_type(self, type):
        self.type = type

    ## Returns the entity's type
    # @return The entity's type as a string
    def get_type(self):
        return self.type

    ## Sets the entity's parent type
    # @param parent_type The parent type
    def set_parent_type(self, parent_type):
        self.parent_type = parent_type

    ## Returns the entity's parent type
    # @return The parent type as a string
    def get_parent_type(self):
        return self.parent_type

    #
    #
    # Subclasses need to close the properties and entities tags
    def print_xml(self):
        return ("\t<entity>\n\t\t<id>{}</id>\n\t\t<span>{},{}</span>\n\t\t"
                "<type>{}</type>\n\t\t<parentsType>{}</parentsType>"
                "\n\t\t<properties>\n\t\t".format(self.entityID, self.start_span,
                                                  self.end_span, self.type, self.parent_type))

# A dose/strength entity
# @author Neha Dil
# @param
class ChronoDoseEntity(ChronoEntity):
    def __init__(self, id, label, span, text):
        super().__init__(id, span[0], span[1], "DosePhrase", None)
        self.id = id
        self.label = label
        self.text = text
        self.span = span

    def getText(self):
        return self.text



    def print_xml(self):
        #return "\t<Mention id=\"{}\" label=\"{}\" span=\"{} {}\" str=\"{}\"/>".format(self.id, self.label,self.span[0], self.span[1],self.text )
        return "{}\t{} {} {}\t{}".format(self.id, self.label, self.span[0], self.span[1], self.text)
class ChronoFrequencyEntity(ChronoEntity):
    def __init__(self, id, label, span, text):
        super().__init__(id, span[0], span[1], "Frequency", None)
        self.id = id
        self.label = label
        self.text = text
        self.span = span

    def getText(self):
        return self.text



    def print_xml(self):
        return (super().print_xml()) + "\t<Type>{}</Type>\n\t\t\t<Text>{}</Text>\n\t\t</properties>\n\t</entity>\n".format("Frequency", self.text)
    def print_ann(self):
        return ("T{}\tFrequency {} {}\t{}".format(self.id, self.span[0], self.span[1], self.text))
class ChronoDoseDurationEntity(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, dose_type, number, text,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Dose", "Duration")
        self.dose_type = dose_type
        self.number = number
        self.modifier = modifier
        self.text = text

    def set_dose_type(self, dose_type):
        self.dose_type = dose_type

    def get_dose_type(self):
        return self.dose_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    ## Prints the xml leaving empty variables blank
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Text>{}</Text>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.dose_type, self.text, self.number or '', self.modifier or ''))
    def print_ann(self):
        return ("T{}\tDuration {} {}\t{}".format( self.entityID, self.start_span, self.end_span, self.text))
## Super class for Intervals which are defined as years
class ChronoIntervalEntity(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, type):
        super().__init__(entityID, start_span, end_span, type, "Interval")


## A year interval
# @param value Which year, e.g. 1998
# @param sub_interval The associated sub-interval, defaults to None
# @param modifier Any modifiers, sometimes "approx", defaults to None
class ChronoYearEntity(ChronoIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, sub_interval=None,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Year")
        self.value = value
        self.sub_interval = sub_interval
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.value, self.sub_interval or '', self.modifier or ''))


## A period of the type of time given
# @param period_type Required {Weeks, Days,...}
# @param number Required
class ChronoPeriodEntity(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, period_type, number,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Period", "Duration")
        self.period_type = period_type
        self.number = number
        self.modifier = modifier

    def set_period_type(self, period_type):
        self.period_type = period_type

    def get_period_type(self):
        return self.period_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.period_type, self.number or '', self.modifier or ''))


## Super class for all Repeating-intervals
class ChronoRepeatingIntervalEntity(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, repeatingType):
        super().__init__(entityID, start_span, end_span, repeatingType,
                         "Repeating-Interval")


## @param month_type Required {January, Februray,...}
class chronoMonthOfYearEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, month_type, sub_interval=None,
                 number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Month-Of-Year")
        self.month_type = month_type
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_month_type(self, month_type):
        self.month_type = month_type

    def get_month_type(self):
        return self.month_type

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.month_type,
                                                                                self.sub_interval or '',
                                                                                self.number or '', self.modifier or ''))


## @param season_type Required {Summer, Winter, Fall, Spring}
class ChronoSeasonOfYearEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, season_type,
                 number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Season-Of-Year")
        self.season_type = season_type
        self.number = number
        self.modifier = modifier

    def set_season_type(self, season_type):
        self.season_type = season_type

    def get_season_type(self):
        return self.season_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.season_type,
                                                                                self.number or '', self.modifier or ''))


## Based on the paper, I assume this takes a value to denote which week of the year
# @param value Required {1-52}
class ChronoWeekOfYearEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, sub_interval=None,
                 number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Week-Of-Year")
        self.value = value
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    #
    # No examples, so this is the assumed format
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.sub_interval or '',
                                                                                self.number or '', self.modifier or ''))


## @param value Required {1-31}
class ChronoDayOfMonthEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, sub_interval=None,
                 number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Day-Of-Month")
        self.value = value
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.value,
                                                                                self.sub_interval or '',
                                                                                self.number or '', self.modifier or ''))


## @param day_type Required {"Monday" - "Sunday"}
class ChronoDayOfWeekEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, day_type, sub_interval=None,
                 number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Day-Of-Week")
        self.day_type = day_type
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_day_type(self, day_type):
        self.day_type = day_type

    def get_day_type(self):
        return self.day_type

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.day_type,
                                                                                self.sub_interval or '',
                                                                                self.number or '', self.modifier or ''))


## @param value Required {0-24}
# @param ampm Optional, refers to a ChronoAMPMOfDayEntity
# @param time_zone Optional, refers to a ChronoTimeZoneEntity
class ChronoHourOfDayEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, ampm=None, time_zone=None,
                 sub_interval=None, number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Hour-Of-Day")
        self.value = value
        self.ampm = ampm
        self.time_zone = time_zone
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_ampm(self, ampm):
        self.ampm = ampm

    def get_ampm(self):
        return self.ampm

    def set_time_zone(self, time_zone):
        self.time_zone = time_zone

    def get(self):
        return self.time_zone

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<AMPM-Of-Day>{}</AMPM-Of-Day>\n"
                                      "\t\t\t<Time-Zone>{}</Time-Zone>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.value, self.ampm or '',
                                                                                self.time_zone or '',
                                                                                self.sub_interval or '',
                                                                                self.number or '',
                                                                                self.modifier or ''))


## @param value Required {0-59}
class ChronoMinuteOfHourEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, sub_interval=None, number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Minute-Of-Hour")
        self.value = value
        self.sub_interval = sub_interval
        self.number = number
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t\t<Number>{}</Number>\n\t\t\t<Modifier>{}</Modifier>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.value,
                                                                                self.sub_interval or '',
                                                                                self.number or '', self.modifier or ''))


## @param value Required {0-59}
class ChronoSecondOfMinuteEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, value, number=None, modifier=None):
        super().__init__(entityID, start_span, end_span, "Second-Of-Minute")
        self.value = value
        self.number = number
        self.modifier = modifier

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.value, self.number or '', self.modifier or ''))


## Specifies a number of {days, weeks, months, etc}
# @param calendar_type Required {Day, Month, Week, etc}
class ChronoCalendarIntervalEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, calendar_type, number=None,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Calendar-Interval")
        self.calendar_type = calendar_type
        self.number = number
        self.modifier = modifier

    def set_calendar_type(self, calendar_type):
        self.calendar_type = calendar_type

    def get_calendar_type(self):
        return self.calendar_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.calendar_type, self.number or '', self.modifier or ''))


## @param part_of_day_type Required {Night, Morning, etc}
class ChronoPartOfDayEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, part_of_day_type, number=None,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Part-Of-Day")
        self.part_of_day_type = part_of_day_type
        self.number = number
        self.modifier = modifier

    def set_part_of_day_type(self, part_of_day_type):
        self.part_of_day_type = part_of_day_type

    def get_part_of_day_type(self):
        return self.part_of_day_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.part_of_day_type, self.number or '', self.modifier or ''))


## @param part_of_week_type Required {Weekend, etc}
class ChronoPartOfWeekEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, part_of_week_type, number=None,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "Part-Of-Week")
        self.part_of_week_type = part_of_week_type
        self.number = number
        self.modifier = modifier

    def set_part_of_week_type(self, part_of_week_type):
        self.part_of_week_type = part_of_week_type

    def get_part_of_week_type(self):
        return self.part_of_week_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.part_of_week_type, self.number or '', self.modifier or ''))


## @param ampm_type Required {AM, PM}
class ChronoAMPMOfDayEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span, ampm_type, number=None,
                 modifier=None):
        super().__init__(entityID, start_span, end_span, "AMPM-Of-Day")
        self.ampm_type = ampm_type
        self.number = number
        self.modifier = modifier

    def set_ampm_type(self, ampm_type):
        self.ampm_type = ampm_type

    def get_ampm_type(self):
        return self.ampm_type

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t\t<Number>{}</Number>\n"
                                      "\t\t\t<Modifier>{}</Modifier>\n\t\t</properties>\n\t</entity>\n".format(
            self.ampm_type, self.number or '', self.modifier or ''))


## No special parameters, just identifies the location of a time zone in text
class ChronoTimeZoneEntity(ChronoRepeatingIntervalEntity):
    def __init__(self, entityID, start_span, end_span):
        super().__init__(entityID, start_span, end_span, "Time-Zone")

    def print_xml(self):
        return (super().print_xml() + "</properties>\n\t</entity>\n")


## Super class for all Operators
class ChronoOperator(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, operator_type):
        super().__init__(entityID, start_span, end_span, operator_type, "Operator")


class ChronoSumOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, period_1, period_2):
        super().__init__(entityID, start_span, end_span, "Sum")
        self.period_1 = period_1
        self.period_2 = period_2

    def set_period_1(self, period_1):
        self.period_1 = period_1

    def get_period_1(self):
        return self.period_1

    def set_period_2(self, period_2):
        self.period_2 = period_2

    def get_period_2(self):
        return self.period_2

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Period>{}</Period>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.period_1, self.period_2))


class ChronoDifferenceOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, period_1, period_2):
        super().__init__(entityID, start_span, end_span, "Difference")
        self.period_1 = period_1
        self.period_2 = period_2

    def set_period_1(self, period_1):
        self.period_1 = period_1

    def get_period_1(self):
        return self.period_1

    def set_period_2(self, period_2):
        self.period_2 = period_2

    def get_period_2(self):
        return self.period_2

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Period>{}</Period>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.period_1, self.period_2))


class ChronoUnionOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, repeating_intervals_1,
                 repeating_intervals_2):
        super().__init__(entityID, start_span, end_span, "Union")
        self.repeating_intervals_1 = repeating_intervals_1
        self.repeating_intervals_2 = repeating_intervals_2

    def set_repeating_intervals_1(self, repeating_intervals_1):
        self.repeating_intervals_1 = repeating_intervals_1

    def get_repeating_intervals_1(self):
        return self.repeating_intervals_1

    def set_repeating_intervals_2(self, repeating_intervals_2):
        self.repeating_intervals_2 = repeating_intervals_2

    def get_repeating_intervals_2(self):
        return self.repeating_intervals_2

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Repeating-Intervals>{}</Repeating-Intervals>\n"
                                      "\t\t\t<Repeating-Intervals>{}</Repeating-Intervals>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.repeating_intervals_1,
                                                                                self.repeating_intervals_2))


class ChronoIntersectionOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, repeating_intervals_1,
                 repeating_intervals_2):
        super().__init__(entityID, start_span, end_span, "Intersection")
        self.repeating_intervals_1 = repeating_intervals_1
        self.repeating_intervals_2 = repeating_intervals_2

    def set_repeating_intervals_1(self, repeating_intervals_1):
        self.repeating_intervals_1 = repeating_intervals_1

    def get_repeating_intervals_1(self):
        return self.repeating_intervals_1

    def set_repeating_intervals_2(self, repeating_intervals_2):
        self.repeating_intervals_2 = repeating_intervals_2

    def get_repeating_intervals_2(self):
        return self.repeating_intervals_2

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Repeating-Intervals>{}</Repeating-Intervals>\n"
                                      "\t\t\t<Repeating-Intervals>{}</Repeating-Intervals>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.repeating_intervals_1,
                                                                                self.repeating_intervals_2))


## No examples, currently a placeholder
class ChronoEveryNthOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span):
        super().__init__(entityID, start_span, end_span, "Every-Nth")


## Create a last(Period) or last(Repeating-Interval) operator,
# must specify one or the other
# @param semantics {Interval-Included, Interval-Not-Included(default)}
# @param interval_type Defaults to ""
# @param interval Defaults to None
# @param period Defaults to None
# @param repeating_interval Defaults to None
class ChronoLastOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, semantics="Interval-Not-Included",
                 interval_type="DocTime", interval=None, period=None,
                 repeating_interval=None):
        super().__init__(entityID, start_span, end_span, "Last")
        self.semantics = semantics
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval

    def set_semantics(self, semantics):
        self.semantics = semantics

    def get_semantics(self):
        return self.semantics

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Semantics>{}</Semantics>\n"
                                      "\t\t\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.semantics,
                                                                                self.interval_type, self.interval or '',
                                                                                self.period or '',
                                                                                self.repeating_interval or ''))


## Create a next(Period) or next(Repeating-Interval) operator,
# must specify one or the other
# @param interval_type Defaults to "DocTime"
# @param interval Defaults to None
# @param period Defaults to None
# @param repeating_interval Defaults to None
# @param semantics {Interval-Included, Interval-Not-Included(default)}
class ChronoNextOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, interval_type="DocTime",
                 interval=None, period=None, repeating_interval=None,
                 semantics="Interval-Not-Included"):
        super().__init__(entityID, start_span, end_span, "Next")
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval
        self.semantics = semantics

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    def set_semantics(self, semantics):
        self.semantics = semantics

    def get_semantics(self):
        return self.semantics

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t\t<Semantics>{}</Semantics>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type,
                                                                                self.interval or '', self.period or '',
                                                                                self.repeating_interval or '',
                                                                                self.semantics))


## Create a This(Period) or This(Repeating-Interval) operator,
# must specify one or the other
# @param interval_type Defaults to "DocTime"
# @param interval Defaults to None
# @param period Defaults to None
# @param repeating_interval Defaults to None
class ChronoThisOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, interval_type="DocTime",
                 interval=None, period=None, repeating_interval=None):
        super().__init__(entityID, start_span, end_span, "This")
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type,
                                                                                self.interval or '', self.period or '',
                                                                                self.repeating_interval or ''))


## Create a before(Period) or before(Repeating-Interval) operator,
# must specify one or the other
# @param interval_type Defaults to "DocTime"
# @param interval Defaults to None
# @param period Defaults to None
# @param repeating_interval Defaults to None
# @param semantics {Interval-Included, Interval-Not-Included(default)}
class ChronoBeforeOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, interval_type="DocTime",
                 interval=None, period=None, repeating_interval=None,
                 semantics="Interval-Not-Included"):
        super().__init__(entityID, start_span, end_span, "Before")
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval
        self.semantics = semantics

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    def set_semantics(self, semantics):
        self.semantics = semantics

    def get_semantics(self):
        return self.semantics

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t\t<Semantics>{}</Semantics>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type,
                                                                                self.interval or '', self.period or '',
                                                                                self.repeating_interval or '',
                                                                                self.semantics))


## Create an after(Period) or after(Repeating-Interval) operator,
# must specify one or the other
# @param interval_type Defaults to "DocTime"
# @param interval Defaults to None
# @param period Defaults to None
# @param repeating_interval Defaults to None
# @param semantics {Interval-Included, Interval-Not-Included(default)}
class ChronoAfterOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, interval_type="DocTime",
                 interval=None, period=None, repeating_interval=None,
                 semantics="Interval-Not-Included"):
        super().__init__(entityID, start_span, end_span, "After")
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval
        self.semantics = semantics

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    def set_semantics(self, semantics):
        self.semantics = semantics

    def get_semantics(self):
        return self.semantics

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t\t<Semantics>{}</Semantics>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type,
                                                                                self.interval or '', self.period or '',
                                                                                self.repeating_interval or '',
                                                                                self.semantics))


## Creates a between operator e.g. Between(Last(January(13)), DocTime)
# @param start_interval_type {Link, DocTime}
# @param start_interval Takes a link to an interval or None(Default) for DocTime
# @param end_interval_type {Link, DocTime}
# @param end_interval Takes a link to an interval or None(Default) for DocTime
# @param start_included {Included, Not-Included(default)}
# @param end_included {Included, Not-Included(default)}
class ChronoBetweenOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, start_interval_type,
                 end_interval_type, start_interval=None, end_interval=None,
                 start_included="Not-Included", end_included="Not-Included"):
        super().__init__(entityID, start_span, end_span, "Between")
        self.start_interval_type = start_interval_type
        self.start_interval = start_interval
        self.end_interval_type = end_interval_type
        self.end_interval = end_interval
        self.start_included = start_included
        self.end_included = end_included

    def set_start_interval_type(self, start_interval_type):
        self.start_interval_type = start_interval_type

    def get_start_interval_type(self):
        return self.start_interval_type

    def set_start_interval(self, start_interval):
        self.start_interval = start_interval

    def get_start_interval(self):
        return self.start_interval

    def set_end_interval_type(self, end_interval_type):
        self.end_interval_type = end_interval_type

    def get_end_interval_type(self):
        return self.end_interval_type

    def set_end_interval(self, end_interval):
        self.end_interval = end_interval

    def get_end_interval(self):
        return self.end_interval

    def set_start_included(self, start_included):
        self.start_included = start_included

    def get_start_included(self):
        return self.start_included

    def set_end_included(self, end_included):
        self.end_included = end_included

    def get_end_included(self):
        return self.end_included

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Start-Interval-Type>{}</Start-Interval-Type>\n"
                                      "\t\t\t<Start-Interval>{}</Start-Interval>\n"
                                      "\t\t\t<End-Interval-Type>{}</End-Interval-Type>\n"
                                      "\t\t\t<End-Interval>{}</End-Interval>\n"
                                      "\t\t\t<Start-Included>{}</Start-Included>\n"
                                      "\t\t\t<End-Included>{}</End-Included>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.start_interval_type,
                                                                                self.start_interval or '',
                                                                                self.end_interval_type,
                                                                                self.end_interval or '',
                                                                                self.start_included, self.end_included))


## Creates and Nth operator e.g. 5th(Value) day(Calendar-Interval)
# of 2016(Repeating-Interval)
# @param value The N in Nth
# @param interval The Calendar-Interval to link to
# @param repeating_interval The repeating interval to link to
class ChronoNthOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, value=None, interval=None, interval_type="DocTime",
                 repeating_interval=None, period=None):
        super().__init__(entityID, start_span, end_span, "NthFromStart")
        self.value = value
        self.interval_type = interval_type
        self.interval = interval
        self.period = period
        self.repeating_interval = repeating_interval

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_period(self, period):
        self.period = period

    def get_period(self):
        return self.period

    def set_repeating_interval(self, repeating_interval):
        self.repeating_interval = repeating_interval

    def get_repeating_interval(self):
        return self.repeating_interval

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Value>{}</Value>\n"
                                      "\t\t\t<Period>{}</Period>\n"
                                      "\t\t\t<Repeating-Interval>{}</Repeating-Interval>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type or '',
                                                                                self.interval or '', self.value or '',
                                                                                self.period or '',
                                                                                self.repeating_interval or ''))


## Creates a two digit year operator
# @param interval_type Defaults to DocTime
# @param interval Defaults to None
class ChronoTwoDigitYearOperator(ChronoOperator):
    def __init__(self, entityID, start_span, end_span, value, sub_interval=None,
                 interval_type="DocTime", interval=None):
        super().__init__(entityID, start_span, end_span, "Two-Digit-Year")
        self.interval_type = interval_type
        self.interval = interval
        self.value = value
        self.sub_interval = sub_interval

    def set_interval_type(self, interval_type):
        self.interval_type = interval_type

    def get_interval_type(self):
        return self.interval_type

    def set_interval(self, interval):
        self.interval = interval

    def get_interval(self):
        return self.interval

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_sub_interval(self, sub_interval):
        self.sub_interval = sub_interval

    def get_sub_interval(self):
        return self.sub_interval

    def print_xml(self):
        return (super().print_xml() + "\t<Interval-Type>{}</Interval-Type>\n"
                                      "\t\t\t<Interval>{}</Interval>\n\t\t\t<Value>{}</Value>\n"
                                      "\t\t\t<Sub-Interval>{}</Sub-Interval>\n"
                                      "\t\t</properties>\n\t</entity>\n".format(self.interval_type or '',
                                                                                self.interval or '', self.value or '',
                                                                                self.sub_interval or ''))


## Super class for all Other entities
class ChronoOtherEntity(ChronoEntity):
    def __init__(self, entityID, start_span, end_span, otherType):
        super().__init__(entityID, start_span, end_span, otherType, "Other")


class ChronoNumber(ChronoOtherEntity):
    def __init__(self, entityID, start_span, end_span, value):
        super().__init__(entityID, start_span, end_span, "Number")
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Value>{}</Value>\n\t\t</properties>\n\t"
                                      "</entity>\n".format(self.value))
    def print_ann(self):
        return ("T{}\tNumber {} {}\t{}".format(self.entityID, self.start_span, self.end_span, self.value))#HAVE TO FIX LATER


class ChronoModifier(ChronoOtherEntity):
    def __init__(self, entityID, start_span, end_span, modifier):
        super().__init__(entityID, start_span, end_span, "Modifier")
        self.modifier = modifier

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    #
    def print_xml(self):
        return (super().print_xml() + "\t<Type>{}</Type>\n\t\t</properties>\n\t"
                                      "</entity>\n".format(self.modifier))


class ChronoEvent(ChronoOtherEntity):
    def __init__(self, entityID, start_span, end_span):
        super().__init__(entityID, start_span, end_span, "Event")

    #
    def print_xml(self):
        return (super().print_xml() + "</properties>\n\t</entity>\n")

