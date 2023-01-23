
################################################################################
# Config
################################################################################

# Set to None for non-fixed random
MODEL_DATABASE_GENERATION_SEED = 0
LEARNING_SET_GENERATION_SEED   = 0

# Features configuration
MIN_FEATURES_NUM          = 5
MAX_FEATURES_NUM          = 5

# Features values configuration
MIN_VALUES_NUM            = 10
MAX_VALUES_NUM            = 15
MIN_NORMAL_VALUES_NUM     = 1
MIN_ABNORMAL_VALUES_NUM   = 1

# Periods configuration
MIN_PERIODS_NUM           = 1
MAX_PERIODS_NUM           = 5
MIN_PERIOD_DURATION       = 1
MAX_PERIOD_DURATION       = 24
MIN_VALUES_PER_PERIOD     = 1
MAX_VALUES_PER_PERIOD     = 5

# Classes configuration
MIN_CLASSES_NUM           = 5
MAX_CLASSES_NUM           = 5
MIN_FEATURES_IN_CLASS_NUM = 5

################################################################################

# Objects generation configuration
MIN_OBJECTS_PER_CLASS_NUM = 3
MAX_OBJECTS_PER_CLASS_NUM = 3

# Observation moments generation configuration
MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM       = 1
MAX_EXTRA_OBSERVATION_MOMENTS_PER_PERIOD_NUM = 2

################################################################################
# Validation
################################################################################

assert MIN_FEATURES_NUM <= MAX_FEATURES_NUM
assert MIN_FEATURES_NUM >= MIN_FEATURES_IN_CLASS_NUM

assert MIN_PERIODS_NUM <= MAX_PERIODS_NUM
assert MIN_PERIOD_DURATION < MAX_PERIOD_DURATION

assert MIN_VALUES_NUM <= MAX_VALUES_NUM
assert MIN_VALUES_NUM >= MIN_NORMAL_VALUES_NUM + MIN_ABNORMAL_VALUES_NUM

assert MIN_CLASSES_NUM <= MAX_CLASSES_NUM

assert MIN_VALUES_PER_PERIOD <= MAX_VALUES_PER_PERIOD
assert MIN_VALUES_PER_PERIOD > 0

assert MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM > 0

# Let's assume:
#   1) generated values_num = MIN_VALUES_NUM;
#   2) there're periods p1 and following p2;
#   3) p1 got MIN_VALUES_PER_PERIOD values.
#
# That means that there's (values_num - MIN_VALUES_PER_PERIOD) values
# left to choose from for p2.
#
# (values_num - MIN_VALUES_PER_PERIOD) can't be lower than MIN_VALUES_PER_PERIOD
assert MIN_VALUES_NUM >= MIN_VALUES_PER_PERIOD * 2

assert MIN_OBJECTS_PER_CLASS_NUM <= MAX_OBJECTS_PER_CLASS_NUM

# MIN_PERIOD_DURATION must be able to fit MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM
assert MIN_PERIOD_DURATION >= MIN_OBSERVATION_MOMENTS_PER_PERIOD_NUM
