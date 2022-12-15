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

    company = StringField("Company")
    title = StringField("Job Title")
    location = StringField("Location",  validators=[
        Length(max=100, message="Must be less than 100 characters.")    
    ])
    application_link = URLField("Link")
    job_description = TextAreaField("Description")
    user_notes = TextAreaField("User Notes")
    date_posted = DateField("Date Posted")
    job_type = SelectField("Job Type", choices=[
        (0, 'Full-time'),
        (1, 'Part-time'),
        (2, 'Contract'),
        (3, 'Internship'),
        (4, 'Volunteer')
    ])
    experience_level = SelectField("Experience Level", choices=[
        (0, 'Internship'),
        (1, 'Entry level'),
        (2, 'Associate'),
        (3, 'Mid-Senior level'),
        (4, 'Director'),
        (5, 'Executive'),
    ])
    company_size = SelectField("Company Size", choices=[
        (0, '1-10 employees'),
        (1, '11-50 employees'),
        (2, '51-200 employees'),
        (3, '201-500 employees'),
        (4, '501-1000 employees'),
        (5, '1001-5000 employees'),
        (6, '5001-10,000 employees'),
        (7, '10,001+ employees')
    ])
    salary_min = IntegerField("Salary Min")
    salary_max = IntegerField("Salary Max")

