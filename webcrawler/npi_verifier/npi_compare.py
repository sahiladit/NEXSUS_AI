def compare_with_npi(user_details, npi_info):
    """
    user_details = {
        "first_name": "",
        "last_name": "",
        "gender": "",
        "city": "",
        "state": "",
        "taxonomy": ""
    }

    npi_info = output from verify_npi()
    """

    score = 0
    mismatches = []
    matches = []

    # -------- NAME MATCH --------
    if user_details.get("first_name"):
        if user_details["first_name"].lower() == npi_info["first_name"].lower():
            score += 20
            matches.append("First name matches")
        else:
            mismatches.append("First name mismatch")

    if user_details.get("last_name"):
        if user_details["last_name"].lower() == npi_info["last_name"].lower():
            score += 20
            matches.append("Last name matches")
        else:
            mismatches.append("Last name mismatch")

    # -------- GENDER MATCH --------
    if user_details.get("gender"):
        if user_details["gender"].lower() == str(npi_info["gender"]).lower():
            score += 10
            matches.append("Gender matches")
        else:
            mismatches.append("Gender mismatch")

    # -------- ADDRESS MATCH --------
    if npi_info["addresses"]:
        addr = npi_info["addresses"][0]  # primary practice address

        if user_details.get("city"):
            if user_details["city"].lower() == addr.get("city", "").lower():
                score += 10
                matches.append("City matches")
            else:
                mismatches.append("City mismatch")

        if user_details.get("state"):
            if user_details["state"].lower() == addr.get("state", "").lower():
                score += 10
                matches.append("State matches")
            else:
                mismatches.append("State mismatch")

    # -------- TAXONOMY MATCH --------
    if user_details.get("taxonomy") and npi_info["taxonomy"]:
        taxonomy_desc = npi_info["taxonomy"][0].get("desc", "").lower()

        if user_details["taxonomy"].lower() in taxonomy_desc:
            score += 20
            matches.append("Specialty matches")
        else:
            mismatches.append("Specialty mismatch")

    # -------- FINAL VERDICT --------
    if score >= 60:
        status = "VERIFIED"
    elif score >= 30:
        status = "PARTIAL MATCH"
    else:
        status = "FAILED VERIFICATION"

    return {
        "status": status,
        "score": score,
        "matches": matches,
        "mismatches": mismatches,
        "npi_data": npi_info
    }
