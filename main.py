import requests
from bs4 import BeautifulSoup
import json

def scrape_goodreads_books():
    base_url = "https://www.goodreads.com/list/show/165313.Books_With_a_Goodreads_Average_Rating_of_4_0_and_above_and_With_At_Least_30_000_Ratings_?page="
    books = []
    
    for page in range(1, 25):  # 24 pages
        url = base_url + str(page)
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        book_items = soup.find_all("tr", itemtype="http://schema.org/Book")
        
        for book in book_items:
            title_tag = book.find("a", class_="bookTitle")
            author_tag = book.find("a", class_="authorName")
            avg_rating_tag = book.find("span", class_="minirating")
            
            title = title_tag.text.strip() if title_tag else "Unknown"
            author = author_tag.text.strip() if author_tag else "Unknown"
            goodreads_url = "https://www.goodreads.com" + title_tag["href"] if title_tag else "Unknown"
            
            if avg_rating_tag:
                rating_text = avg_rating_tag.text.strip()
                avg_rating = rating_text.split(" — ")[0].split()[0]  # Extracts avg rating
                ratings = rating_text.split(" — ")[1].split()[0].replace(",", "")  # Extracts number of ratings
            else:
                avg_rating, ratings = "Unknown", "Unknown"
            
            books.append({
                "title": title,
                "author": author,
                "goodreadsURL": goodreads_url,
                "avgRating": avg_rating,
                "ratings": ratings
            })
        
        print(f"Scraped page {page}")
    
    with open("goodreads_books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)
    
    print("Scraping complete. Data saved to goodreads_books.json")

if __name__ == "__main__":
    scrape_goodreads_books()
