from homeassistant.helpers import entity_registry as er, area_registry as ar
from homeassistant.components.persistent_notification import create as notify

@service
def assign_entities_to_area(
    target_area_name: str = "master bedroom",
    entity_match: str = "masterbedroom",
    move_entities_from_area_name: str = None,
    verbose: bool = False
):
    """
    Assign entities to a target area.
    Can either move entities from a specific area or assign unassigned ones.
    Verbose mode enables detailed notifications.
    """
    def verbose_notify(message: str, title: str):
        if verbose:
            notify(hass, message, title)

    # Step 1: Starting
    action_type = "moving" if move_entities_from_area_name else "assigning"
    verbose_notify(
        f"Starting {action_type} entities with '{entity_match}'...",
        "Step 1: Start"
    )

    # Step 2: Get registries
    ent_reg = er.async_get(hass)
    area_reg = ar.async_get(hass)
    verbose_notify(
        "Entity and area registries loaded",
        "Step 2: Registries Loaded"
    )

    # Step 3: Find target area ID
    target_area = area_reg.async_get_area_by_name(target_area_name)
    if target_area is None:
        notify(
            hass,
            f"Target area '{target_area_name}' not found!",
            "Step 3: Area Not Found"
        )
        return
    verbose_notify(
        f"Target area: {target_area.name}",
        "Step 3: Area Found"
    )

    # Step 4: Collect matching entities
    matching_entities = []
    source_area_id = None

    if move_entities_from_area_name:
        source_area = area_reg.async_get_area_by_name(move_entities_from_area_name)
        if source_area is None:
            notify(
                hass,
                f"Source area '{move_entities_from_area_name}' not found!",
                "Step 4: Source Area Not Found"
            )
            return
        source_area_id = source_area.id
        verbose_notify(
            f"Source area: {source_area.name}",
            "Step 4: Source Area Found"
        )

    for entity_id, entry in ent_reg.entities.items():
        is_match = entity_match.lower() in entity_id.lower()

        if is_match:
            if move_entities_from_area_name:
                if entry.area_id == source_area_id:
                    matching_entities.append(entity_id)
            else:
                if entry.area_id is None:
                    matching_entities.append(entity_id)

    if not matching_entities:
        notify(
            hass,
            f"No entities matched '{entity_match}' in the specified criteria.",
            "Step 4: No Matches"
        )
        return

    verbose_notify(
        "Found the following entities:\n" + "\n".join(matching_entities),
        "Step 4: Entities Found"
    )

    # Step 5: Assign/move them to the target area
    for entity_id in matching_entities:
        ent_reg.async_update_entity(entity_id, area_id=target_area.id)

    notify(
        hass,
        f"{action_type.capitalize()} {len(matching_entities)} entities to area: {target_area_name}\n" + "\n".join(matching_entities),
        "Step 5: Assignment Complete"
    )