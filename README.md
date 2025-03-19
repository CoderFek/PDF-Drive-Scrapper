# 📚 PDF Drive Scraper  

A Python-based scraper that searches for book titles on [**PDF Drive**](https://www.pdfdrive.com/), extracts the book's download page, and retrieves the direct download link using **Selenium** and **BeautifulSoup**. The scraped data is saved in a CSV file.


## ✨ Features  

- **Automated Search**: Finds books based on user-defined titles.  
- **Scrapes Download Links**: Extracts the final download URL using Selenium.  
- **Saves to CSV**: Stores book titles and download links in `Books.csv`.  
- **Headless Browsing**: Uses Selenium for interacting with dynamic pages.

## 👾 Installation  

### 1. Clone the Repository  

```sh
git clone https://github.com/CoderFek/PDF-Drive-Scrapper.git
cd src
```

### 2. Install Dependencies  

Ensure you have Python 3.7 or later installed, then run:  

```sh
pip install -r requirements.txt
```
## How It Works ([SKIP](#usage))

### 1. Setup Web Driver  

The script initializes a Chrome WebDriver to handle JavaScript-rendered content:  

```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### 2. Search for Books  

The script performs a search on PDFDrive, extracts relevant results, and finds the exact match:  

```python
url = f'https://www.pdfdrive.com/search?q={title}'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
search_results = soup.find_all('a', {'class': 'ai-search'})
```

### 3. Extract Download Link  

Once an exact match is found, Selenium navigates to the download page and fetches the final download link:  

```python
final_download_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'btn-user'))
)
download_href = final_download_button.get_attribute('href')
```

### 4. Save Results  

The extracted book details are saved in a CSV file:  

```python
def save_to_csv(books, filename='Books.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Download Link'])
        for book in books:
            writer.writerow([book['title'], book['download_link']])
```

## ✅ Usage  

1. Edit the `titles_to_scrape` list in `pdfDrive_scrapper.py`:  

```python
titles_to_scrape = [
    '''
    ENTER BOOK TITLES HERE
    '''
]
```

2. Run the script:  

```sh
python pdfDrive.scrapper.py
```

3. Check the output in `Books.csv`. Example output:

```sh
|        Title       |               Download Link             |
|--------------------|-----------------------------------------|
| Python Programming | https://www.example.com/python-download |
| Machine Learning   | https://www.example.com/ml-download     |
```

4. Open download_books.py and add the directory path for downloaded books by editing `download_dir`.

```python
'''
ENTER ABSOLUTE OR RELATIVE PATH OF THE DIRECTORY YOU WANT TO SAVE THE DOWNLOADED BOOKS IN.

'''
download_dir = 'Books'  # To use the root directory only enter the directory name
```
  
5. To download books, run the script:

```sh
python download_books.py
```

### ‼️ Disclaimer ‼️ 

- This script is not intended for bulk downloads or unauthorized access.  
- Use it responsibly and comply with website policies.  
- The author is not responsible for misuse.

## License  

This project is licensed under the MIT License. 
