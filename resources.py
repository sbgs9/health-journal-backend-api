import re
import spacy

def get_lines_with_proper_nouns_and_contacts(text):
    # language model
    nlp = spacy.load("en_core_web_sm")

    # Regular expressions for phone numbers and email addresses
    phone_number_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


    doc = nlp(text)

    # storing lines with proper nouns and contacts
    lines_with_proper_nouns_and_contacts = []

    # Iterate over each sentence in the document
    for sentence in doc.sents:
        # checking for at least one proper noun
        if any(token.pos_ == "PROPN" for token in sentence):

            phone_numbers = phone_number_pattern.findall(sentence.text)
            emails = email_pattern.findall(sentence.text)

            if phone_numbers or emails:
                # Add the entire line containing both the proper noun and contact information
                lines_with_proper_nouns_and_contacts.append((sentence.text.strip(), phone_numbers, emails))

    return lines_with_proper_nouns_and_contacts


