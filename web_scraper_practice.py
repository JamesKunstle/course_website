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

RESPONSE_OKAY_TOKEN = 200
RESPONSE_NOTFOUND_TOKEN = 404
SLEEP_TIME = 0.5 #500ms
SLEEP_MESSAGE = "Sleeping for " +  str(SLEEP_TIME) + " seconds to avoid DDOS flags."
COMPLETE_MESSAGE = "Done with page."
NOTFOUND_MESSAGE = "Status: Not Found"
FAILED_MESSAGE = "Status: Failed, unspecified code"



"""
Function definitions
"""
def get_and_print_cs_pages(input_url):
    req = requests.get(input_url) #this is where we get the initial HTML information from
    if(req.status_code == RESPONSE_OKAY_TOKEN):
        soup = BeautifulSoup(req.content, "html.parser") #conversion from req into text for parsing
        course_links = soup.find_all("strong")
        for link in course_links:
            print(link.text)

        print(COMPLETE_MESSAGE)
    elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
        print(NOTFOUND_MESSAGE)
    else:
        print(FAILED_MESSAGE)

def print_all_courses(input_url, low_bound, high_bound):
    for i in range(low_bound, high_bound + 1):
        local_url = input_url + str(i)
        get_courses_and_links_and_prereqs(local_url)
        print(SLEEP_MESSAGE)
        t.sleep(SLEEP_TIME)

def print_enhanced_for_courses_and_prereqs(input_url, low_bound, high_bound):
    pages = []
    for i in range(low_bound, high_bound + 1):
        local_url = input_url + str(i)
        pages.append(get_courses_and_links_and_prereqs(local_url))
        print("Finshed page: "+ str(i))
        t.sleep(SLEEP_TIME)

    for page in pages:
        for course in page:
            print("Course Title:    " + str(course[0]))
            print("Link:            " + str(course[1]))
            print("Prereqs:         " + str(course[2]))
            print("")

def get_courses_and_links(input_url):
    req = requests.get(input_url)

    if(req.status_code == RESPONSE_OKAY_TOKEN):
        soup = BeautifulSoup(req.content, "html.parser") #conversion from req into text for parsing
        course_feed = soup.find("ul", {"class": "course-feed"})
        feed_entries = course_feed.find_all("li")
        course_objects = []
        for entry in feed_entries:
            link = entry.find("a")
            name = entry.find("strong")
            if name is not None and link is not None:
                course_objects.append([name.text, link.attrs["href"]])
        for entry in course_objects:
            print(entry[0], entry[1])
        print(COMPLETE_MESSAGE)
    elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
        print(NOTFOUND_MESSAGE)
    else:
        print(FAILED_MESSAGE)


def get_courses_and_links_and_prereqs(input_url):
    req = requests.get(input_url)

    if(req.status_code == RESPONSE_OKAY_TOKEN):
        soup = BeautifulSoup(req.content, "html.parser") #conversion from req into text for parsing
        course_feed = soup.find("ul", {"class": "course-feed"})
        feed_entries = course_feed.find_all("li")
        course_objects = []
        for entry in feed_entries:
            link = entry.find("a")
            name = entry.find("strong")
            prereq = entry.find("span")
            if name is not None and link is not None:
                if prereq is not None:
                    course_objects.append([name.text, link.attrs["href"], prereq.text])
                else:
                    course_objects.append([name.text, link.attrs["href"], "No Prerequisites"])
        return course_objects
        print(COMPLETE_MESSAGE)
    elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
        print(NOTFOUND_MESSAGE)
    else:
        print(FAILED_MESSAGE)


"""
Calling Functions
"""
#get_and_print(url)
print_enhanced_for_courses_and_prereqs(cs_catalog_pages_url, 1, 3)
#get_courses_and_links(cs_catalog_pages_url)
