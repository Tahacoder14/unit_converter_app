def convert_standard(value, from_unit, to_unit, category_data):
    """Handles non-temperature conversions."""
    if not value: # Handle case where input might be None or 0 before fully typed
        return 0.0
    if from_unit == to_unit:
        return float(value)

    units_map = category_data["units"]

    try:
        value_in_base = float(value) * units_map[from_unit]
        converted_value = value_in_base / units_map[to_unit]
        return converted_value
    except (ZeroDivisionError, TypeError, KeyError):
        # Handle potential errors gracefully, though with predefined factors unlikely
        return None # Or raise a custom error

def convert_temperature(value, from_unit_symbol, to_unit_symbol):
    """Handles temperature conversions."""
    if not value:
        return 0.0
    value = float(value)
    if from_unit_symbol == to_unit_symbol:
        return value

    # Convert to Celsius first
    if from_unit_symbol == "F":
        celsius = (value - 32) * 5/9
    elif from_unit_symbol == "K":
        celsius = value - 273.15
    else: # Already Celsius
        celsius = value

    # Convert from Celsius to target unit
    if to_unit_symbol == "F":
        return (celsius * 9/5) + 32
    elif to_unit_symbol == "K":
        return celsius + 273.15
    else: # Target is Celsius
        return celsius