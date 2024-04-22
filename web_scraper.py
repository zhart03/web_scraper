# Zachary Hart, section 0102

# Libraries
import re   # Used for pattern matching in strings
import requests   # Used to fetch webpages and robots.txt files
from bs4 import BeautifulSoup   # Used to parse the HTML content retrieved from webpages
import tkinter as tk   # Used for creating the GUIs present in the code
from tkinter import simpledialog, messagebox, filedialog
from urllib.parse import urljoin   # Used to construct the full URL for robots.txt files

# This allows the program to "introduce" itself properly to the website it is attempting to scrape
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# Main
def main():  
    root = tk.Tk() 
    root.title("Web Scraping GUI")

    # Create entry fields for URL and keywords
    url_label = tk.Label(root, text="Enter the URL of the website:")
    url_entry = tk.Entry(root, width=40)
    url_label.pack()
    url_entry.pack()

    # Create entry fields for potential keywords
    keyword_entries = []
    for i in range(3):
        entry_label = tk.Label(root, text=f"Enter keyword {i + 1} (optional):")
        entry = tk.Entry(root)
        entry_label.pack()
        entry.pack()
        keyword_entries.append(entry)

    # Create a submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: submit(url_entry, keyword_entries, root))
    submit_button.pack()

    # Start the Tkinter main loop
    root.mainloop()


# Function that is called when the submit button is pressed in the GUI
def submit(url_entry, keyword_entries, root):
    # Get values from entry fields
    url = url_entry.get()
    
    # Filter out empty strings from potential keywords
    keywords = []
    for entry in keyword_entries:
        keyword = entry.get()
        if keyword:
            keywords.append(keyword)

    # Close the Tkinter window
    root.destroy()

    # Check if the link can be accessed
    access = can_access_url(url)

    if access:
        # Get the content of the webpage
        webpage_content = get_webpage_content(url)

        # Check if the webpage content is retrieved successfully
        if webpage_content:
            
            # Extract relevant sentences for each keyword
            sentences_with_keywords = {}
            for keyword in keywords:
                relevant_sentences = extract_sentences_with_keywords(webpage_content, keyword)
                sentences_with_keywords[keyword] = relevant_sentences

            # Prompt user for filename
            filename = filedialog.asksaveasfilename(
                initialfile='output_sentences.txt',
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if filename:
                # Save the sentences to the selected file
                save_to_file(url, sentences_with_keywords, filename)

    else:
        # Display a message box with yes/no question
        error_popup(root)


# Function that deals with errors relating to the url. It is called if the url is invalid and if it cannot be accessed
def error_popup(root):
    retry = messagebox.askyesno("Error", "Invalid link or the webpage cannot be accessed. Do you want to try a different link?")
    if retry:
        main()
    else:
        # Close the Tkinter window
        root.destroy()


# Function that checks the legality of scraping the user's website by accessing the /robots.txt file, which lists any constraints. It also checks if the url is valid
def can_access_url(url, user_agent="*"):
    try:
        # Attempt to access the URL
        response = requests.get(url, headers=headers)

        # Check if the response status code is successful (e.g., 200)
        if response.status_code == 200:
            # Check if it is legal to scrape the given URL based on the rules specified in the robots.txt file
            base_url = '/'.join(url.split('/')[:3])
            robots_txt_url = urljoin(base_url, '/robots.txt')

            try:
                # Fetch the content of the robots.txt file
                robots_txt_content = requests.get(robots_txt_url, headers=headers).text
            except requests.exceptions.RequestException as e:
                
                # If the /robots.txt file doesn't exist for that website, it assumes that scraping is allowed
                print(f"Error fetching robots.txt file.")
                return True

            # Extract disallowed paths for the specified user-agent
            user_agent_pattern = re.compile(fr'^User-agent: {re.escape(user_agent)}.*?((?:Disallow:.*?$\s*)+)', re.MULTILINE | re.IGNORECASE)
            match = user_agent_pattern.search(robots_txt_content)

            if match:
                disallowed_paths = [path.strip() for path in match.group(1).split('\n') if path.strip().startswith("Disallow:")]
                for path in disallowed_paths:
                    if path != "Disallow:" and path[10:].strip() != "/":
                        if urljoin(base_url, path[10:].strip()) in url:
                            return False
            return True

        else:
            # Returns false if the response status code is unsuccessful
            return False

    # Returns false if the url is invalid
    except requests.exceptions.RequestException as e:
        return False


# Function that retrieves the main content on the website and converts it to html
def get_webpage_content(url):
    try:
        # Get the content of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the text content from the parsed HTML
        text_content = soup.get_text(separator=' ')

        return text_content
    
    # Runs if the content cannot be accessed
    except requests.exceptions.RequestException as e:
        error_popup()
        return None


# Function that sorts the text_content into sentences and applies a sentence pattern to it to determine the relevant sentences containing the keywords
def extract_sentences_with_keywords(html_content, keyword):
    # Extract sentences containing the specified keyword
    soup = BeautifulSoup(html_content, 'html.parser')
    text_nodes = soup.find_all(string=True)
    sentence_pattern = re.compile(fr'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s*([^\.]*?\b{re.escape(keyword.lower())}\b[^\.]*?)(?=\.|$|\?|\!)')
    
    # Adds all relevant sentences to the array
    relevant_sentences = []
    for node in text_nodes:
        matches = sentence_pattern.findall(node.lower())
        relevant_sentences.extend(matches)

    # Calls the is_valid_sentence() function to check each sentence against a list of criteria
    relevant_sentences = [sentence for sentence in relevant_sentences if is_valid_sentence(sentence, soup)]

    return relevant_sentences


# Function that contains a set of criteria for a valid sentence to ensure the output contains only sentences from the main content of the webpage
def is_valid_sentence(sentence, soup):
    # Check if a sentence contains less than 15 characters, which is slightly below the average sentence length
    if len(sentence) < 15:
        return False

    # Check if a sentence contains more than 5 newlines, which could indicate a list of content not in traditional sentence form
    if sentence.count('\n') > 5:
        return False

    # Exclude sentences within "navbox" elements
    navbox_elements = soup.find_all(class_='navbox')
    for navbox in navbox_elements:
        if sentence in navbox.get_text(separator=' '):
            return False

    # Exclude sentences within "div.card" elements
    card_elements = soup.find_all(class_='card')
    for card in card_elements:
        if sentence in card.get_text(separator=' '):
            return False

    return True


# Function that saves the sentences to a .txt file for the user to then access and read
def save_to_file(url, sentences_with_keywords, filename='output_sentences.txt'):
    # Save sentences with keywords to a file with newline characters
    with open(filename, 'w', encoding='utf-8') as file:
        # Show the link at the top of the file
        file.write(f"Link: {url}\n\n")
        
        for keyword, sentences in sentences_with_keywords.items():
            file.write(f"\nKeyword: {keyword}\n\n")
            for sentence in sentences:
                file.write(f"{sentence}\n\n")
    
    # Displays a pop up showing the file was created successfully, the name of the file, and its directory path
    messagebox.showinfo("Info", f"Sentences with keywords saved to {filename}")


if __name__ == "__main__":
    main()