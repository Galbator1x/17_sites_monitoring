import requests
import pythonwhois
import os
import argparse
from datetime import datetime, timedelta
from urllib.parse import urlparse


SERVER_WORKS = 0
DOMAIN_IS_PAID = 1
SITE_URL = 2


def get_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='path to the list of urls')
    args = parser.parse_args()
    return args.filepath


def load_urls_for_check(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath) as file_handler:
        return file_handler.read().splitlines()


def is_server_respond_with_200(url):
    if requests.head(url).status_code == 200:
        return 'Yes'
    return 'No'


def get_domain_from_url(url):
    return urlparse(url).netloc


def get_domain_expiration_date(domain_name):
    exp_date = pythonwhois.get_whois(domain_name).get('expiration_date', None)
    return exp_date[0] if exp_date is not None else None


def is_domain_paid_for_month_ahead(expiration_date):
    if expiration_date is None:
        return 'No data'
    domain_is_paid = datetime.now() <= expiration_date - timedelta(days=30)
    return 'Yes' if domain_is_paid else 'No'


def get_list_of_sites_health(urls_list):
    sites_health = []
    for url in urls_list:
        server_works = 'Yes' if is_server_respond_with_200(url) else 'No'
        exp_date = get_domain_expiration_date(get_domain_from_url(url))
        domain_paid = is_domain_paid_for_month_ahead(exp_date)
        sites_health.append([server_works, domain_paid, url])
    return sites_health


def output_sites_health_to_console(sites_health):
    for site in sites_health:
        print('server works: {}, domain is paid for a month ahead: {}  {}'.
              format(site[SERVER_WORKS], site[DOMAIN_IS_PAID], site[SITE_URL]))


if __name__ == '__main__':
    filepath = get_filepath()
    urls = load_urls_for_check(filepath)
    if urls is None:
        print('File does not exists.')
        exit()

    try:
        output_sites_health_to_console(get_list_of_sites_health(urls))
    except (ConnectionResetError, ConnectionError):
        print('Failed to connect, try later.')
