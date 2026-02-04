import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_apple_news():
    try:
        url = "https://developer.apple.com/news/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        # This selector might need adjustment based on Apple's actual DOM
        articles = soup.find_all('a', class_='article-title')
        news = []
        for article in articles[:3]: # Get top 3
            title = article.get_text().strip()
            link = "https://developer.apple.com" + article['href']
            news.append(f"- [Apple] [{title}]({link})")
        return news
    except Exception as e:
        return [f"- [Apple] Error fetching news: {str(e)}"]

def get_android_news():
    try:
        url = "https://android-developers.googleblog.com/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('h2', class_='title')
        news = []
        for article in articles[:3]:
            a_tag = article.find('a')
            if a_tag:
                title = a_tag.get_text().strip()
                link = a_tag['href']
                news.append(f"- [Android] [{title}]({link})")
        return news
    except Exception as e:
        return [f"- [Android] Error fetching news: {str(e)}"]

def update_encyclopedia(news_items):
    file_path = 'public/encyclopedia.md'
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_section = f"\n\n## :newspaper: 最新平台動態 ({today})\n"
    for item in news_items:
        new_section += item + "\n"
    
    # Read existing content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Encyclopedia file not found!")
        return

    # Check if we already updated today to avoid duplicates (simple check)
    if f"({today})" in content:
        print("Already updated today.")
        return

    # Insert after the main title
    # Assuming the first line is the title, insert after line 2
    lines = content.split('\n')
    insert_index = 2
    
    # Reassemble with new section
    new_content = "\n".join(lines[:insert_index]) + new_section + "\n".join(lines[insert_index:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Encyclopedia updated.")

if __name__ == "__main__":
    print("Fetching news...")
    all_news = []
    all_news.extend(get_apple_news())
    all_news.extend(get_android_news())
    
    if all_news:
        print(f"Found {len(all_news)} items. Updating file...")
        update_encyclopedia(all_news)
    else:
        print("No news found.")
