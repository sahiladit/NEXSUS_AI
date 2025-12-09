from npi_verifier.name_cleaner import clean_names
from npi_verifier.npi_lookup import verify_npi
from npi_verifier.npi_compare import compare_with_npi
from crawler.crawler import crawl_web
from crawler.parser import parse_crawled_data


class NPIVerificationAgent:

    def __init__(self):
        self.person_name = None
        self.npi_number = None

    # -----------------------------
    # STEP 1: Prepare & clean name
    # -----------------------------
    def clean_name(self, raw_name):
        cleaned = clean_names(raw_name)
        parts = cleaned.split()

        if len(parts) == 1:
            return parts[0], ""

        return parts[0], parts[-1]  # first, last

    # -----------------------------
    # STEP 2: Fetch NPI data
    # -----------------------------
    def fetch_npi(self, npi):
        return verify_npi(npi)

    # -----------------------------
    # STEP 3: Compare input name vs NPI registry
    # -----------------------------
    def compare_with_npi(self, npi_info, first, last):
        user_details = {
            "first_name": first,
            "last_name": last
        }
        return compare_with_npi(npi_info, user_details)

    # -----------------------------
    # STEP 4: Perform web crawling
    # -----------------------------
    def web_lookup(self, raw_name):
        pages = crawl_web(raw_name)
        parsed = parse_crawled_data(pages, raw_name)
        return parsed

    # -----------------------------
    # STEP 5: Final decision logic
    # -----------------------------
    def compute_final_score(self, npi_score, web_score):
        total_score = npi_score + web_score

        if total_score >= 80:
            status = "VERIFIED"
        elif total_score >= 40:
            status = "PARTIAL MATCH"
        else:
            status = "FAILED"

        return status, total_score

    # -----------------------------
    # AGENT MAIN WORKFLOW
    # -----------------------------
    def run(self, raw_name, npi_number):

        self.person_name = raw_name
        self.npi_number = npi_number

        # Clean name
        first, last = self.clean_name(raw_name)

        # Fetch NPI data
        npi_info = verify_npi(npi_number)

        if not npi_info["valid"]:
            return {
                "status": "INVALID NPI",
                "npi_score": 0,
                "web_score": 0,
                "final_score": 0
            }

        # Compare input vs NPI registry
        npi_result = self.compare_with_npi(npi_info, first, last)
        npi_score = npi_result["score"]

        # Web crawling verification
        web_data = self.web_lookup(raw_name)
        web_score = sum(item["score"] for item in web_data)

        # Final scoring
        final_status, final_score = self.compute_final_score(npi_score, web_score)

        return {
            "input_name": raw_name,
            "npi": npi_number,
            "npi_verification": npi_result,
            "web_results": web_data,
            "web_score": web_score,
            "final_score": final_score,
            "status": final_status
        }
