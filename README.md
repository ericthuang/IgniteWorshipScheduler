# Ignite Worship Scheduler

## Description
Ignite Worship Scheduler (IWS, ver 3) generates an optimal set of weekly band assignments. 

Without considering blackout dates, we have (very) roughly 1.36E+39 possible unique schedules for a given quarter. If we consider blackout dates, the number is reduced significantly, but the number of possible unique schedules is still astronomically large. 

By default, 10,000,000 random possible schedules are examined, scored, and ranked. 

![](https://thumbs.gfycat.com/BetterThankfulEnglishsetter-max-1mb.gif)

## Libraries Used
Nothing besides standard python lib.

## Possible Roles
* `lead` - Worship Leader
* `vocals` - Vocalist/Singer
* `leadKeys` - Lead Keyboardist (midi, synth, pads, percussion, loops, tracks, bass, click, etc.) 
* `rhythmKeys` - Rhythm Keyboardist (piano, pads, click)
* `acoustic` - Acoustic Guitarist
* `leadElectric` - Lead Electric Guitarist 
* `rhythmElectric` - Rhythm Electric Guitarist
* `bass` - Bassist
* `drums` - Drummer
* `percussion` - Percussionist (percussion sampling pad, ableton, etc.)
See `RoleParameters.json`

### Map of Possible Combinations
See `RoleParameters.json`

## IWS Algo
For N iterations:
1. Semi-randomly generate a schedule of X Sunday bands that adheres to the following conditions:
* Members are not assigned if date is blacked out
* Members are assigned to serve only within their primary or secondary role(s)
* Each band must have one lead (vocalist)
* Each band has no more than 2 leads (vocalist)
* Each band must have one lead rhythm instrument (see 'Possible Lead Rhythm Roles')
* Each band has no more than one of each: 
  * lead keyboardist, rhythm keyboardist, drummer, percussionist, bassist

2. Score set of Sunday bands (starting at 0) as follows: 
* +5 low utilization mean across all members in schedule
* +5 low utilization variability (standard deviation) across all members in schedule
* +3 for every band in schedule that is complete (meets all minimum requirements as defined by `RoleParameters.json`
* +2 for every band in schedule that has two leaders
* +2 for every band in schedule that has at least one non-lead vocalist
* +2 for every band in schedule that has a lead electric guitarist
* +2 for every band in schedule that has a lead keyboardist
* +2 for every band in schedule that has a percussionist
* +10 for each pair of consecutive Sunday bands that don't have carryover members (members serving 2 consecutive weeks)
* +10 for each set of 3 consecutive Sunday bands that don't have any carryover members

3. Output top 3 schedules (+ supporting metrics) for human evaluation

Why do it this way? Using rules/logic to generate schedules is friggin hard. Judging stochastically bruteforced results is way easier. Is this the best solution? Probably not. But easiest to implement forsure.


## Future Features/Improvements
* Integrate into web service for more automation (pull directly from mongo)
* Optimize by hashing and memoizing already generated schedules so that we dont look at the same one twice
* Parallelization to save time
* more 'intelligent' pruning to further reduce number of possibilities, including feedback of previous Sunday band into pruning process
* An overall different, non-stochastic, non-bruteforcey approach (tried, too hard/complex)

## Changelog (from V2):
* additive scoring only, no more subtractive scoring
* pruning possible band candidates instead of purely logical decision making
* addition of RoleParameters.json to enforce some 'rules'
* new input json format
* conformity to PEP 8


