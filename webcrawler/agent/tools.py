# agent/tools.py
from core.verification_engine import verify_person
from npi_verifier.npi_lookup import verify_npi
from crawler.crawler import crawl_web

def run_verify_person(name: str, npi: str = None):
    return verify_person(name, npi)

def run_npi_lookup(npi: str):
    return verify_npi(npi)

def run_crawl(name: str, max_pages: int = 5):
    return crawl_web(name, max_pages=max_pages)
