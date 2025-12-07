import requests

def verify_npi(npi_number):
    url = f"https://npiregistry.cms.hhs.gov/api/?number={npi_number}&version=2.1"
    response = requests.get(url)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return {"valid": False}

    info = data["results"][0]

    return {
        "valid": True,
        "name": info["basic"].get("name"),
        "first_name": info["basic"].get("first_name"),
        "last_name": info["basic"].get("last_name"),
        "gender": info["basic"].get("gender"),
        "enumeration_date": info["basic"].get("enumeration_date"),
        "last_updated": info["basic"].get("last_updated"),
        "addresses": info.get("addresses", []),
        "taxonomy": info.get("taxonomies", [])
    }
