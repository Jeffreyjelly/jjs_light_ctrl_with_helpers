# jjs_light_ctrl_with_helpers
Home Assistant Blueprint for controlling the lights with a daytime and nighttime scenes via timer helpers and more

## Features:
- Two light scenes, one for day and night
- Wont override the current light state if manually changed
- Dims to show the lights are about to turn off
- Time period after lights are off and motion is active to recover the last
light state.
- Fully customizable with the helpers
- Controllable via other automations via using the helpers called with the
blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FJeffreyjelly%2Fjjs_light_ctrl_with_helpers%2Fblob%2Fmain%2FJJs_light_ctrl_w_helpers.yaml)

## Helpers, scenes, light groups, and more you'll need with suggested names

### light or light Group [ 1 ]:
 - group_`{name_of_area}`_all
   - > (the light(s) to control)

### input_boolean [ 1 ]:
 - in_bool_`{name_of_area}`_auto_enable
   - > (a boolean for you to disable the automation when needed)

### binary_sensor [ 2 ]:
 - motion detection
   - > (PIR sensor or any other means)
 - motion not detection
   - > (PIR sensor, mmwave or any other means)

### timer [ 2 ]:
 - timer_`{name_of_area}`_on_to_dim
   - > (keep at default 0 as the automation uses this as a control from no motion to dim)
 - timer_`{name_of_area}`_dim_to_off
   - > (keep at default 0 as the automation uses this as a control from dim to off)

### input_numbers [ 7 ]:
 - in_num_perc_dimmed
   - > (-99 to -1 percentage that your lights are dimmed by before turn off, if it hit's 0 it'll turn back on to 1%)
 - in_num_`{name_of_area}`_on_light_day_dly
   - > (20 to 7200 time in seconds from no motion to dim during the day)
 - in_num_`{name_of_area}`_on_light_night_dly
   - > (20 to 7200 time in seconds from no motion to dim during the night)
 - in_num_`{name_of_area}`_dim_light_day_dly
   - > (10 to 1800 time in seconds from dim to off during the day)
 - in_num_`{name_of_area}`_dim_light_night_dly
   - > (10 to 1800 time in seconds from dim to off during the night)
 - in_num_transition_time_norm
   - > (0 to 10)  time in seconds for light to transition from off to on)
 - in_num_transition_time_fast
   - > (0 to 3)  time in seconds for light to transition from dim to on or vice versa)

### input_daytime [ 2 ]:
 - in_datetime_day
   - > (Whenever you want the lights to start to use the day scene)
 - in_datetime_night
   - > (Whenever you want the lights to start to use the night scene)

### scenes [ 2 ]:
 - scene_`{name_of_area}`_daytime
   - > (day scene that should be controlling the lights listed for your lights chosen above)
 - scene_`{name_of_area}`_nighttime
   - > (night scene that should be controlling the lights listed for your lights chosen above)


## Ideas to add
 - boolean to not save last on state for others to use this with other automations
 - another input_number for controlling the length of time it preserves the temporary scene instead of just copying the `in_num_{name_of_area}_dim_light_{day}_dly`.
 - adding code for packages for people to make the helpers easier
 - adding a card for the dashboards
   - add a section to the card for the timers to show when last ran etc.
 - add the ability to add a list of other blueprint timers you'd reset
   - can you reference the timer used underneath a blueprint?
   - for instance if your office is in the second half of your living room you dont want the living room to turn off
 - ability to change the day and night scenes used from a drop down list or something.
 - choice from user to reset the timers if lights were manually changed (off should still just always kill the timers though for problem seen below)

## Known problems
 - when dimming the lights and they fall below 0 I set the group to turn on at 1% and it turns on unwanted lights against the nightlight scene
   - need to calculate the dim percent and just set it to 1 instead of checking if the lights turned off after dimming
 - When the lights are turned off manually and the timer for `motion to dim` is still active the lights wont turn back on.
   - this needs a major fix as that is a rather broken feature that won't fly for me. change the beginning check for the three (two timers and lights on) to just only check light by itself first. If lights were off clear out the dim to off timer and continue normal operation.
   - instead just write a branch trigger that adjusts the timer if the lights are changed not from this automation. (if the lights are manually turned off to cancel and existing timers)
