# Python Web Scraper
A program designed to enhance the "Control-F" function found on countless devices, searching for up to three keywords provided by the user to pull sentences from a specified website and compile them into a .txt file for easy reading.

## How It's Made:

**Tech used:** HTML, Python

This program takes advantage of Python's HTML handling and web-surfing abilities to create a .txt file containing the important info needed by the user. It was designed with the idea of streamlining the research process by having a program do the skimming for you and allowing
the user to skip straight to looking at all the relevant info.

It was important to consider the legality of doing this on websites that have restrictions for web scraping. In order to identify websites that have these restrictions, the program utilized a function that read the Robots.txt files that many websites are equipped with.
These files outline all of the restrictions for scraping a specific website and if the program detects a restriction that it could potentially break, the program would not run.

One of the biggest challenges in designing this program was developing the definition of a sentence. Since computers are pretty dumb when it comes to human languages, these rules must be clearly outlined so that when picking and choosing relevant sentence containing
certain keywords, the program can distinguish when a word appears, for example, as a link to another page on the website, and when it appears in a full, complete sentence. This took much trial and error, but the definition finally reached a point that the program would rarely
include false sentences.

In order to ensure the user understood how to use the program, a Graphical User Interface (GUI) was created that popped up when the program was first run. It provided a spot to paste a website link as well as three optional spots to put any keywords the user wanted to
search for. For an optimal run, the sentences would be compiled in the background, then saved to the user's computer for later usage. However, the program was also equipped to display any error messages that could have occurred from problems with visiting certain sites,
not being able to find any of the keywords, or anything else anticipated by the program.

The last major part of this project was formatting the arrays of sentences into a .txt file to be easily read by the user. Since up to three keywords could be provided by the user, it made sense to format the .txt file in a way that the sentences were separated by the
keywords they corresponded to. In the .txt file, one would see a keyword, then the list of sentences below that, which would be the same pattern for any subsequent keywords. Additionally, there is added functionality to name the .txt file to anything the user desires
as well as to save it in any file location on the user's computer.

Each of these components work together to enhance one's ability to skim through articles, blogs, online encyclopedias, etc. to get the important information as fast as possible. It is intended to be used as a research aid to increase the rate at which information can be
consumed and ensure that the right information needed by the user is reaching them in an efficient manner.

## Lessons Learned:

This program was my first major coding project with an outcome that could benefit me and my future studies. Throughout the designing process, I was constantly learning new things and needing to overcome countless challenges. One of the most impressive parts to me was
Python's ability to correctly handle both URLs and HTML text. At the time, I had been working with Python for the class that assigned this project. We were allowed to choose any coding language that made sense for our chosen project, and it took very little research
to see that Python would be the ideal language for my program.

The development of this program taught me how to utilize the resources available to me. Throughout the development, I found myself scrolling through other GitHub pages, Stack Overflow, and even asking ChatGPT questions that were not available through regular web-surfing.
This was encouraged by my professor from the beginning of the class and proved to be a vital asset to the coding process.

The first test that gave an acceptable .txt file was somewhat late in the development process. Leading up to this point, I had been conducting small tests to check the functionality of each individual function, which often revealed missed mistakes. However, the frequent
checks paid off when the first full test of the program worked almost perfectly. I had been using a Wikipedia page to test my program, and was stunned when I opened up the .txt file to see the sentences I expected to see there. It was truly an incredible feeling to see
my very own program work, and made me excited to get the chance to use it for my own research.

## How to Use:

In order to use this program on any computer, you must download the "web_scraper.exe" file, since this contains all the necessary files and libraries needed to independently run.

Once downloaded, double click on the file to run it. A command window should pop up first, then the starup GUI containing a spot for you to input a URL, then up to three unique keywords that may be found on this website.
Click submit once ready.

The program will now start to perform its web scraping duties. If any errors occur, please read the message carefully before restarting the program to avoid causing more errors.

Once the sentences have been compiled into a .txt file, it will then give you the option to rename the file from its default name, as well as choose a file location to store your .txt file. Once these have been selected,
save the file in the location. A final popup should show, saying that the file was successfully saved under the specified name and in the specified file location. Once this popup is closed, the program will finish running
and the .txt file will be available for use.
