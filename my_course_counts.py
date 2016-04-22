from os import chdir
from os.path import realpath
from os.path import dirname, join as join_path
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)


class Courses:
    def __init__(self, year, season, number, section_title,
                 units, instructors, meetings, core, seats,
                 enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.season = season
        self.number = number
        self.section_title = section_title
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
    class_list = []
    placeholder = []
    with open(join_path(dirname(__file__), 'counts.tsv')) as fd:
        for i in range(13):
            placeholder.append('-')
        for line in fd.read().splitlines():
            placeholder = [word for word in line.split("\t") if word is not ""]
            placeholder[3:5] = [' '.join(placeholder[3:5])]
            placeholder[-1] = placeholder[-1][:-1]
            year = placeholder[0]
            season = placeholder[1]
            department = placeholder[2]
            number = placeholder[3]
            section_title = placeholder[4]
            units = placeholder[5]
            instructors = placeholder[6]
            meetings = placeholder[7]
            core = placeholder[8]
            seats = placeholder[9]
            enrolled = placeholder[10]
            reserved = placeholder[11]
            reserved_open = placeholder[12]
            waitlisted = placeholder[13]
            class_list.append(Courses(year, season, department, number, section_title, units,
                                   instructors, meetings, core, seats, enrolled,
                                   reserved, reserved_open, waitlisted))
    return sorted(class_list, key=(lambda x: x.section_title))

# @app.route('/directory')
# def view_directory():
#     stu = get_data()
#     return render_template('directory.html', students = stu)

@app.route('/directory')
def view_root():
    class_list = get_data()
    return render_template('base.html', classes = class_list)

@app.route('/<section_title>')
def view_section_title(section_title):
    my_list = get_data()
    for course in my_list:
        if course.section_title == section_title:
            section_title = section_title
    return render_template('offering.html', secton_title=section_title)




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
