# Ignite Worship Scheduler

## Description
The Ignite Worship Scheduler (IWS) generates an optimal set of weekly band assignments. 

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
* `percussionist` - Percussionist (percussion sampling pad, ableton, etc.)

### Possible Lead Rhythm Roles
`rhythmKeys`, `acoustic`, `rhythmElectric`

### Map of Possible Combinations
See `RoleMapping.json`

## Algo
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
* +3 for each worship set that is complete (contains leader, lead rhythm instrument, bass, keys, drums)
* +2 if low variability of utilization across all ministry members (goal is for close to uniform utilization)
* +2 for each pair of consecutive Sundays that do not have carryover members (check with moving window)
* +2 for each set of 3 consecutive Sundays that do not have carryover members (check with moving window)
* +2 for each worship set that has two leads
* +2 for each worship set that has a secondary vocalist
* +2 for each worship set that has a lead electric guitarist
* +1 for each worship set that that has a second keyboardist
* +1 for each worship set that has a percussionist
* +1 for each worship member that serves in their secondary role at least once per term and no more than 50% of their Sundays

3. Output top 3 schedules (+ supporting metrics) for human evaluation


## Future Features
* Integrate into web service for more automation (pull directly from mongo)
* Less bruteforcey algorithm to reduce runtime


