CONVERSION_FACTORS = {
    "Length": {
        "units": {
            "Meter (m)": 1.0,
            "Kilometer (km)": 1000.0,
            "Centimeter (cm)": 0.01,
            "Millimeter (mm)": 0.001,
            "Mile (mi)": 1609.34,
            "Yard (yd)": 0.9144,
            "Foot (ft)": 0.3048,
            "Inch (in)": 0.0254,
            "Nautical Mile (NM)": 1852.0,
        },
        "base_unit": "Meter (m)",
        "icon": "📏"
    },
    "Weight/Mass": {
        "units": {
            "Kilogram (kg)": 1.0,
            "Gram (g)": 0.001,
            "Milligram (mg)": 0.000001,
            "Metric Ton (t)": 1000.0,
            "Pound (lb)": 0.453592,
            "Ounce (oz)": 0.0283495,
            "Stone (st)": 6.35029, # Added Stone
        },
        "base_unit": "Kilogram (kg)",
        "icon": "⚖️"
    },
    "Temperature": {
        "units": {
            "Celsius (°C)": "C",
            "Fahrenheit (°F)": "F",
            "Kelvin (K)": "K",
        },
        "base_unit": None, # Handled differently
        "icon": "🌡️"
    },
    "Volume": {
        "units": {
            "Liter (L)": 1.0,
            "Milliliter (mL)": 0.001,
            "Cubic Meter (m³)": 1000.0,
            "Cubic Centimeter (cm³)": 0.001,
            "US Gallon (gal)": 3.78541,
            "US Quart (qt)": 0.946353,
            "US Pint (pt)": 0.473176,
            "US Cup (cup)": 0.236588,
            "US Fluid Ounce (fl oz)": 0.0295735,
            "Imperial Gallon (imp gal)": 4.54609, # Added Imperial
            "Imperial Pint (imp pt)": 0.568261,  # Added Imperial
        },
        "base_unit": "Liter (L)",
        "icon": "💧"
    },
    "Area": {
        "units": {
            "Square Meter (m²)": 1.0,
            "Square Kilometer (km²)": 1_000_000.0,
            "Hectare (ha)": 10_000.0,
            "Acre (ac)": 4046.86,
            "Square Mile (mi²)": 2_589_988.11,
            "Square Foot (ft²)": 0.092903,
            "Square Inch (in²)": 0.00064516,
        },
        "base_unit": "Square Meter (m²)",
        "icon": "🖼️"
    },
    "Speed": {
        "units": {
            "Meters per second (m/s)": 1.0,
            "Kilometers per hour (km/h)": 1/3.6, # 1 m/s = 3.6 km/h
            "Miles per hour (mph)": 1/2.23694, # 1 m/s = 2.23694 mph
            "Knots (kn)": 1/1.94384,       # 1 m/s = 1.94384 knots
            "Feet per second (ft/s)": 1/0.3048, # 1 m/s = 1/0.3048 ft/s
        },
        "base_unit": "Meters per second (m/s)",
        "icon": "💨"
    },
    "Data Storage": {
        # Using IEC prefixes (powers of 1024) for KiB, MiB etc.
        # And SI prefixes (powers of 1000) for KB, MB etc.
        "units": {
            "Byte (B)": 1.0,
            "Kilobyte (KB) [10³ B]": 10**3,
            "Megabyte (MB) [10⁶ B]": 10**6,
            "Gigabyte (GB) [10⁹ B]": 10**9,
            "Terabyte (TB) [10¹² B]": 10**12,
            "Kibibyte (KiB) [2¹⁰ B]": 2**10,
            "Mebibyte (MiB) [2²⁰ B]": 2**20,
            "Gibibyte (GiB) [2³⁰ B]": 2**30,
            "Tebibyte (TiB) [2⁴⁰ B]": 2**40,
            "Bit (b)": 0.125, # 1 Byte = 8 Bits
        },
        "base_unit": "Byte (B)",
        "icon": "💾"
    }
}