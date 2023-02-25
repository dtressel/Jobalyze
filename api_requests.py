import requests
import math
from datetime import date, datetime, timedelta, timezone
from models import SavedJob

try:
    from keys import COS_API_TOKEN, COS_USER_ID, COS_API_TOKEN_BAD, COS_BASE_URL_BAD
except:
    import os
    COS_API_TOKEN = os.environ.get('COS_API_TOKEN')
    COS_USER_ID = os.environ.get('COS_USER_ID')

COS_BASE_URL = 'https://api.careeronestop.org/v1/jobsearch'

def get_jobs(form):
    """form is WTForm form object, convert_to_dict is True (return dict) or False (return json)"""

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

def get_postings_for_dashboard(hunt, recent_job_postings = None, start_record = 0, loops = 0):
    """get job postings for dashboard based on hunt"""

    if not recent_job_postings:
        recent_job_postings = []
    
    if hunt.o_net_code:
        keyword = hunt.o_net_code
    else:
        keyword = hunt.job_title_desired
    location = hunt.location
    radius = hunt.radius
    days_old = 14

    resp = requests.get(
        f'{COS_BASE_URL}/{COS_USER_ID}/{keyword}/{location}/{radius}/accquisitiondate/DESC/{start_record}/20/{days_old}',
        params={"locationFilter": None, "source": "NLx", "showFilters": True},
        headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
    )
    
    if resp.status_code != 200:
        return {'error': 'Job Postings from the CareerOneStop API are currently unavailable. Refresh the page to try again.'}

    for job in resp.json()['Jobs']:
        if not SavedJob.already_saved(hunt.user.id, job['JvId']):
            recent_job_postings.append(job)
            if len(recent_job_postings) > 9:
                break

    # if can't find 10 unique job postings recurse a maximum of 3 times to fill recent_job_postings
    if len(recent_job_postings) < 10 and loops < 3:
        get_postings_for_dashboard(hunt, recent_job_postings, start_record + 20, loops = loops + 1)

    prepared_job_postings = add_posted_today_flag(recent_job_postings)
    job_postings_dict = {'hunt_id': str(hunt.id),
                         'expiration': datetime.now(timezone.utc) + timedelta(hours = 1),
                         'postings': prepared_job_postings}

    return job_postings_dict

def add_posted_today_flag(job_postings):
    for posting in job_postings:
        posting_date = datetime.strptime(posting['AccquisitionDate'], '%Y-%m-%d %I:%M %p')
        difference = date.today() - posting_date.date()
        if difference.days < 1:
            posting['posted_today'] = True
        else:
            posting['posted_today'] = False
    return job_postings

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