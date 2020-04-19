""" Coordinates file. 

Coordinates are relative to in-game top-left corner. 
"""

# some user constants
FAST_SLEEP = 0.15
MEDIUM_SLEEP = 0.3

GAME_WIDTH = 960
GAME_HEIGHT = 600

BASIC_TRAINING = 235, 45
BASIC_TRAINING_ADD = 842, 166
ATK1 = 912, 164
ATK2 = 914, 198
ATK3 = 911, 233
ATK4 = 911, 263
ATK5 = 912, 297
ATK6 = 913, 327
DEF1 = 912, 408
DEF2 = 914, 444
DEF3 = 913, 475
DEF4 = 918, 507
DEF5 = 913, 540
DEF6 = 913, 570

ENERGY_CUSTOM_AMOUNT_CAP = 674, 44
ENERGY_CUSTOM_AMOUNT_HALF = 704, 46
ENERGY_CUSTOM_AMOUNT_QUARTER = 734, 43
ENERGY_CUSTOM_AMOUNT_HALF_IDLE = 868, 46
ENERGY_CUSTOM_AMOUNT_QUARTER_IDLE = 897, 43
MAGIC_CUSTOM_AMOUNT_CAP = 672, 69
MAGIC_CUSTOM_AMOUNT_HALF = 704, 67
MAGIC_CUSTOM_AMOUNT_QUARTER = 734, 67

FIGHT_BOSS = 230, 73
NUKE = 627, 177
FIGHT = 629, 288

MONEY_PIT = 239, 102
FEED_ME = 420, 190
FEED_YEAH = 430, 344

ADVENTURE = 231, 128

ABILITY_OFFSET_X = 104
ABILITY_OFFSET_Y = 35
ABILITY_1 = 463, 119  # Regular attack
# Ability 1 pixel is to take a screenshot only of the pixel we need to check
ABILITY_1_REGION = (463, 119, 2, 2)
ABILITY_ROW_1_READY_COLOR = 248, 155, 155
ABILITY_ROW_2_READY_COLOR = 102, 135, 163
ABILITY_ROW_3_READY_COLOR = 15, 15, 15


IS_IDLE = 414, 144
IS_IDLE_COLOR = 255, 235, 4
ADVANCE_ZONE = 942, 235
GO_BACK_ZONE = 732, 237
# SNIPE COORDS
MY_HEALTH_BAR_BORDER = 320, 439
MY_HEALTH_BAR_THRESHOLD = 450, 440
MY_HEALTH_BAR_FULL = 513, 439  # 100% of player's health bar
ENEMY_HEALTH_BAR = 770, 440
HEALTH_BAR_RED = 235, 52, 52
CROWN_LOCATION = 737, 307
CROWN_COLOR = 247, 239, 41
ENEMY_HEALTH_BAR_BORDER = 737, 439

ITOPOD_ENTER = 371, 252
ITOPOD_OPTIMAL = 701, 231
ITOPOD_MAX = 706, 268
ITOPOD_START_INPUT = 629, 224
ITOPOD_END_INPUT = 625, 261
ITOPOD_ENTER_CONFIRMATION = 614, 321
ITOPOD_PERKS = 452, 252
ITOPOD_PP_REGION = (764, 482, 100, 30)

INVENTORY = 236, 157
INV_DIFF = 50
ACC1 = 481, 87
ACC2 = 481, 139
ACC3 = 481, 189
HEAD = 529, 82
CHEST = 529, 138
LEGS = 537, 188
BOOTS = 532, 241
WEAPON = 585, 138
CUBE = 625, 138
SLOT1 = 356, 354

LOADOUT1 = 329, 285
LOADOUT2 = 359, 281


AUGMENTATION = 236, 187
AUG_DIFF = 65  # on y
AUG1 = 542, 288
AUG1_UPGRADE = 542, 318

# plus buttons
ADV_TRAINING = 229, 212
ADV_TOUGHNESS = 892, 255
ADV_POWER = 892, 293
ADV_BLOCK = 892, 333
ADV_WANDOOS_ENERGY = 892, 374
ADV_WANDOOS_MAGIC = 892, 413


TIME_MACHINE = 230, 237
TM_ADD_ENERGY = 530, 259
TM_ADD_MAGIC = 529, 357

BLOOD_MAGIC = 226, 264
BM1_ADD = 494, 253
BM1_CAP = 567, 251
BM_DIFF = 35  # y

WANDOOS = 231, 292

NGU = 231, 318

YGGDRASIL = 235, 347
FRUITS = {
    'GOLD': (349, 201),
    'POWER_ALPHA': (558, 201),
    'ADVENTURE': (769, 200),
    'KNOWLEDGE': (348, 299),
    'POMEGRANATE': (557, 298),
    'LUCK': (772, 295),
    'POWER_BETA': (348, 394),
    'ARBITRARINESS': (619, 365),
    'NUMBERS': (770, 393)
}
FRUITS_IS_HARVESTED = {
    'GOLD': (338, 171),
    'POWER_ALPHA': (544, 173),
    'ADVENTURE': (743, 173),
    'KNOWLEDGE': (338, 269),
    'POMEGRANATE': (533, 269),
    'LUCK': (744, 271),
    'POWER_BETA': (321, 365),
    'ARBITRARINESS': (533, 365),
    'NUMBERS': (744, 364)
}
FRUIT_GOLD_HARVEST = 347, 201
FRUIT_POWER_HARVEST = 561, 202
FRUIT_POM_HARVEST = 561, 298
HARVEST_ALL_MAX_TIER = 815, 474


REBIRTH_MENU = 91, 445
REBIRTH_BUTTON = 547, 542
REBIRTH_CONFIRMATION = 439, 344


# OCR
EXP_MENU = 91, 480  # EXPERIMENTAL
EXP_REGION = (592, 99, 100, 20)
BOSS_NUMBER_REGION = (785, 334, 80, 20)
