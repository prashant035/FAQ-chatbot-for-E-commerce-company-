from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
from rapidfuzz import fuzz
import logging

app = Flask(__name__, template_folder='templates')
CORS(app)

logging.basicConfig(level=logging.INFO)

nlp = spacy.load("en_core_web_md")

# Expanded product-related FAQ dataset (50+ questions for demo, can be expanded)
faqs = [
    {"question": "What is your return policy?", "answer": "You can return any item within 30 days of purchase."},
    {"question": "How long does shipping take?", "answer": "Shipping usually takes 5-7 business days."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we ship to most countries worldwide."},
    {"question": "How can I track my order?", "answer": "Once shipped, you will receive a tracking number via email."},
    {"question": "What payment methods do you accept?", "answer": "We accept credit cards, PayPal, and Apple Pay."},
    {"question": "Can I change or cancel my order?", "answer": "Orders can be changed or cancelled within 2 hours of placing them."},
    {"question": "Are your products covered by warranty?", "answer": "Yes, all products come with a one-year warranty."},
    {"question": "How do I contact customer support?", "answer": "You can reach customer support via email at support@example.com or call 123-456-7890."},
    {"question": "Do you offer gift wrapping?", "answer": "Yes, gift wrapping is available for an additional fee at checkout."},
    {"question": "Is my personal information secure?", "answer": "We use industry-standard encryption to protect your data."},
    {"question": "Can I get a discount on bulk orders?", "answer": "Yes, please contact sales@example.com for bulk order discounts."},
    {"question": "What should I do if I receive a damaged product?", "answer": "Please contact customer support immediately with your order details and photos of the damage."},
    {"question": "Do you have a physical store location?", "answer": "Currently, we operate only online, but we plan to open stores soon."},
    {"question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, 9 AM to 6 PM EST."},
    {"question": "Can I update my shipping address after ordering?", "answer": "Shipping address can be updated within 1 hour of placing the order."},
    {"question": "How do I create an account?", "answer": "Click the 'Sign Up' button on the top right and fill in your details."},
    {"question": "What should I do if I forgot my password?", "answer": "Click on 'Forgot Password' at login to reset your password via email."},
    {"question": "Are your products eco-friendly?", "answer": "Yes, we are committed to sustainable and eco-friendly products."},
    {"question": "Do you have student discounts?", "answer": "Yes, students can get 10% off with a valid student ID."},
    {"question": "What sizes are available?", "answer": "Sizes vary per product, check the product page for details."},
    {"question": "Can I pre-order new products?", "answer": "Yes, pre-orders are available for select items."},
    {"question": "Do you offer subscription services?", "answer": "Yes, check the subscriptions page for details."},
    {"question": "How do I apply a promo code?", "answer": "You can enter the promo code at checkout."},
    {"question": "Are there any hidden fees?", "answer": "No, all prices are final and include taxes."},
    {"question": "Do you offer same-day delivery?", "answer": "Same-day delivery is available in select cities."},
    {"question": "How do I return a gift?", "answer": "Gift returns can be processed through our returns portal."},
    {"question": "Do you provide product manuals?", "answer": "Yes, downloadable manuals are available on product pages."},
    {"question": "Can I track my return?", "answer": "Yes, returns have tracking numbers just like shipments."},
    {"question": "Do you offer bulk shipping?", "answer": "Yes, contact our sales team for bulk shipping options."},
    {"question": "Are your products tested for safety?", "answer": "Yes, all products go through strict safety testing."},
    {"question": "How do I replace a defective item?", "answer": "Contact customer support with photos of the defective item."},
    {"question": "What is the warranty coverage?", "answer": "Warranty covers defects in materials and workmanship for one year."},
    {"question": "Do you offer product customization?", "answer": "Yes, select products have customization options."},
    {"question": "Can I change my order after checkout?", "answer": "Order changes are allowed within 2 hours of purchase."},
    {"question": "Do you offer eco-friendly packaging?", "answer": "Yes, we use recyclable and sustainable packaging materials."},
    {"question": "Are international shipping charges included?", "answer": "No, international shipping costs vary by country."},
    {"question": "Can I schedule delivery?", "answer": "Yes, you can choose a preferred delivery date at checkout."},
    {"question": "Do you offer gift cards?", "answer": "Yes, digital and physical gift cards are available."},
    {"question": "How can I track my digital orders?", "answer": "Digital orders are delivered instantly via email with download links."},
    {"question": "Do you provide installation services?", "answer": "Yes, installation is available for select products."},
    {"question": "What is your privacy policy?", "answer": "Your data is protected according to our privacy policy listed on the website."},
    {"question": "Do you have seasonal sales?", "answer": "Yes, seasonal sales are announced on our homepage and newsletters."},
    {"question": "How do I cancel my subscription?", "answer": "Subscriptions can be cancelled via your account settings."},
    {"question": "Are returns free?", "answer": "Yes, returns are free within 30 days."},
    {"question": "Can I change my payment method after purchase?", "answer": "Yes, contact customer support to update payment details."},
    {"question": "Do you offer loyalty programs?", "answer": "Yes, join our loyalty program to earn rewards on purchases."},
    {"question": "Are your products vegan?", "answer": "Most products are vegan; check product labels for details."},
    {"question": "Can I combine multiple promo codes?", "answer": "No, only one promo code can be applied per order."},
    {"question": "Do you offer free samples?", "answer": "Yes, some products come with free samples; check product pages."},
    {"question": "What do I do if my order is delayed?", "answer": "Contact customer support with your order number for assistance."},
    {"question": "How do I unsubscribe from emails?", "answer": "Click 'unsubscribe' at the bottom of any email we send."},
    {"question": "Do you offer express shipping?", "answer": "Yes, express shipping options are available at checkout."}
]

# Precompute SpaCy docs
faq_docs = [nlp(faq["question"]) for faq in faqs]

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not (token.is_stop or token.is_punct)]
    return " ".join(tokens)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()
    if not user_question:
        return jsonify({"answer": "Please ask a question."})

    user_doc = nlp(user_question)
    sim_scores = [user_doc.similarity(fdoc) for fdoc in faq_docs]

    user_processed = preprocess_text(user_question)
    faq_processed = [preprocess_text(faq['question']) for faq in faqs]
    fuzzy_scores = [fuzz.ratio(user_processed, fp)/100 for fp in faq_processed]

    combined_scores = [(0.7*spa + 0.3*fz) for spa, fz in zip(sim_scores, fuzzy_scores)]

    top_idx = combined_scores.index(max(combined_scores))
    best_score = combined_scores[top_idx]

    if best_score < 0.6:
        return jsonify({"answer": "Sorry, I don't understand your question. Please ask a product-related question."})

    best_answer = faqs[top_idx]["answer"]
    return jsonify({"answer": best_answer, "confidence": round(best_score, 2)})

if __name__ == "__main__":
    app.run(debug=True, port=8800)
