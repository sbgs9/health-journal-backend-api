from flask import Flask, request, jsonify
from urllib.parse import urlparse,urljoin
import requests
import re
from urlValidatorFun import *
from bs4 import BeautifulSoup
import validators

def crawlerParagraph(link):
    # Check if URL has been visited before
    # if link in visited_urls:
    #     print("Already Visited")
    #     return

    text_with_urls = ""


    response = requests.get(link)
    html = response.text

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract text and URLs from all paragraphs
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text(strip=True)

        for anchor in paragraph.find_all('a', href=True):
            # Extract the href attribute
            href = urljoin(link, anchor['href'])
            if is_pdf_url(href):
                print(f"Found PDF URL: {href}")

            # anchor tag text with the text and href combined
            paragraph_text = paragraph_text.replace(anchor.get_text(), f"{anchor.get_text()}  {href}")

        # Append the modified paragraph text to the result
        text_with_urls += paragraph_text + " " + "\n"


    print("Data is being added successfully for: ", link)
    return text_with_urls


def crawlerPDF(link):
  relevant_pdf = []

  url = link


  response = requests.get(url)
  print(response)


  soup = BeautifulSoup(response.text, 'html.parser')

  hyperlinks = soup.find_all('a')

  for link in hyperlinks:
      href = link.get('href')
      if href and validators.url(href) and is_pdf_url(href):
          if href not in relevant_pdf:
              relevant_pdf.append(href)

  return relevant_pdf