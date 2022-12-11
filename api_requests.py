import requests

from keys import COS_API_TOKEN, COS_USER_ID, COS_BASE_URL

def get_jobs(form):
    """form is WTForm form object, convet_to_dict is True (return dict) or False (return json)"""

    keyword = form.keyword.data
    location = form.location.data
    radius = form.radius.data
    days = form.days.data
    companyName = form.companyName.data
    startRecord = form.startRecord.data
    if form.remote.data:
        keyword = keyword + " remote"

    resp = requests.get(
        f'{COS_BASE_URL}/{COS_USER_ID}/{keyword}/{location}/{radius}/0/0/{startRecord}/10/{days}',
        params={"companyName": companyName, "locationFilter": None, "source": "NLx", "showFilters": True},
        headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
    )
        
    return resp.json()

def get_job_details(job_id):
    """job_id is COS job id"""
    
    resp = requests.get(
        f'{COS_BASE_URL}/{COS_USER_ID}/{job_id}',
        headers={"Content-Type": "application/json", "Authorization": f'Bearer {COS_API_TOKEN}'}
    )

    return resp.json()