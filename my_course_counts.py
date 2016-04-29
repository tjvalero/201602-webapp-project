from os import chdir
from os.path import realpath
from os.path import dirname, join as join_path
from flask import Flask, render_template, send_from_directory, request


app = Flask(__name__)

# List of cores taken from Justin's github
CORE_ABBRS = {
    'CPAF': 'Core Africa and The Middle East',
    'CPAS': 'Core Central/South/East Asia',
    'CPEU': 'Core Europe',
    'CPFA': 'Core Fine Arts',
    'CFAP': 'Core Fine Arts Partial',
    'CPGC': 'Core Global Connections',
    'CPIC': 'Core Intercultural',
    'CPLS': 'Core Laboratory Science',
    'CPLA': 'Core Latin America',
    'CMSP': 'Core Math/Science Partial',
    'CPMS': 'Core Mathematics/Science',
    'CPPE': 'Core Pre-1800',
    'CPRF': 'Core Regional Focus',
    'CPUS': 'Core United States',
    'CPUD': 'Core United States Diversity',
    'CICP': 'Core Program (obsolete)',
    'CUSP': 'Core United States (obsolete)',
    'CAFP': 'Core Africa (obsolete)',
}

# List of departments taken from Justin's github
DEPARTMENT_ABBRS = {
    'ABAR': 'Occidental-in-Argentina',
    'ABAS': 'Occidental-in-Austria',
    'ABAU': 'Occidental-in-Australia',
    'ABBO': 'Occidental-in-Bolivia',
    'ABBR': 'Occidental-in-Brazil',
    'ABBW': 'Occidental-in-Botswana',
    'ABCH': 'Occidental-in-China',
    'ABCI': 'Occidental-in-Chile',
    'ABCR': 'Occidental-in-Costa Rica',
    'ABCZ': 'Occidental-in-the-Czech Republic',
    'ABDE': 'Occidental-in-Denmark',
    'ABDR': 'Occidental-in-the-Dominican Republic',
    'ABFR': 'Occidental-in-France',
    'ABGE': 'Occidental-in-Germany',
    'ABHU': 'Occidental-in-Hungary',
    'ABIC': 'Occidental-in-Iceland',
    'ABID': 'Occidental-in-Indonesia',
    'ABIN': 'Occidental-in-India',
    'ABIR': 'Occidental-in-Ireland',
    'ABIT': 'Occidental-in-Italy',
    'ABJA': 'Occidental-in-Japan',
    'ABJO': 'Occidental-in-Jordan',
    'ABMO': 'Occidental-in-Morocco',
    'ABNA': 'Occidental-in-the-Netherlands Antilles',
    'ABNI': 'Occidental-in-Nicaragua',
    'ABNT': 'Occidental-in-the-Netherlands',
    'ABNZ': 'Occidental-in-New Zealand',
    'ABPE': 'Occidental-in-Peru',
    'ABRU': 'Occidental-in-Russia',
    'ABSA': 'Occidental-in-South Africa',
    'ABSE': 'Occidental-in-Senegal',
    'ABSM': 'Occidental-in-Samoa',
    'ABSN': 'Occidental-in-Sweden',
    'ABSP': 'Occidental-in-Spain',
    'ABSW': 'Occidental-in-Switzerland',
    'ABTN': 'Occidental-in-Taiwan',
    'ABUA': 'Occidental-in-the-United Arab Emirates',
    'ABUK': 'Occidental-in-the-United Kingdom',
    'AMST': 'American Studies',
    'ARAB': 'Arabic',
    'ARTH': 'Art History and Visual Arts/Art History',
    'ARTM': 'Art History and Visual Arts/Media Arts and Culture',
    'ARTS': 'Art History and Visual Arts/Studio Art',
    'BICH': 'Biochemistry',
    'BIO': 'Biology',
    'CHEM': 'Chemistry',
    'CHIN': 'Chinese',
    'CLAS': 'Classical Studies',
    'COGS': 'Cognitive Science',
    'COMP': 'Computer Science',
    'CSLC': 'Comparative Studies in Literature and Culture',
    'CSP': 'Cultural Studies Program',
    'CTSJ': 'Critical Theory and Social Justice',
    'DWA': 'Diplomacy and World Affairs',
    'ECLS': 'English and Comparative Literary Studies',
    'ECON': 'Economics',
    'EDUC': 'Education',
    'ENGL': 'English',
    'ENWR': 'English Writing',
    'FREN': 'French',
    'GEO': 'Geology',
    'GERM': 'German',
    'GRK': 'Greek',
    'HIST': 'History',
    'ITAL': 'Italian',
    'JAPN': 'Japanese',
    'KINE': 'Kinesiology',
    'LANG': 'Language',
    'LATN': 'Latin',
    'LING': 'Linguistics',
    'LLAS': 'Latino/a and Latin American Studies',
    'MATH': 'Mathematics',
    'MUSA': 'Music Applied Study',
    'MUSC': 'Music',
    'OXAB': 'Study Abroad',
    'PHAC': 'Physical Activities',
    'PHIL': 'Philosophy',
    'PHYS': 'Physics',
    'POLS': 'Politics',
    'PSYC': 'Psychology',
    'RELS': 'Religious Studies',
    'RUSN': 'Russian',
    'SOC': 'Sociology',
    'SPAN': 'Spanish and French Studies',
    'THEA': 'Theater',
    'UEP': 'Urban and Environmental Policy',
    'WRD': 'Writing and Rhetoric',
}

class Courses:
    def __init__(self, year, season, department, number, section, title,
                 units, instructor, meetings, core, seats,
                 enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.season = season
        self.department = department
        self.number = number
        self.section = section
        self.title = title
        self.units = units
        self.instructor = instructor
        self.meetings = meetings
        self.core = core
        self.seats = seats
        self.enrolled = enrolled
        self.reserved = reserved
        self.reserved_open = reserved_open
        self.waitlisted = waitlisted

# Gets list of instructors from get_data()
def get_instructor_list():
    list_of_instructor = []
    course_data = get_data()
    for instance in course_data:
        if instance.instructor not in list_of_instructor:
            list_of_instructor.append(instance.instructor)
    return sorted(list_of_instructor)

# gets list of departments using Justin's DEPARTMENT_ABBRS
def get_dept_list():
    list_of_dept = []
    for abbreviation in DEPARTMENT_ABBRS.keys():
        list_of_dept.append(abbreviation)
    return sorted(list_of_dept)

# gets list of departments using Justin's CORE_ABBRS
def get_core_list():
    list_of_core = []
    for abbreviation in CORE_ABBRS.keys():
        list_of_core.append(abbreviation)
    return sorted(list_of_core)


def get_data():
    # This function opens the counts.tsv file and reads line by line.
    # With each line, it splits the words by tabs (\t)
    class_list = []
    placeholder = []
    first_loop = False
    with open(join_path(dirname(__file__), 'counts.tsv')) as fd:
        for i in range(15):
            placeholder.append('-')
        for line in fd.read().splitlines():
            if first_loop:
                placeholder = line.split("\t")

                # This is to get rid of the "\n" at the end of every line
                placeholder[-1] = placeholder[-1][:-1]

                # Assigning pieces of placeholder list with respective names
                year = placeholder[0]
                season = placeholder[1]
                department = placeholder[2]
                number = placeholder[3]
                section = placeholder[4]
                title = placeholder[5]
                units = placeholder[6]
                instructor = placeholder[7].split(';')
                instructor = ", ".join(instructor)
                meetings = placeholder[8]
                core = placeholder[9]
                seats = placeholder[10]
                enrolled = placeholder[11]
                reserved = placeholder[12]
                reserved_open = placeholder[13]
                waitlisted = placeholder[14]

                # I then place each instance of Courses into a list called class_list which I
                # use later to loop through and gather specific information.
                class_list.append(Courses(year, season, department, number, section, title, units,
                                          instructor, meetings, core, seats, enrolled,
                                          reserved, reserved_open, waitlisted))
            first_loop = True
    return class_list


# This is the first page. Everything provided is used in drop down selectors.
@app.route('/')
def view_root():
    list_of_instructor = get_instructor_list()
    list_of_dept = get_dept_list()
    list_of_core = get_core_list()
    return render_template('year_directory.html', list_of_instructor=list_of_instructor, list_of_dept=list_of_dept,
                           list_of_core = list_of_core)

# This is the second page after the selections have been made.
@app.route('/year_season')
def view_season():
    # FOR GROUP:
    # The URL will look something like "http://127.0.0.1:5000/year_season?year=2010&season=fall"
    # Everything after the '?' in the URL are elements that can be grabbed using args as seen in the next five lines.
    year = request.args.get('year')
    season = request.args.get('season')
    instructor = request.args.get('instructor')
    department = request.args.get('department')
    core = request.args.get('core')
    open_only = request.args.get('open_only')
    same_year = []
    same_season = []
    same_instructor = []
    same_department = []
    same_core = []
    its_a_match = []
    class_list = get_data()
    # Go through instances of Courses and check if year
    # equals course year, then add it to a list if it does.
    if year == "Select...":
        same_year = class_list
    else:
        for class_instance in class_list:
            if year == class_instance.year:
                same_year.append(class_instance)
    # This does the same thing but this time using filtered list "same_year"
    # And so on for the rest...
    if season == "Select...":
        same_season = same_year
    else:
        for class_instance in same_year:
            if season == class_instance.season:
                same_season.append(class_instance)
    if instructor == "Select...":
        same_instructor = same_season
    else:
        for class_instance in same_season:
            if class_instance.instructor.find(instructor) != -1:
                same_instructor.append(class_instance)
    if department == "Select...":
        same_department = same_instructor
    else:
        for class_instance in same_instructor:
            if class_instance.department.find(department) != -1:
                same_department.append(class_instance)
    if core == "Select...":
        its_a_match = same_department
    # Filter again by Core...
    if core == "Show All Classes":
        same_core = same_department
    else:
        for class_instance in same_department:
            if core in class_instance.core:
                same_core.append(class_instance)
    if open_only == 'yes':
        for class_instance in same_core:
            if class_instance.enrolled < class_instance.seats:
                its_a_match.append(class_instance)
    # year and season are not currently used on this page, but I am including them
    else:
        its_a_match = same_core
    # year=year and season=season are not currently used on this page, but I am including them
    # in case you guys want to add a title that displays what options were picked.
    return render_template('offering.html', year=year, season=season, its_a_match=its_a_match)

@app.route('/secret_page')
def view_secret():
    return render_template('secret_page.html')

# The functions below lets you access files in the css, js, and images folders.
# You should not change them unless you know what you are doing.

@app.route('/images/<file>')
def get_image(file):
    return send_from_directory('images', file)

@app.route('/css/<file>')
def get_css(file):
    return send_from_directory('css', file)

@app.route('/js/<file>')
def get_js(file):
    return send_from_directory('js', file)

if __name__ == '__main__':
    chdir(dirname(realpath(__file__)))
    app.run(debug=True)
