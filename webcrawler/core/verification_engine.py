from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
from crawler.crawler import crawl_web
from crawler.parser import parse_crawled_data
from npi_verifier.npi_lookup import verify_npi
from npi_verifier.npi_compare import compare_with_npi


def verify_person(name, npi=None):

    final = {
        "input_name": name,
        "npi_status": None,
        "web_data": [],
        "match_confidence": 0
    }

    if npi:
        npi_info = verify_npi(npi)

        if npi_info["valid"]:
            npi_verification = compare_with_npi(DEFAULT_MAX_INCLUSION_DEPTH, npi_info)
            final["npi_verification"] = npi_verification
            final["final_score"] += npi_verification["score"]
        else:
            final["npi_verification"] = {"status": "INVALID NPI", "score": 0}

    raw_pages = crawl_web(name)
    parsed = parse_crawled_data(raw_pages, name)

    final["web_data"] = parsed

    final["match_confidence"] = sum(item["score"] for item in parsed)

    return final
