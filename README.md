# E-commerce FAQ Chatbot

## Overview
The FAQ Chatbot is an intelligent assistant for E-commerce platforms that provides instant answers to customer queries regarding products, orders, shipping, payments, returns, subscriptions, and other services. It enhances user experience by offering 24/7 support and reduces repetitive workload on customer support teams.

## Features
- **Instant Responses:** Quickly provides answers to product and service-related queries.
- **Natural Language Understanding:** Uses SpaCy NLP model for understanding user questions.
- **Fuzzy Matching:** Handles typos and variations in user queries with RapidFuzz.
- **Extensive FAQ Database:** Supports a large collection of frequently asked questions.
- **Confidence Scoring:** Indicates how closely the question matches an FAQ.
- **Interactive Chat Interface:** User-friendly frontend with chat window and FAQ accordion list.
- **Responsive Design:** Works on desktop, tablet, and mobile devices.
- **Secure & Scalable:** Handles multiple users and maintains privacy.

## Technologies Used
- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **NLP & Matching:** SpaCy (`en_core_web_md`), RapidFuzz  
- **Cross-Origin Requests:** Flask-CORS  
- **Deployment:** Can be hosted on AWS, Heroku, or any cloud platform  

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-faq-chatbot.git
   cd ecommerce-faq-chatbot
