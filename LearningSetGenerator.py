import os
import argparse
import json

import random
from   random import randint
from   random import choice

from CustomTypes import TClass
from CustomTypes import TObject
from CustomTypes import TObservation
from CustomTypes import TSymptom
from CustomTypes import TObservationMoment

import Config as CFG

################################################################################
# Procedures definition
################################################################################

def gen_observation_moments(symptom: TSymptom) -> list[TObservationMoment]:
    result = []

    # Need to be generated separately to be able to recalculate moments time
    # from relative to period timescale to absolute timescale.
    durations = [randint(period['duration_lower'], period['duration_upper']) for period in symptom['periods']]

    # Offsets for recalculating moments time to absolute timescale.
    # Basically it's also a period start time.
    periods_time_offset = [0]
    for i in range(len(durations) - 1):
        periods_time_offset.append(periods_time_offset[i] + durations[i])

    for i in range(len(symptom['periods'])):
        duration    = durations[i]
        period      = symptom['periods'][i]
        time_offset = periods_time_offset[i]

        # Each period has at least MIN_OBSERVATION_MOMENTS_PER_SYMPTOM_NUM observation moments.
        moments = CFG.MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM

        # Calculate the probability of extra observation moments appearing.
        # Longer the period duration, higher the probability.
        # Probability would be 0 if duration doesn't fit more than CFG.MIN_OBSERVATION_MOMENTS_PER_SYMPTOM_NUM.
        probability = (duration - CFG.MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM) / CFG.MAX_PERIOD_DURATION

        if probability != 0 and probability >= random.uniform(0, 1):
            if CFG.MAX_EXTRA_OBSERVATION_MOMENTS_PER_PERIOD_NUM != 0:
                moments += randint(1, min(duration - moments, CFG.MAX_EXTRA_OBSERVATION_MOMENTS_PER_PERIOD_NUM))

        # Time in relative to period timescale.
        moments_time_relative_timescale = sorted(random.sample(range(1, duration + 1), moments))

        # Recalculate to absolute timescale.
        moments_time_absolute_timescale = [(t + time_offset) for t in moments_time_relative_timescale]

        for time_rel, time_abs in zip(moments_time_relative_timescale, moments_time_absolute_timescale):
            result.append(
                {
                    # 'dbg_period_idx'     : i,
                    # 'dbg_period_duration': duration,
                    # 'dbg_time_relative'  : time_rel,
                    'time'               : time_abs,
                    'value'              : choice(period['values'])
                }
            )

    return result



def gen_observations(symptoms: list[TSymptom]) -> list[TObservation]:
    result = []

    for symptom in symptoms:
        result.append(
            {
                'feature'            : symptom['feature'],
                'observation_moments': gen_observation_moments(symptom)
            }
        )

    return result



def gen_object(class_descr: TClass) -> TObject:
    return {
        'class'       : class_descr['name'],
        'observations': gen_observations(class_descr['symptoms'])
    }



def gen_learning_set(classes_descr: list[TClass]) -> list[TObject]:
    result = []

    for class_descr in classes_descr:
        for n in range(randint(CFG.MIN_OBJECTS_PER_CLASS_NUM, CFG.MAX_OBJECTS_PER_CLASS_NUM)):
            result.append(gen_object(class_descr))

    return result

################################################################################
# Main
################################################################################

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(allow_abbrev=False)

    arg_parser.add_argument(
        '-o', '--output',
        dest='output',
        required=True,
        type=str,
        help="path to the output json file"
    )

    arg_parser.add_argument(
        '-i', '--input',
        dest='input',
        required=True,
        type=str,
        help="path to the knowledge base model json file"
    )

    args = arg_parser.parse_args()

    output_dir = os.path.dirname(args.output)
    if output_dir != "" and not os.path.isdir(output_dir):
        print('Directory \"{}\" doesn\'t exist'.format(output_dir))
        exit(-1)

    input_dir = os.path.dirname(args.input)
    if input_dir != "" and not os.path.isdir(input_dir):
        print('Directory \"{}\" doesn\'t exist'.format(input_dir))
        exit(-1)

################################################################################

    random.seed(CFG.LEARNING_SET_GENERATION_SEED)

################################################################################

    with open(args.input, "r", encoding="UTF-8") as f:
        knowledge_base_model = json.load(f)

    learning_set = gen_learning_set(knowledge_base_model['classes'])

    with open(args.output, "w", encoding="UTF-8") as f:
        json.dump(learning_set, f, ensure_ascii=False, indent=4)