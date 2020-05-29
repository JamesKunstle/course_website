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
    def __init__(self, pages_URL: str,
                       stem_URL: str,
                       pages_start: int,
                       pages_end: int)->None:
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
        self.parent_page = pages_URL
        self.child_page = stem_URL

        self.parent_pages_data = []
        self.child_pages_data = []
        self.collated_data = []
        return None
    def crawl_parent_pages(self)->None:
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

        return None
    def crawl_child_pages(self)->None:
        return None
    def collate_data(self)->None:
        return None
    def print_formatted_data(self)->None:
        return None






"""
Main
"""

def main() -> None:


if __name__ == "__main__":
    main()
