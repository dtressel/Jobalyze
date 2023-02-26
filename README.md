# Jobalyze:
## Job Application Tracker (and Job Finder)
- Deployed at https://jobalyze.herokuapp.com/
- Developed by Daniel Tressel (dtresseldev@gmail.com)

### Overview
- Jobalyze is a web application designed to help job seekers organize their job search, find jobs, and track their open applications.

### Features
1. Job Postings Search
    - Available to both anonymous and registered users, users can search current U.S. job postings.
    - Job postings are collected behind the scenes through the Career One Stop API: https://www.careeronestop.org/Developers/WebAPI/Jobs/list-jobs.aspx
2. Save Job Postings
    - Registered users can easily save jobs found through the job postings search on Jobalyze by clicking a Save button found on each job postings details page.
    - Registered users can also save jobs found outside of Jobalyze by entering the job data into a form. 
3. Organize a Job Hunt
    - Jobalyze allows users to define their goals and what kind of job their looking for in a "job hunt" and optionally create multiple job hunts.
    - Newly registered users are prompted to create a job hunt and users are allowed to create additional job hunts at any time.
    - Job hunts allow Jobalyze to send the user matching job postings to the user's dashboard.
    - The user's job hunt(s) also serves as a container for their job application data, which allows the user to keep the data separate for each job hunt that they define.
4. Track Job Applications
    - Jobalyze allows users to report job applications that they've submitted.
    - After reporting the job application, users can view a table of their job applications and easily update the status of their application.
    - In the job application table, users can also view some data and stats about their job applications such as how long the job application has been open.
    - The job application table is a feature designed to help job seekers who may be applying to many jobs weekly and may have dozens of open applications to keep track of. 
5. Job Application Analytics and "Factors"
    - Users can add "factors" when they report their job applications.
    - Factors are words or short phrases defined by the user that the user can add as descriptors of that particular job application.
    - Factors can be characteristics of the job that the user is applying to or can be strategies that the user used in that particular application.
    - Factors are designed to be used to allow the user to distinguish the unique characteristics of that particular job application.
    - Users should define factors in a way so that a particular factor may be applied to several applications that have the same or similar feature.
    - The user can view what factors they added to each job application in the job application table.
    - Factors are designed to allow the user to analyze the features of a particular job application that may have made that particular application more or less successful.
    - Factors will be used for future additional analytical features that will allow users to view tables or charts measuring the success of each factor.

### Typical User Experience
1. Unregistered User:
    - A user that has not registered or signed in is mostly limited to searching for job postings.
    - An unregistered user will land at the home page with a short job search form.
    - After filling in the short job search form, the user will be redirected to search results, which will also include a form that allows the user to specify their search in more detail.
    - The user will have access to the job posting details page, which has an "apply" link, which sends them to the job posting's external application page.
2. Registered User:
    - After landing on Jobalyze's home page, a user can login or register through buttons found on the navigation bar.
    - Both a newly registered user and a returning user will be sent to the user dashboard upon login.
    - For a newly registered user, prompts on the dashboard will direct the user to create a job hunt and will be shown additional information about how to use certain features.
    - On the dashboard, the user will see four panels:
        1. Saved Jobs
        2. New Job Postings
        3. Job Applications
        4. Job Hunt Details
    - Each panel will show information about each panel's subject.
    - Expand links allow the user to be redirected to a full page of information about the selected subject.
    - Users will likely navigate back and forth between (1) viewing new job postings, (2) viewing their saved jobs and using the application links to apply to their saved jobs, (3) viewing their job applications and updating the status for their job applications, and (4) managing their job hunts. The dashboard being the main page that directs the user to the respective pages to do the above 4 things.

## Technology Used to Create Jobalyze
- Frontend Technologies
    1. HTML
    2. "Vanilla" JavaScript
    3. "Vanilla" CSS
    <br>
    ** As a way to increase proficiency and more thoroughly understand core frontend technlogies, I used no frontend libraries or frameworks. 
    <br>
- Main Backend Technologies
    1. Flask (Python framework)
    2. PostgreSQL (relational database)
- Additional Backend Tools
    1. WTForms
    2. SQLAlchemy
    3. Bcrypt
    4. Flask-Login
