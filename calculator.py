import requests


def apply_teen_multiplier(base_rate: float, age: int) -> float:
    """
    Apply a teen driver multiplier to the base rate. In Georgia, teens typically
    pay 1.5x to 2.5x the base rate. We'll use a sliding scale.
    """
    if age < 16:
        raise ValueError("Age must be at least 16 for driving")
    if 16 <= age <= 17:
        return base_rate * 2.5
    if 18 <= age <= 19:
        return base_rate * 1.5
    return base_rate


def decode_vin(vin: str) -> dict:
    """Use NHTSA vPIC API to decode a VIN (no API key required)."""
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("Results", [{}])[0]


def has_safety_features(vin_info: dict) -> bool:
    """Check for electronic stability control or advanced airbags in the decoded VIN info."""
    # field names from vPIC: 'StabilityControl' may contain 'Yes' or 'No'
    esc = vin_info.get("StabilityControl")
    # airbags might be indicated via multiple airbag fields; treat presence of 'Dual' or 'Front' etc.
    airbags = vin_info.get("AirBagLocFront") or vin_info.get("AirBagLocSide")
    esc_ok = isinstance(esc, str) and esc.lower().startswith("y")
    airbags_ok = isinstance(airbags, str) and airbags.strip() != ""
    return esc_ok or airbags_ok


def calculate_premium(base_rate: float, age: int, vin: str) -> float:
    """Compute an estimated annual premium applying teen multiplier and safety discount."""
    rate = apply_teen_multiplier(base_rate, age)
    vin_info = decode_vin(vin)
    if has_safety_features(vin_info):
        rate *= 0.95  # 5% safety discount
    return rate


if __name__ == "__main__":
    # simple CLI for testing
    import argparse
    parser = argparse.ArgumentParser(description="Estimate a premium with teen multiplier and safety discount.")
    parser.add_argument("--base", type=float, required=True, help="Base annual rate")
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--vin", required=True)
    args = parser.parse_args()

    annual = calculate_premium(args.base, args.age, args.vin)
    monthly = annual / 12.0
    print(f"Estimated annual premium: ${annual:.2f}")
    print(f"Estimated monthly premium: ${monthly:.2f}")
    print("Note: VIN is used transiently and not stored; see privacy policy.")
