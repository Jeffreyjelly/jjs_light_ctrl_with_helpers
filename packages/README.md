## config_jj_light_helper.yaml :
- Contains the helpers needed for this automation that aren't specific to each room instantiation.
- At the bottom there is yaml code for a dashboard card that has two example "roomexample1" and "roomexample2" and other light configurations

## roomexample_jj_light_helper.yaml :
- base code for all helpers needed for one room initialization to get the automation going.
- (needs the words "roomexample" to be renamed with the room you're trying to automate as well as the filename)
- Has an example of the yaml code for the automation call to this blueprint
  - needs the binary_sensor replaced for the detected and not detected.
- Followed by yaml for a dashboard card if you didn't use the card from config_jj_light_helper.yaml then you can use the card yaml
