from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import time
import csv


start_time = time.time()


def scrape_pdf_drive(titles_to_scrape):
    books = []

    for title in titles_to_scrape:
        url = f'https://www.pdfdrive.com/search?q={title}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = soup.find_all('a', {'class': 'ai-search'})
        if not search_results:
            print(f"No results found for the book: {title}")
            continue
        else:
            exact_match = False
            for result in search_results:
                book_title = result.get('title', result.get_text()).strip()

                if book_title.lower() == title.lower():
                    exact_match = True
                    book_link = f"https://www.pdfdrive.com{result.get('href')}"
                    response = requests.get(book_link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    download_button = soup.find('a', {'id': 'download-button-link'})
                    download_page_link = f"https://www.pdfdrive.com{download_button['href']}"
            
                    books.append({'title': book_title,
                                  'link': download_page_link})
                    break
            
            if not exact_match:
                print(f"No exact match found for the title {title}")
            

    return books


# Finding the download link using selenium

def get_download_link(download_page_url):
    driver.get(download_page_url)
    
    try:
        
        # Wait for the final download button
        final_download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-user'))
        )
        
        # Extract the href attribute
        download_href = final_download_button.get_attribute('href')
        
        return download_href
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# save to csv
def save_to_csv(books, filename='Books.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Download Link'])
        for book in books:
            writer.writerow([book['title'], book['download_link']])


# main function that involes the other two functions
def main():
    titles_to_scrape = [
        '''
        ENTER BOOK LIST HERE

        For example:
        Python Programming,
        Machine learning,
        ...

        For accurate book list use AI.
        '''

        
    ]

    books = scrape_pdf_drive(titles_to_scrape)

    for book in books:
        download_link = get_download_link(book['link'])
        if download_link:
            book['download_link'] = download_link
        else:
            book['download_link'] = 'Download link not found'

    save_to_csv(books)

    # Print the books with their titles and download links
    for book in books:
        print(f"Title: {book['title']}")
        print(f"download_link: {book['download_link']}")
        print()

    end_time = time.time()
    time_taken = end_time - start_time
    print(time_taken)
    


# Invoking the main function
if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    main()
    driver.quit()