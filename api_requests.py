import requests
import math

from keys import COS_API_TOKEN, COS_USER_ID, COS_BASE_URL, COS_API_TOKEN_BAD, COS_BASE_URL_BAD

def get_jobs(form):
    """form is WTForm form object, convet_to_dict is True (return dict) or False (return json)"""

    keyword = form['keyword']
    location = form['location']
    radius = form['radius']
    days = form['days']
    companyName = form['companyName']
    startRecord = form['startRecord']
    if form['remote']:
        keyword = keyword + " remote"
    if not location:
        location = "US"
    if not radius:
        radius = 50
    if not days:
        days = 0

    try:
        resp = requests.get(
            f'{COS_BASE_URL}/{COS_USER_ID}/{keyword}/{location}/{radius}/0/0/{startRecord}/10/{days}',
            params={"companyName": companyName, "locationFilter": None, "source": "NLx", "showFilters": True},
            headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
        )
    except:
        return {'Message': 'COS API did not respond', 'ErrorCode': 600}
        
    return resp.json()

def get_postings_for_dashboard(hunt):
    """get job postings for dashboard based on hunt"""

    if hunt.o_net_code:
        keyword = hunt.o_net_code
    else:
        keyword = hunt.job_title_desired
    location = hunt.location
    radius = hunt.radius
    days_old = 1

    resp = requests.get(
        f'{COS_BASE_URL}/{COS_USER_ID}/{keyword}/{location}/{radius}/0/0/0/10/{days_old}',
        params={"locationFilter": None, "source": "NLx", "showFilters": True},
        headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
    )

    return resp.json()

def get_page_navigation_values(form):
    next_page_record = int(form.startRecord.data) + 10
    last_page_record = int(form.startRecord.data) - 10
    if last_page_record < 0:
        last_page_record = 0
    page_number = math.ceil(next_page_record / 10)
    return {'next_page_record': next_page_record, 'last_page_record': last_page_record, 'page_number': page_number}


def get_job_details(cos_id):
    """job_id is COS job id"""
    
    resp = requests.get(
        f'{COS_BASE_URL}/{COS_USER_ID}/{cos_id}',
        headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
    )

    return resp.json()