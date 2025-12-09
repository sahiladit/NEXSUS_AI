def compare_with_npi(npi_info, user_details):
    """
    npi_info = result of verify_npi()
    user_details = {"first_name": "", "last_name": ""}
    """

    score = 0
    report = []

    # safe extract
    basic = {
        "first_name": (npi_info.get("first_name") or "").lower(),
        "last_name": (npi_info.get("last_name") or "").lower(),
        "gender": (npi_info.get("gender") or "").lower()
    }

    addresses = npi_info.get("addresses", [])
    taxonomies = npi_info.get("taxonomy", [])

    # --- NAME MATCH ---
    if user_details["first_name"].lower() == basic["first_name"]:
        score += 30
    else:
        report.append("First name mismatch")

    if user_details["last_name"].lower() == basic["last_name"]:
        score += 30
    else:
        report.append("Last name mismatch")

    # --- ADDRESS MATCH ---
    if addresses:
        practice_addr = addresses[0]  # primary address
        npi_city = (practice_addr.get("city") or "").lower()
        npi_state = (practice_addr.get("state") or "").lower()

        input_city = (user_details.get("city") or "").lower()
        input_state = (user_details.get("state") or "").lower()

        if input_city and input_city == npi_city:
            score += 10
        elif input_city:
            report.append("City mismatch")

        if input_state and input_state == npi_state:
            score += 10
        elif input_state:
            report.append("State mismatch")

    # --- TAXONOMY MATCH ---
    if taxonomies:
        taxonomy_desc = (taxonomies[0].get("desc") or "").lower()
        if user_details.get("taxonomy"):
            if user_details["taxonomy"].lower() in taxonomy_desc:
                score += 20
            else:
                report.append("Specialty mismatch")

    status = "VERIFIED" if score >= 60 else "PARTIAL MATCH" if score >= 30 else "FAILED"

    return {
        "status": status,
        "score": score,
        "report": report
    }
