from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, BooleanField, HiddenField, TextAreaField, DateField, URLField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, Optional

class RegistrationForm(FlaskForm):
    """Form to register a user."""

    username = StringField('Username', validators=[
        InputRequired(),
        Length(max=40, message="Must be less than 40 characters.")        
    ])
    email = StringField('Email', validators=[
        InputRequired(),
        Email(message="Must be a valid email address."),
        Length(max=100, message="Must be less than 100 characters.")    
    ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Must be at least 8 characters.")
    ])
    password_confirm = PasswordField("Confirm Password", validators=[
        InputRequired(),
        EqualTo(fieldname="password", message="Passwords do not  match.")
    ])

class LoginForm(FlaskForm):
    """Form to login user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class UserEditForm(FlaskForm):
    "Form to edit a user and add additional info"

    first_name = StringField('Username', validators=[
        Length(max=40, message="Must be less than 40 characters.")        
    ])
    last_name = StringField('Username', validators=[
        Length(max=40, message="Must be less than 40 characters.")        
    ])
    country = SelectField('Country', choices=[
       'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda',
       'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
       'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria',
       'Burkina Faso', 'Burundi', 'Côte d''Ivoire', 'Cabo Verde', 'Cambodia', 'Cameroon',
       'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
       'Comoros', 'Republic of Condo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus',
       'Czechia (Czech Republic)', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti',
       'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea',
       'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon',
       'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea',
       'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India',
       'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
       'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon',
       'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
       'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania',
       'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro',
       'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
       'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway',
       'Oman', 'Pakistan', 'Palau', 'Palestine State', 'Panama', 'Papua New Guinea', 'Paraguay',
       'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
       'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa',
       'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
       'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
       'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname',
       'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
       'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu',
       'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'U.S.A',
       'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe' 
    ])
    state = SelectField('State', choices=[
        'Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii',
        'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
        'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Minor Outlying Islands',
        'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
        'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands',
        'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island',
        'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'U.S. Virgin Islands', 'Utah',
        'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ])
    linkedin_url = StringField('Linkedin URL', validators=[
        Length(max=150, message="Must be less than 150 characters.")
    ])

class ApiJobSearchForm(FlaskForm):
    """Form to fetch api job list data."""

    keyword = StringField("What", validators=[InputRequired()], render_kw={"placeholder": "job title, O*NET code, or keywords"})
    location = StringField("Where", render_kw={"placeholder": "zip code or city, state"})
    radius = IntegerField("Radius", validators=[Optional()], render_kw={"placeholder": "miles"})
    days = IntegerField("Days Old", validators=[Optional()])
    companyName = StringField("Company Name")
    remote = BooleanField("Remote Only")
        # If remote only is selected, add "remote" to user's keyword input
    startRecord = HiddenField("Start", default=0)

class ManualJobAddForm(FlaskForm):
    """Form to manually add a job."""

    title = StringField("Job Title")
    company = StringField("Company")
    location = StringField("Location",  validators=[
        Length(max=100, message="Must be less than 100 characters.")    
    ])
    date_posted = DateField("Date Posted", validators=[Optional()])
    application_link = URLField("Link")
    job_description = TextAreaField("Description")
    job_type = SelectField("Job Type", choices=[
        ('-', ''),
        ('f', 'Full-time'),
        ('p', 'Part-time'),
        ('c', 'Contract'),
        ('i', 'Internship'),
        ('v', 'Volunteer')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    experience_level = SelectField("Experience Level", choices=[
        ('-', ''),
        ('i', 'Internship'),
        ('e', 'Entry level'),
        ('a', 'Associate'),
        ('m', 'Mid-Senior level'),
        ('d', 'Director'),
        ('x', 'Executive'),
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    salary_min = StringField("Salary range")
    salary_max = StringField()
        # ******************* write custom validator that requires both or none of below ************************
        # https://stackoverflow.com/questions/42614091/wtforms-create-form-with-both-or-no-fields-that-validates-but-not-just-one-fie
    company_size = SelectField("Company Size", choices=[
        ('-', ''),
        (1, '1-10 employees'),
        (2, '11-50 employees'),
        (3, '51-200 employees'),
        (4, '201-500 employees'),
        (5, '501-1,000 employees'),
        (6, '1,001-5,000 employees'),
        (7, '5,001-10,000 employees'),
        (8, '10,001+ employees')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    federal_contractor = SelectField("Federal contractor", choices=[
        ('-', ''),
        ('True', 'Yes'),
        ('False', 'No')
    ])
        # coerced to True, False, or None in models.SavedJob.save_job
    user_notes = TextAreaField("User Notes")

class SavedJobRegularEditForm(FlaskForm):
    """Form to edit a saved job"""

    title = StringField("Job Title")
    company = StringField("Company")
    location = StringField("Location",  validators=[
        Length(max=100, message="Must be less than 100 characters.")    
    ])
    date_posted = DateField("Date Posted", validators=[Optional()])
    application_link = URLField("Link")
    job_description = TextAreaField("Description")
    job_type = SelectField("Job Type", choices=[
        ('-', ''),
        ('f', 'Full-time'),
        ('p', 'Part-time'),
        ('c', 'Contract'),
        ('i', 'Internship'),
        ('v', 'Volunteer')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    experience_level = SelectField("Experience Level", choices=[
        ('-', ''),
        ('i', 'Internship'),
        ('e', 'Entry level'),
        ('a', 'Associate'),
        ('m', 'Mid-Senior level'),
        ('d', 'Director'),
        ('x', 'Executive'),
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    salary_min = StringField("Salary range")
    salary_max = StringField()
        # ******************* write custom validator that requires both or none of below ************************
        # https://stackoverflow.com/questions/42614091/wtforms-create-form-with-both-or-no-fields-that-validates-but-not-just-one-fie
    company_size = SelectField("Company Size", choices=[
        ('-', ''),
        (1, '1-10 employees'),
        (2, '11-50 employees'),
        (3, '51-200 employees'),
        (4, '201-500 employees'),
        (5, '501-1,000 employees'),
        (6, '1,001-5,000 employees'),
        (7, '5,001-10,000 employees'),
        (8, '10,001+ employees')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    federal_contractor = SelectField("Federal contractor", choices=[
        ('-', ''),
        ('True', 'Yes'),
        ('False', 'No')
    ])
        # coerced to True, False, or None in models.SavedJob.save_job
    user_notes = TextAreaField("User Notes")

class SavedJobCosEditForm(FlaskForm):
    """Form to edit a saved job"""

    job_type = SelectField("Job Type", choices=[
        ('-', ''),
        ('f', 'Full-time'),
        ('p', 'Part-time'),
        ('c', 'Contract'),
        ('i', 'Internship'),
        ('v', 'Volunteer')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    experience_level = SelectField("Experience Level", choices=[
        ('-', ''),
        ('i', 'Internship'),
        ('e', 'Entry level'),
        ('a', 'Associate'),
        ('m', 'Mid-Senior level'),
        ('d', 'Director'),
        ('x', 'Executive'),
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    salary_min = StringField("Salary range")
    salary_max = StringField()
        # ******************* write custom validator that requires both or none of below ************************
        # https://stackoverflow.com/questions/42614091/wtforms-create-form-with-both-or-no-fields-that-validates-but-not-just-one-fie
    company_size = SelectField("Company Size", choices=[
        ('-', ''),
        (1, '1-10 employees'),
        (2, '11-50 employees'),
        (3, '51-200 employees'),
        (4, '201-500 employees'),
        (5, '501-1,000 employees'),
        (6, '1,001-5,000 employees'),
        (7, '5,001-10,000 employees'),
        (8, '10,001+ employees')
    ], validators=[Optional()])
        # '-' changed to Null in JS file
    user_notes = TextAreaField("User Notes")

class NewJobHuntForm(FlaskForm):
    """Form to create a new Job Hunt from dialog. Form is not displayed."""

    name = StringField()
    job_title_desired = StringField()
    o_net_code = StringField()
    location = StringField()
    radius = IntegerField(validators=[Optional()])
    non_us = BooleanField()
    remote = BooleanField()
    app_goal_time_frame = StringField()
    app_goal_number = IntegerField()
    hired_by_goal_date = DateField()
    description = StringField()

    # https://stackoverflow.com/questions/33429510/wtforms-selectfield-not-properly-coercing-for-booleans

# class JobAppCreateForm(FlaskForm):
#     """Form to create a new job app from dialog. Form is not displayed."""

#     date_applied = DateField()
#     # In popup-ja.html I add a custom select field here from which the value is transferred to the job_hunt_id field
#     id = IntegerField()
#         # saved job id
#     user_id = IntegerField()
#     job_hunt_id = IntegerField()