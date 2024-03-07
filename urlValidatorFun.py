from urllib.parse import urlparse
import requests
import validators
import re

def is_pdf_url(url):
    if check_mental_health_keywords_in_url(url) and url.lower().endswith('.pdf'):
        return True
    else:
      False
      # write logic to parse pdf later

def check_mental_health_keywords_in_url(url):
    # keywords related to mental health
    mental_health_keywords = [
        'mental-health', 'behavioral-health', 'drug-abuse', 'substance-abuse',
        'addiction', 'alcoholism', 'opioid', 'overdose', 'suicide', 'stress',
        'anxiety', 'depression', 'psychology', 'therapy', 'counseling',
        'psychiatry', 'ptsd', 'trauma', 'abuse', 'violence', 'grief',
        'bereavement', 'brain-injury', 'autism', 'asd', 'adhd', 'personality',
        'crisis-center', 'hospital', 'facility', 'treatment',
        'support-group', 'therapist', 'counseling-center', 'mental-wellness',
        'emotional-health', 'coping-strategies', 'coping-skills', 'recovery',
        'self-care', 'well-being', 'peer-support', 'mental-health-awareness',
        'mindfulness', 'meditation', 'relaxation-techniques', 'anger-management',
        'substance-use-treatment', 'rehabilitation-center', 'community-mental-health',
        'mental-health-services','prevent','prevention', 'assistance', 'behavior', 'mental', 'emotional','crisis',
        'risk','hot', '988'
    ]

    # Parsing URL to extract the path
    parsed_url = urlparse(url)
    url_path = parsed_url.path

    # Check if any of the keywords are present in the URL path
    for keyword in mental_health_keywords:
        if re.search(keyword, url_path, re.IGNORECASE):
            return True

    return False


def linkExtractor(text):

    url_pattern = re.compile(r'https?://\S+')

    # all matches of the URL pattern in the text
    links = re.findall(url_pattern, text)
    for i in links:
        if not (check_mental_health_keywords_in_url(i) and validators.url(i)):
            links.remove(i)

    return links