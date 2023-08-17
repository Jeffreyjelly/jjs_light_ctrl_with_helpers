# jjs_light_ctrl_with_helpers
Home Assistant Blueprint for controlling the lights with a daytime and nighttime scenes via timer helpers and more

## Helpers, scenes, light groups, and more you'll need with suggested names

### input_boolean [ 1 ]:
 - helper_`{name_of_area}`_auto_enable

### light or light Group [ 1 ]:
 - group_`{name_of_area}`_all

### binary_sensor [ 2 ]:
 - motion detection
   - > (PIR sensor or any other means)
 - motion not detection
   - > (PIR sensor, mmwave or any other means)

