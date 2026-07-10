"""
aqi_calculator.py

Implements the Indian CPCB National AQI sub-index formula for PM2.5 and PM10
and converts the final AQI number into a category + health recommendation.
Reference breakpoints: CPCB National Air Quality Index (2014).
"""

# (BP_lo, BP_hi, I_lo, I_hi)
PM25_BREAKPOINTS = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 500, 401, 500),
]

PM10_BREAKPOINTS = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 600, 401, 500),
]

CATEGORIES = [
    (0, 50, "Good", "#4CAF50",
     "Air quality is satisfactory and poses little or no risk."),
    (51, 100, "Satisfactory", "#8BC34A",
     "Air quality is acceptable; minor breathing discomfort to sensitive people."),
    (101, 200, "Moderate", "#FFC107",
     "Air quality is acceptable. However, for some pollutants there may be a "
     "moderate health concern for a very small number of people."),
    (201, 300, "Poor", "#FF9800",
     "May cause breathing discomfort to people with lung disease, children, and older adults."),
    (301, 400, "Very Poor", "#8E24AA",
     "May cause respiratory illness on prolonged exposure. Avoid outdoor activity."),
    (401, 500, "Severe", "#7B1E1E",
     "Affects healthy people and seriously impacts those with existing diseases. "
     "Avoid all outdoor exertion."),
]


def _sub_index(value, breakpoints):
    value = max(0, value)
    for bp_lo, bp_hi, i_lo, i_hi in breakpoints:
        if bp_lo <= value <= bp_hi:
            return ((i_hi - i_lo) / (bp_hi - bp_lo)) * (value - bp_lo) + i_lo
    # above table range -> clamp to top band, scale linearly past it
    bp_lo, bp_hi, i_lo, i_hi = breakpoints[-1]
    if value > bp_hi:
        return i_hi + (value - bp_hi)
    return i_lo


def compute_aqi(pm25: float, pm10: float) -> float:
    """National AQI = max of the individual pollutant sub-indices."""
    i_pm25 = _sub_index(pm25, PM25_BREAKPOINTS)
    i_pm10 = _sub_index(pm10, PM10_BREAKPOINTS)
    return round(max(i_pm25, i_pm10), 1)


def classify_aqi(aqi: float):
    """Returns (category, color_hex, health_recommendation)."""
    for lo, hi, category, color, advice in CATEGORIES:
        if lo <= aqi <= hi:
            return category, color, advice
    lo, hi, category, color, advice = CATEGORIES[-1]
    return category, color, advice


def full_report(pm25: float, pm10: float) -> dict:
    aqi = compute_aqi(pm25, pm10)
    category, color, advice = classify_aqi(aqi)
    return {
        "aqi": aqi,
        "pm25": round(pm25, 1),
        "pm10": round(pm10, 1),
        "category": category,
        "color": color,
        "health_recommendation": advice,
    }
