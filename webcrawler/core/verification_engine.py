from npi_verifier.name_cleaner import clean_names
from crawler.crawler import crawl_web
from crawler.parser import parse_crawled_data
from npi_verifier.npi_lookup import verify_npi
from npi_verifier.npi_compare import compare_with_npi

def extract_names(raw_name):
    name = clean_names(raw_name)
    parts = name.split()

    if len(parts) == 1:
        return parts[0], ""

    first = parts[0]
    last = parts[-1]
    return first, last


def verify_person(name, npi=None):

    first, last = extract_names(name)

    # default values
    npi_verification = {"status": "NO NPI", "score": 0, "report": []}

    if npi:
        npi_info = verify_npi(npi)
        if npi_info["valid"]:
            user_details = {
                "first_name": first,
                "last_name": last
            }
            npi_verification = compare_with_npi(npi_info, user_details)

    # ------ WEB CRAWLING ------
    raw_pages = crawl_web(name)
    parsed = parse_crawled_data(raw_pages, name)
    web_score = sum(item["score"] for item in parsed)

    # ------ FINAL SCORE ------
    final_score = npi_verification["score"] + web_score

    status = (
        "VERIFIED" if final_score >= 80 else
        "PARTIAL MATCH" if final_score >= 40 else
        "FAILED"
    )

    return {
        "input_name": name,
        "npi": npi,
        "npi_verification": npi_verification,
        "web_results": parsed,      # <- FIXED
        "web_score": web_score,     # <- FIXED
        "final_score": final_score, # <- FIXED
        "status": status            # <- FIXED
    }
