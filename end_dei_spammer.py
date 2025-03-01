import csv
import names
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import string
import time


def load_list_from_csv(file_path, header_row=False):
    """Open CSV file and load contents into a list, skipping header row"""
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        if header_row:
            next(reader) #skip header row
        return list(reader)


def generate_name():
    """Generate randomized first and last name."""
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    return first_name.lower(), last_name.lower()


def generate_random_email():
    """Generate a realistic randomized email address"""
    separators = ["", ".", "_"]
    #25 most common email domains
    domains = ["gmail.com",    
               "yahoo.com",
               "hotmail.com",
               "outlook.com",
               "aol.com",
               "icloud.com",
               "mail.com",
               "live.com",
               "yandex.com",
               "protonmail.com",
               "gmx.com",
               "zoho.com",
               "msn.com",
               "rocketmail.com",
               "att.net",
               "comcast.net",
               "verizon.net",
               "sbcglobal.net",
               "me.com",
               "mac.com",
               "inbox.com",
               "earthlink.net",
               "charter.net",
               "cox.net",
               "bellsouth.net"]
    first_name, last_name = generate_name()
    number = str(random.randint(0, 999)) if random.random() < 0.5 else ""  #Add a number 50% of the time
    separator = random.choice(separators)
    domain = random.choice(domains)
    return f"{first_name}{separator}{last_name}{number}@{domain}"


def sleep_random(min_seconds, max_seconds):
    """Sleep a random number of seconds between min and max"""
    time.sleep(random.randint(min_seconds, max_seconds))

def generate_random_message(driver, word_limit):
    """Use webdriver to get some random text, then shorten within set word limit"""
    driver.get("https://randomtextgenerator.com/")
    time.sleep(2)
    random_text_box = driver.find_element(By.ID, "randomtext_box")
    full_random_text = random_text_box.text
    
    #Randomize length of output to between 25% and 100% of limit
    word_cap = random.randint(int(word_limit/4), int(word_limit))
    all_random_words = full_random_text.split()
    capped_words = all_random_words[:word_cap]
    
    #Remove words after the last period.
    idx = -1
    while -1*idx < word_cap and not capped_words[idx].endswith('.'):
        idx -= 1
    capped_words = capped_words[:idx+1] #keep last word of last full sentence
    final_message = " ".join(capped_words) #Put spaces back between words
    return final_message


def main():
    """Generate some random data and fill out a web form using it"""
    print_logging = False
    num_loops = 666
    success_count = 0
    #US school data: https://public.opendatasoft.com/explore/dataset/us-public-schools/table/?flg=en-us
    schools = load_list_from_csv("us-schools.csv", True)
        
    for i in range(num_loops):        
        # driver = webdriver.Firefox() # In case you prefer Firefox
        driver = webdriver.Chrome()  # Opens Chrome browser
        
        curr_message = generate_random_message(driver, 450) #limit = 450 words
        print("Random Message: " + curr_message) if print_logging else None
        
        curr_email = generate_random_email()
        print("Random Email: " + curr_email) if print_logging else None
        
        curr_school, curr_zip = random.choice(schools) #Pick a random school and zip
        print("Random School: " + str(curr_school)) if print_logging else None
        print("Random Zip: " + str(curr_zip)) if print_logging else None
        
        try:
            # Go to target site
            driver.get("https://enddei.ed.gov/")
            time.sleep(2) #Wait for the page to load

            # Enter the current random email
            email_input = driver.find_element(By.ID, "email")
            email_input.send_keys(curr_email)
            
            # Enter random school name
            location_input = driver.find_element(By.ID, "location")
            location_input.send_keys(curr_school)
            
            # Enter random school zip
            zipcode_input = driver.find_element(By.ID, "zipcode")
            zipcode_input.send_keys(curr_zip)
            
            # Enter a message
            description_input = driver.find_element(By.ID, "description")
            description_input.send_keys(curr_message)
            
            sleep_random(1, 4) #randomize a waiting period
            # Click submit button
            submit_button = driver.find_element(By.ID, "submitButton")
            submit_button.click()
            
            # Wait for the results to load
            time.sleep(2)
            success_count += 1
            print("Messages successfully sent: " + str(success_count))

        finally:
            driver.quit() #Close the browser
#end main()

if __name__ == "__main__":
    main()
