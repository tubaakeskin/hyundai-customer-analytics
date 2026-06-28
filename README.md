# 🚙 Hyundai Customer Insights & QA Analytics Pro

This project is a **Customer Experience (CX) and Quality Assurance Decision Support System** developed to track chronic production defects, customer satisfaction trends, and model performances by analyzing **more than 8,200 real customer feedbacks** belonging to Hyundai models (Elantra, Accent, Tucson, Sonata, Santa Fe, Azera).

## 🚀 Live Application
Test the application directly in your browser: [Hyundai Customer Analytics App](https://hyundai-customer-analytics.streamlit.app/)

## 🎯 Key Features & Project Highlights

*   **Scroll-Free Executive Summary:** Access all critical metrics, pros, cons, and strategic action plans on a single screen without needing to scroll down.
*   **QA Alert (Quality Assurance Warning):** The system automatically triggers a Quality Assurance alert and requests a root-cause analysis whenever the negative feedback rate exceeds the 20% threshold within the filtered dataset.
*   **Lightweight Morphological Pattern Classifier:** A smart, tailored algorithm designed to bypass heavy libraries (~2 GB). It focuses on word roots and suffixes to handle negation (such as detecting Turkish negative structures like "-medim", "-madı", "değil", "yok") within milliseconds, while successfully filtering out random/meaningless character strings.
*   **Advanced Data Optimization:** Real-time dynamic filtering and comment-sorting options based on manufacturing year, vehicle model, and raw keyword searches.

## 🛠️ Tech Stack & Tools
*   **Frontend & Deployment:** Streamlit
*   **Data Manipulation & Analytics:** Python (Pandas, NumPy)
*   **Text Processing:** Custom Morphological NLP Logic / Regular Expressions (Regex)
