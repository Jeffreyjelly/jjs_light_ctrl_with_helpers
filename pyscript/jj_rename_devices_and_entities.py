# Once pyscript is installed > Developer Tools > Actions > choose jj_rename_devices_and_entities

# action: pyscript.jj_rename_devices_and_entities
# data:
#   device_and_entity_match: "0x5cc7c1fffe890f57"
#   replace_text: "0x5cc7c1fffe890f57"
#   with_text: btn2_ikea_2025_n03
#   device_name_all_underscores: true
#   device_remove_with_text_underscores: true
#   swap: true
#   verbose: false


from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
from homeassistant.components.persistent_notification import create as notify
import re

# Case-insensitive replacement
def replace_ci(text: str, old: str, new: str) -> str:
    """
    Replace all occurrences of 'old' in 'text' with 'new', ignoring case.
    """
    pattern = re.compile(re.escape(old), re.IGNORECASE)
    return pattern.sub(new, text)

@service
def jj_rename_devices_and_entities(
    device_and_entity_match: str,
    replace_text: str,
    with_text: str,
    device_name_all_underscores: bool = True, #converts the device name "_" to " "
    device_remove_with_text_underscores: bool = True, #if you want to remove the spaces from the "with_text"
    swap: bool = True,
    verbose: bool = False
):
    """
    Rename entities by replacing part of their entity_id.
    """
    try:
        def verbose_notify(message: str, title: str):
            if verbose:
                notify(hass, message, title)
        def always_notify(message: str, title: str):
            notify(hass, message, title)

        # ---- Input validation: type and non-empty strings ----
        for name, value in [("device_and_entity_match", device_and_entity_match),
                            ("replace_text", replace_text),
                            ("with_text", with_text)]:
            if not isinstance(value, str):
                always_notify(f"Error: {name} must be a string", "Input Error")
                return
            if not value.strip():  # catches empty or whitespace-only strings
                always_notify(f"Error: {name} cannot be empty", "Input Error")
                return

        verbose_notify("beginning function...", "Step 0: Start")
        ent_reg = er.async_get(hass)
        dev_reg = dr.async_get(hass)
        renamed_entities = []
        renamed_devices = []
        renamed_device_ids = set()
        scanned_entity_count = 0
        scanned_device_count = 0
        replace_text_with_spaces =  replace_text.replace("_", " ")
        device_and_entity_match_with_spaces = device_and_entity_match.replace("_", " ")

        verbose_notify(
            f"Starting scan for entities... '{device_and_entity_match}' \n\nand to replace:'{replace_text}' \n\n with: {with_text}",
            "Step 1: Start")

        try:
            for entity_id, entry in list(ent_reg.entities.items()):
                scanned_entity_count += 1 #count every time we check
                if device_and_entity_match.lower() in entity_id.lower() or (
                    entry.name and device_and_entity_match.lower() in entry.name.lower()
                ):
                    if swap:
                        new_entity_id = replace_ci(entity_id, replace_text, with_text)

                        verbose_notify(
                            f"Matched entity: {entity_id}\n\n (friendly name: {entry.name})\n\n New Entity Planned: {new_entity_id}",
                            "Step 2: Replace Entity")
                        # Safety check: make sure new ID doesn’t already exist
                        if ent_reg.async_get_entity_id(entry.domain, entry.platform, new_entity_id):
                            always_notify(f"Skipping {entity_id} → {new_entity_id} (already exists)", "Conflict")
                            continue

                        ent_reg.async_update_entity(entity_id, new_entity_id=new_entity_id)
                        renamed_entities.append(f"{entity_id} → {new_entity_id}")
        except Exception as e:
            always_notify(f"Error processing for loop on entities: {e}", "Error")


        verbose_notify(
            f"Starting scan for devices... '{device_and_entity_match_with_spaces}' or '{device_and_entity_match}' \n\nand to replace:'{replace_text}' or '{replace_text_with_spaces}'\n\n with: {with_text}",
            "Step 3: Device rename")

        try:
            for device_id, device in list(dev_reg.devices.items()):
                if not device.name:
                    continue
                scanned_device_count += 1
                if device_and_entity_match.lower() in device.name.lower() or \
                    device_and_entity_match_with_spaces.lower() in device.name.lower():
                        # Rename the associated device if it hasn't been renamed yet
                        if device_id not in renamed_device_ids:
                            current_name = device.name

                            #switch all the _ to spaces
                            desired_name = current_name.replace("_", " ")
                            #change the match to the with_text
                            desired_name = replace_ci(desired_name, replace_text_with_spaces, with_text)
                            # Determine the desired device name based on the flag
                            if device_name_all_underscores:
                                desired_name = desired_name.replace(" ", "_") #put it back to all _
                            elif device_remove_with_text_underscores:
                                desired_name = desired_name.replace("_", " ") #remove the rest of the _
                            
                            verbose_notify(
                                f"Matched device: {current_name}\n\n New Device Planned: {desired_name}",
                                "Step 4: Replace Device")
                            # Only rename if the name actually changes
                            if desired_name != current_name:
                                dev_reg.async_update_device(device_id, name=desired_name)
                                renamed_devices.append(f"{current_name} → {desired_name}")
                                renamed_device_ids.add(device_id)
                            else:
                                always_notify(f"Skipping {current_name} → {desired_name} (already exists)", "Error Device Name")
        except Exception as e:
            always_notify(f"Error processing for loop on devices: {e}", "Error")

        verbose_notify("Ending scan and rename for devices and entities...", "Step End: Finished loop")

        # After loop finishes
        summary = [
            f"Scanned {scanned_entity_count} entities in total.",
            f"Renamed {len(renamed_entities)} entities." if renamed_entities else "No entities were renamed.",
            f"\nScanned {scanned_device_count} devices in total.",
            f"Renamed {len(renamed_devices)} devices." if renamed_devices else "No devices were renamed."
        ]
        if renamed_entities:
            summary.append("\nEntity Changes:\n" + "\n".join(renamed_entities))
        if renamed_devices:
            summary.append("\nDevice changes:\n" + "\n".join(renamed_devices))

        always_notify("\n".join(summary), title="Entity & Device Rename Summary")
    except Exception as e:
        always_notify(f"Error in jj_rename_devices_and_entities: {e}", "Error")
