# =============================================================================
# Import Section Start
# =============================================================================
import pandas as pd
import numpy as np
#import matplotlib as plt

# =============================================================================
# Import Section End
# =============================================================================

#%% [Function Definitions]

def die_roll(dice = 1):
    result = pd.Series(np.random.randint(1,6,6))
    score = score_check(result)
    return score, result

def farkle_check(score):
    if score > 0:
        return 1
    else: return 0

def check_5(value_counts, score):
    if value_counts.iloc[0] == 5:
        score += 2000
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    return score    

def check_4(value_counts, score):
    if value_counts.iloc[0] == 4:
        score += 1000
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    return score

    5 in value_counts[5]

def check_3(value_counts, score):
    if value_counts.iloc[0] == 3:
        score += 100*value_counts.index[0]
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    return score
    
def score_check(result):
    score = 0
    value_counts = result.value_counts()    
    if len(result) == 6:
        if value_counts.iloc[0] == 6:
            score = 3000
            return score
        elif value_counts.iloc[0] == 3 and value_counts.iloc[1] == 3:
            score = 2500
            return score
        elif value_counts.iloc[0] == 4 and value_counts.iloc[1] == 2:
            score = 1500
            return score
        elif value_counts.iloc[0] == 2 and value_counts.iloc[1] == 2 and value_counts.iloc[2] == 2:
            score = 1500
            return score
        elif sorted(result) == [1,2,3,4,5,6]:
            score = 1500
            return score
        score = check_5(value_counts, score)
        if score > 0:
            return score
        score += check_4(value_counts, score)
        if score > 0:
            return score
        score += check_3(value_counts, score)
        if score > 0:
            return score
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    if len(result) == 5:
        score += check_5(value_counts, score)
        if score > 0:
            return score
        score += check_4(value_counts, score)
        if score > 0:
            return score
        score += check_3(value_counts, score)
        if score > 0:
            return score
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    if len(result) == 4:
        score += check_4(value_counts, score)
        if score > 0:
            return score
        score += check_3(value_counts, score)
        if score > 0:
            return score
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    if len(result) == 3:
        score += check_3(value_counts, score)
        if score > 0:
            return score
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    else:
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
    return score

def play_a_round(roll_dice, used_dice, score):
    score_hold, result = die_roll(roll_dice)
    
#%%
score = input("Enter current score:")
roll_dice = int(input("Enter dice available to roll:"))
used_dice = 6-roll_dice

die_roll(roll_dice)
mc = pd.DataFrame([die_roll(roll_dice) for i in range(10000)], columns = ['Score', 'Result'] )

mc['Score'].mean()

farkle_chance = mc['Score'].value_counts()[0]/10000

mc['Score'].plot.hist()
