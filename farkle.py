#%% [Import Section]
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
    result = pd.Series(np.random.randint(1,7,dice))
    score, dice_avail = score_check(result, dice)
    return score, result.values, dice_avail

def farkle_check(score):
    if score > 0:
        return 1
    else: return 0
    
def check_6(value_counts, score, dice_avail):
    if value_counts.iloc[0] == 6:
        score = 3000
        return score, 6
    elif value_counts.iloc[0] == 3 and value_counts.iloc[1] == 3:
        score = 2500
        return score, 6
    elif value_counts.iloc[0] == 4 and value_counts.iloc[1] == 2:
        score = 1500
        return score, 6
    elif value_counts.iloc[0] == 2 and value_counts.iloc[1] == 2 and value_counts.iloc[2] == 2:
        score = 1500
        return score, 6
    return score, dice_avail
    
def check_5(value_counts, score, dice_avail):
    if value_counts.iloc[0] == 5:
        score += 2000
        dice_avail -= 5
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
            dice_avail -= value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
            dice_avail -= value_counts[5]
    return score, dice_avail

def check_4(value_counts, score, dice_avail):
    if value_counts.iloc[0] == 4:
        score += 1000
        dice_avail -= 4
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
            dice_avail -= value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
            dice_avail -= value_counts[5]
    return score, dice_avail

def check_3(value_counts, score, dice_avail):
    if value_counts.iloc[0] == 3:
        score += 100*value_counts.index[0]
        dice_avail -= 3
        if 1 in value_counts.index[1:]:
            score += 100*value_counts[1]
            dice_avail -= value_counts[1]
        if 5 in value_counts.index[1:]:
            score += 50*value_counts[5]
            dice_avail -= value_counts[5]
    return score, dice_avail

def check_21(value_counts, score, dice_avail):
    if 1 in value_counts.index:
        score += 100*value_counts[1]
        dice_avail -= value_counts[1]
    if 5 in value_counts.index:
        score += 50*value_counts[5]
        dice_avail -= value_counts[5]
    return score, dice_avail
    
def score_check(result, dice):
    score = 0
    dice_avail = dice
    value_counts = result.value_counts()    
    # 6 dice score combos
    if sorted(result) == [1,2,3,4,5,6]:
        return 1500, 6
    if len(result) == 6:
        score, dice_avail = check_6(value_counts, score, dice_avail)
        if score > 0:
            return score, dice_avail
    # 5 dice score combos
        score, dice_avail = check_5(value_counts, score, dice_avail)
        if score > 0:
            return score, dice_avail  
    # 4 dice score combos    
        score, dice_avail = check_4(value_counts, score, dice_avail)
        if score > 0:
            return score, dice_avail
    # 3 dice score combos
        score, dice_avail = check_3(value_counts, score, dice_avail)
        if score > 0:
            return score, dice_avail 
   # 2 dice or 1 die score combos
        score, dice_avail = check_21(value_counts, score, dice_avail)
        return score, dice_avail
    if len(result) == 5:
   # 5 dice score combos
         score, dice_avail = check_5(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail  
   # 4 dice score combos    
         score, dice_avail = check_4(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail
   # 3 dice score combos
         score, dice_avail = check_3(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail 
   # 2 dice or 1 die score combos
         score, dice_avail = check_21(value_counts, score, dice_avail)
         return score, dice_avail
    if len(result) == 4:
   # 4 dice score combos    
         score, dice_avail = check_4(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail
   # 3 dice score combos
         score, dice_avail = check_3(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail 
   # 2 dice or 1 die score combos
         score, dice_avail = check_21(value_counts, score, dice_avail)
         return score, dice_avail
    if len(result) == 3:
   # 3 dice score combos
         score, dice_avail = check_3(value_counts, score, dice_avail)
         if score > 0:
             return score, dice_avail 
   # 2 dice or 1 die score combos
         score, dice_avail = check_21(value_counts, score, dice_avail)
         return score, dice_avail
    else:
   # 2 dice or 1 die score combos
         score, dice_avail = check_21(value_counts, score, dice_avail)
         return score, dice_avail

def play_a_round(score, roll_dice):
    results = pd.DataFrame([die_roll(roll_dice)], columns = ['Score', 'Result', 'Dice Avail'])
    dice_avail = results['Dice Avail'].values[0]
    
    while roll_dice > dice_avail:
        roll_dice = dice_avail
        if roll_dice == 0:
            roll_dice = 6
        if roll_dice < 6 and results['Score'].cumsum().tail(1).values[0]*(threshold[roll_dice]) > calc_risk[roll_dice]:
            break
        results = pd.concat([results, pd.DataFrame([die_roll(roll_dice)], columns = ['Score', 'Result', 'Dice Avail'])])
        dice_avail = results.tail(1)['Dice Avail'].values[0]
    results['Cum Score'] = results['Score'].cumsum()
    if results['Score'].tail(1).values[0] == 0:
        return 0
    return results['Cum Score'].tail(1).values[0]

def score_analyzer(score, roll_dice):
    mc = pd.DataFrame([play_a_round(score,roll_dice) for i in range(10000)], columns = ['Score'], dtype = object )
    farkle_chance = mc['Score'].value_counts()[0]/10000
    score_chance = 1-farkle_chance
    poss_score = mc['Score'].mean()*score_chance+score
    mc['Poss Score'] = poss_score
    mc['Score %'] = score_chance*100
    mc['Farkle %'] = farkle_chance*100
    return mc[['Poss Score', 'Score %', 'Farkle %']].drop_duplicates()

#%%

farkle_risk = {6:.023, 5:.079, 4:.16, 3:.2808, 2:.4444, 1:.6667}
score_risk = {6:650, 5:400, 4:300, 3:200, 2:150, 1:50}
calc_risk = {6:635, 5:368, 4:252, 3:144, 2:83, 1:17}
threshold = {6:1.1, 5:1.8, 4:1.8, 3:1.8, 2:.8, 1:1.10}
score = int(input("Enter current score:"))
roll_dice = int(input("Enter dice available to roll:"))

results = pd.DataFrame(score_analyzer(score, roll_dice), columns = ['Poss Score', 'Score %', 'Farkle %'])
#%%


results.plot.line(y =['Poss Score', 'Farkle %'])
