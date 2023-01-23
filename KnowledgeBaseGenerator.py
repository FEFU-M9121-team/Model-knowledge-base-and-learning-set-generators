import os
import argparse
import json

import random
from   random import randint

from CustomTypes import TFeature
from CustomTypes import TPeriod
from CustomTypes import TClass

import Config as CFG

################################################################################
# Procedures definition
################################################################################

def generate_features() -> list[TFeature]:
    result = []

    features_num = randint(CFG.MIN_FEATURES_NUM, CFG.MAX_FEATURES_NUM)

    for i in range(features_num):
        values_num = randint(
            CFG.MIN_VALUES_NUM,
            CFG.MAX_VALUES_NUM
        )
        normal_values_num = randint(
            CFG.MIN_NORMAL_VALUES_NUM,
            values_num - CFG.MIN_ABNORMAL_VALUES_NUM
        )

        result.append(
            {
                'name'         : 'feature{}'.format(i),
                'values'       : ['f{}value{}'.format(i, j) for j in range(values_num)],
                'normal_values': ['f{}value{}'.format(i, j) for j in range(normal_values_num)]
            }
        )

    return result



def generate_periods(feature_values: list[str]) -> list[TPeriod]:
    result = []

    periods_num = randint(CFG.MIN_PERIODS_NUM, CFG.MAX_PERIODS_NUM)

    period_values = []

    for i in range(periods_num):
        if i == 0:
            count = randint(CFG.MIN_VALUES_PER_PERIOD, min(CFG.MAX_VALUES_PER_PERIOD, len(feature_values) - CFG.MIN_VALUES_PER_PERIOD))
            period_values.append(random.sample(feature_values, count))
        else:
            possible_values = [v for v in feature_values if not v in period_values[i - 1]]
            count = randint(CFG.MIN_VALUES_PER_PERIOD, min(CFG.MAX_VALUES_PER_PERIOD, len(possible_values)))
            period_values.append(random.sample(possible_values, count))


    for i in range(periods_num):
        duration_lower = randint(CFG.MIN_PERIOD_DURATION, CFG.MAX_PERIOD_DURATION - 1)
        duration_upper = randint(duration_lower + 1, CFG.MAX_PERIOD_DURATION)
        result.append(
            {
                'duration_lower': duration_lower,
                'duration_upper': duration_upper,
                'values'        : period_values[i]
            }
        )

    return result



def generate_classes(features: list[TFeature]) -> list[TClass]:
    result = []

    classes_num  = randint(CFG.MIN_CLASSES_NUM, CFG.MAX_CLASSES_NUM)

    for i in range(classes_num):
        features_in_class_num = randint(CFG.MIN_FEATURES_IN_CLASS_NUM, len(features))
        selected_features = sorted(random.sample(features, features_in_class_num), key=lambda d: d['name'])

        class_symptoms = []

        for feature in selected_features:
            class_symptoms.append(
                {
                    'feature': feature['name'],
                    'periods': generate_periods(feature['values'])
                }
            )

        result.append(
            {
                'name'    : 'disease{}'.format(i),
                'symptoms': class_symptoms
            }
        )

    return result

################################################################################
# Main
################################################################################

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(allow_abbrev=False)

    arg_parser.add_argument(
        '-o', '--output',
        dest='output',
        required=True,
        type=str,
        help="path to the output json file"
    )

    args = arg_parser.parse_args()

    output_dir = os.path.dirname(args.output)
    if output_dir != "" and not os.path.isdir(output_dir):
        print('Directory \"{}\" doesn\'t exist'.format(output_dir))
        exit(-1)

################################################################################

    random.seed(CFG.MODEL_DATABASE_GENERATION_SEED)

################################################################################

    knowledge_database_model = {
        'features': None,
        'classes' : None
    }

    knowledge_database_model['features'] = generate_features()
    knowledge_database_model['classes']  = generate_classes(knowledge_database_model['features'])

    with open(args.output, 'w', encoding="UTF-8") as f:
        json.dump(knowledge_database_model, f, ensure_ascii=False, indent=4)

    exit(0)