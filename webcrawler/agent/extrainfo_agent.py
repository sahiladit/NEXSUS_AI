from rapidfuzz import fuzz

def run_extrainfo(name: str, extra_info: dict, web_results: list):
    score = 0
    report = []

    combined_text = " ".join(
        item.get("snippet", "") for item in web_results
    ).lower()

    for key, value in extra_info.items():
        if not value:
            continue

        value = value.lower()
        similarity = fuzz.partial_ratio(value, combined_text)

        if similarity >= 50:
            score += 15
        else:
            report.append(f"{key} not confidently found (score={similarity})")

    status = (
        "VERIFIED" if score >= 30 else
        "PARTIAL MATCH" if score >= 20 else
        "FAILED"
    )
    return {
        "status": status,
        "score": score,
        "report": report
    }
