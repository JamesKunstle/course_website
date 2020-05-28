"""
This is a website crawler playgrounf that is designed with a 500ms-tick to avoid any DDOS complaints.

It crawls the course catalog provided to students from BU.

Written by James Kunstle -- Starting: 5/26/2020 --
"""


from bs4 import BeautifulSoup
import requests
import time as t


"""
Global Scope: Variables and Report Strings.
"""
cs_catalog_pages_url = "https://www.bu.edu/academics/cas/courses/computer-science/"

#stem that will be used for the other pages after getting the general course data.
academics_url_stem = "https://www.bu.edu"

RESPONSE_OKAY_TOKEN = 200
RESPONSE_NOTFOUND_TOKEN = 404
SLEEP_TIME = 0.5 #500ms
SLEEP_MESSAGE = "Sleeping for " +  str(SLEEP_TIME) + " seconds to avoid DDOS flags."
COMPLETE_MESSAGE = "Done with page."
NOTFOUND_MESSAGE = "Status: Not Found"
FAILED_MESSAGE = "Status: Failed, unspecified code"

"""
Functions
"""

def print_general_course_data(input_url, low_bound, high_bound):
    pages = []
    for i in range(low_bound, high_bound + 1):
        local_url = input_url + str(i)
        pages.append(get_general_course_data(local_url))
        print("Finshed page: "+ str(i))
        t.sleep(SLEEP_TIME)

    for page in pages:
        for course in page:
            print("Course Title:    " + str(course[0]))
            print("Link:            " + str(course[1]))
            print("Prereqs:         " + str(course[2]))
            print("")

def print_general_and_schedule_data(input_url, stem_url, low_bound, high_bound):
        pages = []
        schedules = []
        for i in range(low_bound, high_bound + 1):
            local_url = input_url + str(i) #get url of website page
            general_course_data = get_general_course_data(local_url) #get the names of the courses, url-end, and prereqs

            pages.append(general_course_data) #add ^^ to the pages list
            schedules.append(get_professor_and_schedule_data(stem_url, general_course_data)) #add schedule to pages list
            print("Finshed page: "+ str(i))
            t.sleep(SLEEP_TIME)


        for page, schedule in zip(pages, schedules):
            for course, schedule_data in zip(page, schedule):
                print("Course Title:            " + str(course[0]))
                print("Link:                    " + str(course[1]))
                print("Prereqs:                 " + str(course[2]))
                print("Schedule info:\n")

                for entry in schedule_data:
                     print("")
                     print("Semester:       " + str(entry[0]))

                     info = str(entry[1]).split('\n')
                     possible_categories = ["Section", "Instructor", "Location", "Schedule", "Notes"]
                     for info_section in zip(possible_categories, info[1:]):
                         print(info_section[0] + ": " + info_section[1])


                print("")
                print("---------------------------------------------------------")


def collate_general_and_schedule(input_url, stem_url):
    print( get_professor_and_schedule_data(stem_url, get_general_course_data(input_url)))


def get_professor_and_schedule_data(input_url, course_objects):
    schedule_objects = []
    for course in course_objects:
        t.sleep(SLEEP_TIME)
        #use the URL for each individual course to access the page.
        req = requests.get(input_url + course[1])

        course_schedule = []

        if(req.status_code == RESPONSE_OKAY_TOKEN):
            #parse the HTML from the URL into a soup object.
            soup = BeautifulSoup(req.content, "html.parser")
            #based on the structure, we need this object.
            whole_schedule = soup.find("div", {"class":"cf-course"})

            semesters = whole_schedule.find_all("h4")
            course_details = whole_schedule.find_all("table")

            for semester, detail in zip(semesters, course_details):
                sem = semester.find("strong")
                det = detail.find_all("tr")[1]
                course_schedule.append([sem.text, det.text])

            schedule_objects.append(course_schedule)
            print(COMPLETE_MESSAGE)
        elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
            print(NOTFOUND_MESSAGE)
        else:
            print(FAILED_MESSAGE)


    return schedule_objects


#returns an array of courses that include (name, url_postfix, prereqs)
def get_general_course_data(input_url):
    #get general data from the URL that is given
    req = requests.get(input_url)
    course_objects = []

    #perform necessary error checking
    if(req.status_code == RESPONSE_OKAY_TOKEN):
        #parse the HTML from the URL into a soup object.
        soup = BeautifulSoup(req.content, "html.parser")
        #based on the structure, we need this object.
        course_feed = soup.find("ul", {"class": "course-feed"})
        feed_entries = course_feed.find_all("li")
        for entry in feed_entries:
            link = entry.find("a")
            name = entry.find("strong")
            prereq = entry.find("span")
            if name is not None and link is not None:
                if prereq is not None:
                    course_objects.append([name.text, link.attrs["href"], prereq.text])
                else:
                    course_objects.append([name.text, link.attrs["href"], "No Prerequisites"])
        print(COMPLETE_MESSAGE)
    elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
        print(NOTFOUND_MESSAGE)
    else:
        print(FAILED_MESSAGE)

    return course_objects


"""
Calling Functions
"""
#print_general_course_data(cs_catalog_pages_url, 1, 3)
#collate_general_and_schedule(cs_catalog_pages_url, academics_url_stem)
print_general_and_schedule_data(cs_catalog_pages_url, academics_url_stem, 1, 1)
