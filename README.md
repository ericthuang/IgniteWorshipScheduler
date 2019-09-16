# Ignite Worship Scheduler (PyCharm Project)

## Description
Version 3 of Ignite Worship Scheduler (IWS) generates an optimal set of weekly band assignments. 

Without considering blackout dates, we have (very) roughly 1.36e+39 possible unique schedules for a given quarter. If we consider blackout dates, the number is reduced significantly, but the number of possible unique schedules is still astronomically large. 

By default, 10,000,000 random possible schedules are examined, scored, and ranked. 

![](drstrange.gif)

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

2. Score set of Sunday bands as follows: 
* +3 for each sunday band that is complete (contains leader, lead rhythm instrument, bass, keys, drums)
* +2 if low variability of utilization across all ministry members (goal is for close to uniform utilization)
* +2 for each pair of consecutive Sundays that do not have carryover members (check with moving window)
* +2 for each set of 3 consecutive Sundays that do not have carryover members (check with moving window)
* +2 for each sunday band that has two leads
* +2 for each sunday band that has a secondary vocalist
* +2 for each sunday band that has a lead electric guitarist
* +1 for each sunday band that that has a second keyboardist
* +1 for each sunday band that has a percussionist
* +1 for each member that serves in their secondary role at least once per term and no more than 50% of their Sundays

3. Output top 3 schedules (+ supporting metrics) for human evaluation

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


