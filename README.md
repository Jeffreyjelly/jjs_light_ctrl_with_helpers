# jjs_light_ctrl_with_helpers
Home Assistant Blueprint for controlling the lights with a daytime and nighttime scenes via timer helpers and more

The only piece you need to provide is a light group and a binary sensor for motion! (packages used to instantiate helpers per the room you want to set this up for)

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
 - timer_`{name_of_area}`_motion_to_dim
   - > (keep at default 0 as the automation uses this as a control from no motion to dim)
 - timer_`{name_of_area}`_dim_to_off
   - > (keep at default 0 as the automation uses this as a control from dim to off)

### input_numbers [ 8 ]:
 - in_num_dim_amt
   - > (0 to 255 value that your lights are dimmed by before turn off, or otherwise current brightness-in_num_dim_amt. If the current brightness is below this value, the value will be set to 1 instead of 0 during the dim period)
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
 - in_num_`{name_of_area}`_hold_scene
   - > (1 to 7200) time in seconds for automation to hold onto the temporary scene

### input_daytime [ 2 ]:
 - in_datetime_day
   - > (Whenever you want the lights to start to use the day scene)
 - in_datetime_night
   - > (Whenever you want the lights to start to use the night scene)

### input_select [ 2 ]:
 - in_select_light_control_card
   - > (List of settings and rooms to control the card that is in the package for config_jj_light_helper.yaml)
 - in_select_light_settings_card
   - > (When under a room for the card yaml example this controls what the room is displaying for configuration, light, settings for day, or night)

### scenes [ 2 ]:
 - scene_`{name_of_area}`_daytime
   - > (day scene that should be controlling the lights listed for your lights chosen above)
 - scene_`{name_of_area}`_nighttime
   - > (night scene that should be controlling the lights listed for your lights chosen above)


## Ideas to add / Things to test
 - boolean to not save last on state for others to use this with other automations
 - ~~another input_number for controlling the length of time it preserves the temporary scene instead of just copying the `in_num_{name_of_area}_dim_light_{day}_dly`.~~ - done
 - adding code for packages for people to make the helpers easier
   - Also to add a snipped of the automation instantiation with all the helpers filled in to make this super easy to add new rooms.  
 - ~~adding a card for the dashboards~~ -done
   - ~~add a section to the card for the timers to show when last ran etc.~~ - just did a tile for the timer if active for now
   - ~~This will be a package that you have to rename to add each room you'd want to add as a condition.~~ adding a package for the individual rooms or all together.
 - add the ability to add a list of other blueprint timers you'd reset
   - can you reference the timer used underneath a blueprint?
   - for instance if your office is in the second half of your living room you dont want the living room to turn off
 - ability to change the day and night scenes used from a drop down list or something.
 - ~~choice from user to reset the timers if lights were manually changed (off should still just always kill the timers though for problem seen below)~~ Set the automation to cancel the two timers if manually turned off.
 - Need to verilfy using other sensors for turn on/turn off like door and window binary sensors.

## Known problems
 - ~~when dimming the lights and they fall below 0 I set the group to turn on at 1% and it turns on unwanted lights against the nightlight scene~~
   - ~~need to calculate the dim percent and just set it to 1 instead of checking if the lights turned off after dimming~~ - done
   - have a problem with this still for lights that are on switches get turned on when they were set to be off for certain scenes. Need to ask forums on ideas for this.
 - ~~When the lights are turned off manually and the timer for `motion to dim` is still active the lights wont turn back on.~~
 - still seems to be problem when the lights are getting stuck at the dim value but I haven't figured out what path is causing it yet.

## Revision history
 - 1.1 - 2023_11_06
   - added input_number for the time the automation holds onto the temporary scene so your lights stay to the old value for however long you want to specifiy.
   - added a package for a room to be added easily
   - adding the main config_jj_light_helper.yaml package also for all the other standalone helpers
