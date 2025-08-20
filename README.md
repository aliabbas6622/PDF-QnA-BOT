A Python-based project that lets you upload a PDF and ask questions about its content using Google Generative AI. Perfect for students, researchers, or anyone who wants instant answers from large documents.

✨ Features

📂 Upload any PDF file

🤖 Ask natural language questions about the content

⚡ Powered by Google’s Generative AI

🔑 Secure API key management with .env

📦 Installation

Clone the repository

git clone https://github.com/aliabbas6622/Langchain-Practice.git
cd Langchain-Practice


Set up a virtual environment

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies

pip install -r requirements.txt


Configure environment variables

Copy .env.example → .env

Add your API key in .env

GOOGLE_API_KEY=your_api_key_here

▶️ Usage

Run the script:

python Pdf-QnA.py


It will:

Load your PDF

Process its content

Let you ask questions and get AI-generated answers
