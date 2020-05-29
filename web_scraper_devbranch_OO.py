"""
Web crawler and collator. 500ms request rate. Object-oriented and strongly
typed refactor of playground code.

Written by James Kunstle -- Starting: 5/28/2020 --
"""


from bs4 import BeautifulSoup
import requests
import time as t

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
        RESPONSE_OKAY_TOKEN = 200       #expected response from server if request accepted
        RESPONSE_NOTFOUND_TOKEN = 404   #expected response from server if page not found
        SLEEP_TIME = 0.5                #500ms sleep between all requests to avoid raising DDOS flags

        SLEEP_MESSAGE = "Sleeping for " +  str(SLEEP_TIME) + " seconds to avoid DDOS flags."
        COMPLETE_MESSAGE = "Done with course."
        NOTFOUND_MESSAGE = "Status: Not Found"
        FAILED_MESSAGE = "Status: Failed, unspecified code"

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

    def crawl_parent_pages(self, start_URL: str = None)->List:
        #get general data from the URL that is given
        if start_URL not None:
            URL = self.parent_page
        else:
            URL = start_URL

        req = requests.get(URL)
        course_objects = []

        #perform necessary error checking
        if(req.status_code == RESPONSE_OKAY_TOKEN):
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
            print(COMPLETE_MESSAGE)
        elif(req.status_code == RESPONSE_NOTFOUND_TOKEN):
            print(NOTFOUND_MESSAGE)
        else:
            print(FAILED_MESSAGE)


        return course_objects

    def crawl_child_pages(self, start_URL:str = None, course_data: List = None)->List:
        if start_URL not None:
            URL: str = self.child_page
        else:
            URL: str = start_URL

        schedule_objects = []
        for course in self.parent_pages_data:
            t.sleep(SLEEP_TIME)
            #use the URL for each individual course to access the page.
            req = requests.get(URL + course[1])

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

        return = schedule_objects

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
            t.sleep(SLEEP_TIME)

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

                    course_object.append([details_object])

                self.courses.append(course_object)
        return None

    def print(self)->None:
        for course in self.courses:
            print(course[0])
        return None






"""
Main
"""

def main() -> None:


if __name__ == "__main__":
    main()
