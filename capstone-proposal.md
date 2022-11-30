# Jobalyze:
## Job Application Tracker (and Job Finder)

1. Goal of the website  
    - It will be an app designed to help job seekers organize their job hunt, track open applications, and refine job hunt strategies in addition to finding and applying to job openings.
2. User Demographic  
    - Users of the site would be adult job seekers who are in the process of a potentially long job hunt. I want this application to also be specifically useful for the Springboard Community and the larger tech. community.
3. Data used in the site  
    - There will be at least two sources of data, data generated from the API and data provided by the user.
    - API data: from the API, I will be importing data on current job openings for the job search portion of the website.
    - User data: I will be storing the following data provided by the user:
        - User information including username and email required to register a user, and also optionally, full name, location, linkedin profile, and maybe more.
        - Saved jobs: the user will have a saved jobs list where they can save job info for jobs that they are interested in.
        - Job hunt info/goals (the user will define one or more “job hunts” where they can store goals and under which they can store data associated with the jobs that they’ve applied to).
        - Job applications: Under a particular job hunt, the user will store information about the jobs that they’ve applied to and the application strategies that they used.
4. Database Schema   
    - Users table with user data.
    - Saved Jobs table with storing the data for the jobs that users have saved.
    - Job Hunts table storing a user’s “job hunts.”
    - Job Applications table (extends Saved Jobs table) that stores additional information about the jobs that a user has applied to.
    - Strategies table that stores a user’s defined strategies for each job hunt.
    - Applications/Strategies table that connects the strategies with the applications that user used those strategies for (man-to-many relationship).
5. API
    - I plan to use the Career One Stop “List Jobs” API: https://www.careeronestop.org/Developers/WebAPI/Jobs/list-jobs.aspx
    - This API seems well-maintained and is completely free with no request limits.
    - It doesn’t have categories for some useful data such as whether the job is remote, the experience level required, or salary range information, but it is the most extensive free API that I’ve found for U.S. jobs.
6. Functionality  
    - Not logged-in users will be able to access a home page, login page, a registration page, and the job search page (the API requires that I allow not logged-in users to access the job search). They can view the results of the job search page and the details of the jobs that appear in the search but can’t save jobs or create a “job hunt.”
    - Logged-in users will additionally be able to do the following:
        - Save jobs that appear in the job search.
        - Save jobs found elsewhere by entering the job information in a form.
        - View a saved jobs page that lists their saved jobs.
        - Create “job hunts” through a form where they specify what kind of job they are seeking, their timeline, their goals, and set application strategies.
        - Mark a job from the saved jobs list as “applied to”, mark what “job hunt” that job corresponds with, and mark the application strategies that they used for that job.
        - View a page that lists a user’s “job hunts.”
        - View a page that shows the details of a particular job hunt including a list of the jobs that they applied to corresponding to that “job hunt.” This page also allows users to update the status of their job applications and sort the list of applied-to jobs by their application status or applied-to dates, etc.
        - View an analytics page where the users can pick parameters from which to generate charts to view the success of their applications according to their defined job strategies or from characteristics of the job.
            - Use chart.js to generate charts?
7. Stretch Goal  
    - Incorporate a web scraper to pre-populate form fields for users who are manually entering jobs from Linkedin. Users would just have to provide the Linkedin job URL, and other form fields would populate.
