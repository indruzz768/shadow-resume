# 🧠 Shadow Resume

An AI-powered resume builder that lets users create, enhance, and manage professional resumes with smart skill extraction, PDF export, and public sharing. Built with Django, Tailwind CSS, and modern full-stack tools.

🔗 **Live Demo**: [https://shadow-resume.onrender.com](https://shadow-resume.onrender.com)  
📂 **GitHub Repo**: [github.com/indruzz768/shadow-resume](https://github.com/indruzz768/shadow-resume)

---

## ✨ Features

- 🔐 User Registration & Authentication (Email, Password)
- 👥 Role-Based Dashboards (User, Admin, Staff)
- 📝 Resume Builder (Create, Edit, Delete)
- 🤖 AI Skill Extraction from Resume Content
- 📄 Resume PDF Export (via WeasyPrint)
- 🌐 Public Resume Share via Unique URL
- 📬 Email Notifications (moderation updates)
- 📸 Profile Photo Upload
- 🧾 Resume Versioning & Tagging
- 🛡️ Admin/Staff Moderation System
- 📊 Admin Dashboard with Analytics
- 🧪 REST APIs for Resume Management
- 🎨 Tailwind CSS for UI Styling
- 🛑 Custom 404 & 500 Error Pages
- 🚀 Deployed on Render (Free Hosting)

---

## 🛠 Tech Stack

![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![WeasyPrint](https://img.shields.io/badge/-WeasyPrint-blue?style=for-the-badge)
![DRF](https://img.shields.io/badge/-Django%20REST%20Framework-red?style=for-the-badge)

---



---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/indruzz768/shadow-resume.git
cd shadow-resume

2. Create & activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies

pip install -r requirements.txt
4. Create .env file (use .env.example as reference)
env
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

5. Apply migrations & run server
python manage.py migrate
python manage.py runserver

📬 API Endpoints
/api/resumes/ – Resume CRUD API

/ai/extract-skills/ – AI skill extraction

Uses DRF Token Authentication

🧪 Running Tests
python manage.py test

📄 License
MIT License.
Feel free to use, modify, and share the project.

👤 Author
Made with ❤️ by Indran Satheesan

