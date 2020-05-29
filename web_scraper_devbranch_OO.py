"""
Web crawler and collator. 500ms request rate. Object-oriented and strongly
typed refactor of playground code.

Written by James Kunstle -- Starting: 5/28/2020 --
"""


from bs4 import BeautifulSoup
import requests
import time as t
from typing import List

"""
Global Scope: Variables and Report Strings.
"""
catalog_URL = "https://www.bu.edu/academics/cas/courses/computer-science/"
stem_URL = "https://www.bu.edu"
"""
Crawler class
"""

class WebCrawler_CS_CL(object):

    def __init__(self, pages_URL: str, stem_URL: str, pages_start: int, pages_end: int)->None:
        """
        Variables used for requests library and reporting statuses.
        """
        self.RESPONSE_OKAY_TOKEN = 200       #expected response from server if request accepted
        self.RESPONSE_NOTFOUND_TOKEN = 404   #expected response from server if page not found
        self.SLEEP_TIME = 0.5                #500ms sleep between all requests to avoid raising DDOS flags

        self.SLEEP_MESSAGE = "Sleeping for " +  str(self.SLEEP_TIME) + " seconds to avoid DDOS flags."
        self.COMPLETE_MESSAGE = "Done with course."
        self.NOTFOUND_MESSAGE = "Status: Not Found"
        self.FAILED_MESSAGE = "Status: Failed, unspecified code"

        """
        Object Variables
        """
        self.parent_page: str = pages_URL
        self.child_page: str = stem_URL

        self.pages_start: int = pages_start
        self.pages_end: int = pages_end

        self.parent_pages: List = []
        self.child_pages: List = []
        self.courses: List = []
        return None

    def crawl_parent_pages(self, start_URL: str)->List:
        #get general data from the URL that is given

        URL = start_URL

        req = requests.get(URL)
        course_objects = []

        #perform necessary error checking
        if(req.status_code == self.RESPONSE_OKAY_TOKEN):
            #parse the HTML from the URL into a soup object.
            soup = BeautifulSoup(req.content, "html.parser")
            #based on the structure of the HTML, we need this object.
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
            print(self.COMPLETE_MESSAGE)
        elif(req.status_code == self.RESPONSE_NOTFOUND_TOKEN):
            print(self.NOTFOUND_MESSAGE)
        else:
            print(self.FAILED_MESSAGE)


        return course_objects

    def crawl_child_pages(self, start_URL:str, course_data: List)->List:
        URL: str = start_URL #this was used for debugging but is useless now
        schedule_objects = []
        for course in course_data:
            t.sleep(self.SLEEP_TIME)
            #use the URL for each individual course to access the page.
            req = requests.get(URL + course[1])

            course_schedule = []

            if(req.status_code == self.RESPONSE_OKAY_TOKEN):
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
                print(self.COMPLETE_MESSAGE)
            elif(req.status_code == self.RESPONSE_NOTFOUND_TOKEN):
                print(self.NOTFOUND_MESSAGE)
            else:
                print(self.FAILED_MESSAGE)

        return schedule_objects

    def crawl_all(self)->None:
        parent_pages = []
        child_pages = []

        for i in range(self.pages_start, self.pages_end + 1):
            local_url = self.parent_page + str(i) #get url of website page
            general_course_data = self.crawl_parent_pages(start_URL=local_url) #get the names of the courses, url-end, and prereqs

            parent_pages.append(general_course_data) #add ^^ to the pages list
            child_pages.append(self.crawl_child_pages(start_URL = self.child_page,
                                                    course_data = general_course_data)) #add schedule to pages list
            print("Finshed page: "+ str(i))
            t.sleep(self.SLEEP_TIME)

        self.parent_pages = parent_pages
        self.child_pages = child_pages

        return None

    def parse_and_join(self)->None:
        #for each page of parents and page of children:
        for parent_page, child_page in zip(self.parent_pages, self.child_pages):
            #for each course in a parent page and its details:
            for course, course_details in zip(parent_page, child_page):
                #preliminary object containing (Title, Link, Prereq string)
                course_object = [course[0], course[1], course[2]]

                #these are all of the class sections. need to be parsed and each is added individually
                for entry in course_details:
                    #initialize with semester details
                    details_object = [entry[0]]

                    info = str(entry[1]).split('\n')
                    for info_section in info[1:]:
                        details_object.append(info_section)

                    course_object.append(details_object)

                self.courses.append(course_object)
        return None

    def print(self)->None:
        for course in self.courses:
                print("")
                print("---------------------------------------------------------------")
                print("Course Title:            " + str(course[0]))
                print("Link:                    " + str(course[1]))
                print("Prereqs:                 " + str(course[2]))
                print("Schedule info:\n")

                possible_categories = ["Semester", "Section", "Instructor", "Location", "Schedule", "Notes"]
                for times in course[3:]:
                    print("\n")
                    for entry in zip(times, possible_categories):
                        print("\t" + entry[1] + ": " + entry[0])

        return None


"""
Main
"""

def main() -> None:
    scraper = WebCrawler_CS_CL(catalog_URL, stem_URL, 1, 1)
    scraper.crawl_all()
    scraper.parse_and_join()
    scraper.print()


if __name__ == "__main__":
    main()
