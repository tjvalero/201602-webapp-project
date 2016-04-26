from os import chdir
from os.path import realpath
from os.path import dirname, join as join_path
from flask import Flask, render_template, send_from_directory, request


app = Flask(__name__)


class Courses:
    def __init__(self, year, season, department, number, section, title,
                 units, instructors, meetings, core, seats,
                 enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.season = season
        self.department = department
        self.number = number
        self.section = section
        self.title = title
        self.units = units
        self.instructors = instructors
        self.meetings = meetings
        self.core = core
        self.seats = seats
        self.enrolled = enrolled
        self.reserved = reserved
        self.reserved_open = reserved_open
        self.waitlisted = waitlisted

def get_data():
    # This function opens the counts.tsv file and reads line by line.
    # With each line, it splits the words by tabs (\t)
    class_list = []
    placeholder = []
    with open(join_path(dirname(__file__), 'counts.tsv')) as fd:
        for i in range(15):
            placeholder.append('-')
        for line in fd.read().splitlines():
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
            instructors = placeholder[7]
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
                                      instructors, meetings, core, seats, enrolled,
                                      reserved, reserved_open, waitlisted))
    return sorted(class_list, key=(lambda x: x.title))

# This is the first page, no information is needed from python.
@app.route('/')
def view_root():
    return render_template('year_directory.html')

# This is the second page after the two selections have been made.
@app.route('/year_season')
def view_season():
    # As youll see, the URL will look something like "http://127.0.0.1:5000/year_season?year=2010&season=fall"
    # Everything after the '?' in the URL are aspects that can be grabbed using args as seen in the next two lines.
    year = request.args.get('year')
    season = request.args.get('season')
    same_year = []
    its_a_match = []
    class_list = get_data()
    print('list_of_courses', class_list)
    # Go through ALL instances of courses and check if selected
    # year equals course year, then add it to a list if it does
    for class_instance in class_list:
        if year == class_instance.year:
            same_year.append(class_instance)
    print('same_year', same_year)
    # With our list of classes with correct year, go through
    # this list and check if selected season equals course season
    for class_instance in same_year:
        if season == class_instance.season:
            its_a_match.append(class_instance)
    print('its_a_match', its_a_match)
    # year=year and season=season are not currently used on this page, but I am including them
    # in case you guys want to add a title that displays what options were picked.
    return render_template('offering.html', year=year, season=season, its_a_match=its_a_match)

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
