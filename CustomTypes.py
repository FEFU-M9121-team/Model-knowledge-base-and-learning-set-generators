from typing import TypeAlias

################################################################################
# Types definition
################################################################################

#
# { 'name': str, 'values': list[str], 'normal_values': list[str] }
#
TFeature : TypeAlias = dict[str, list[str], list[str]]

#
# { 'duration_lower': int, 'duration_upper': int, 'values': list[str] }
#
TPeriod : TypeAlias = dict[int, int, list[str]]

#
# { 'feature': str, 'periods': list[TPeriod] }
#
TSymptom : TypeAlias = dict[str, list[TPeriod]]

#
# { 'name': str, 'symptoms': list[TSymptom] }
#
TClass : TypeAlias = dict[str, list[TSymptom]]

#
# { 'features': list[TFeature], 'classes': list[TClass] }
#
TDatabaseModel : TypeAlias = dict[list[TFeature], list[TClass]]

#
# { 'time': int, 'value': str }
#
TObservationMoment : TypeAlias = dict[int, str]

#
# { 'feature': str, 'observation_moments': list[TObservationMoment] }
#
TObservation : TypeAlias = dict[str, list[TObservationMoment]]

#
# { 'class': str, 'observations': list[TObservation] }
#
TObject : TypeAlias = dict[str, list[TObservation]]

#
# { 'feature': str, 'periods_alternatives': list[list[TPeriod]] }
#
TSymptomAlternatives : TypeAlias = dict[str, list[list[TPeriod]]]

#
# { 'name': str, 'symptoms_alternatives': list[TSymptomAlternatives] }
#
TClassAlternative : TypeAlias = dict[str, list[TSymptomAlternatives]]