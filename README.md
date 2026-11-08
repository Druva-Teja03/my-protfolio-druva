# Druva Teja C — Portfolio

> **"A Software Engineer's Digital Headquarters"**  
> An ultra-fast, minimalist, and recruiter-focused personal portfolio website engineered with **HTML5, CSS3, Vanilla JavaScript**, and a high-performance **Python FastAPI** backend.

---

## 📌 Project Overview

This repository houses the personal portfolio and digital engineering headquarters of **Druva Teja**—a first-year B.Tech CSE student at NIAT, S-VYASA University, building FastAPI backends, MySQL databases and computer-vision pipelines.

The project is architected with a dual philosophy:
1. **Senior Developer Craftsmanship**: Aesthetic principles inspired by Apple, Stripe, Linear, and Vercel (dark mode, glassmorphism, responsive CSS grid, 60fps canvas particles, asynchronous REST API, and SQLite database persistence).
2. **First-Year Student Simplicity**: Zero complicated build steps, zero frontend frameworks (No React, Vue, Angular, Next.js, Tailwind, Bootstrap, or jQuery), and an ultra-clean JSON data layer so content can be updated over the next 4–5 years without touching HTML or CSS.

---

## ✨ Features

- **Linear / Apple Aesthetic**: Dark palette (`#050505`), glassmorphic cards with subtle backdrop blurs, soft glowing accents (`#4F8CFF`, `#8B5CF6`), and clean typography.
- **Dynamic Content Management (JSON Data Layer)**: All personal information, projects, skills, and leadership milestones are stored in human-readable JSON files (`data/*.json`). FastAPI reads these files and renders them cleanly with Jinja2.
- **Zero-Dependency Frontend**: Pure HTML5, modern CSS3 variables/grid, and Vanilla JavaScript. Sub-second load times and lightweight footprint.
- **Interactive Canvas Particles**: Ambient, non-distracting node network drawn natively with the HTML5 Canvas API.
- **Typewriter Role Rotator**: Cycles through Druva's roles (*Backend Developer, Python & FastAPI Developer, Computer Vision Builder, Hackathon Team Lead, Aspiring SDE Intern*) with natural human typing and deletion cadence.
- **Asynchronous Contact Form**: Submits inquiries via AJAX `fetch()` directly to FastAPI (`POST /contact`) without page reloads.
- **Relational Persistence**: Submissions are validated with Pydantic and securely stored in an SQLite database using SQLAlchemy ORM.
- **Case Study Presentations**: Detailed technical architecture, problem statements, highlights, and source code links for featured projects.
- **Leadership & Hackathon Timeline**: Chronological vertical milestones showing team leadership at Advanced Tech Club, Smart India Hackathon, and InnovateX.
- **Accessibility & SEO Ready**: Semantic HTML5 tags (`<header>`, `<main>`, `<article>`, `<section>`, `<footer>`), ARIA attributes, skip link, and complete OpenGraph / Twitter meta tags.

---

## 🛠️ Tech Stack

### Frontend
- **HTML5**: Semantic markup, accessible headings, keyboard navigability.
- **CSS3**: CSS Custom Properties (Variables), Flexbox, CSS Grid, Glassmorphism (`backdrop-filter`), keyframe animations.
- **Vanilla JavaScript (ES6+)**: DOM APIs, IntersectionObserver for scroll reveals, Canvas API for particles, and Fetch API for async HTTP requests.

### Backend
- **Python 3.10+**: Core programming language.
- **FastAPI**: Modern, asynchronous web framework for high-throughput routing.
- **Uvicorn**: Lightning-fast ASGI production web server.
- **Jinja2**: Server-side template rendering engine.
- **SQLAlchemy**: Object Relational Mapper (ORM) for declarative database schemas.
- **SQLite**: Zero-configuration, serverless, transactional database.
- **Pydantic**: Type validation, data sanitization, and request schemas.

---

## 📂 Folder Structure

```text
Druva Portfolio/
│
├── main.py                  # Master entry point; initializes FastAPI, mounts static files & routes
├── database.py              # SQLite connection, engine configuration, and session factory
├── models.py                # SQLAlchemy ORM models (ContactSubmission table schema)
├── routes.py                # Application endpoints (GET /, POST /contact, GET /api/health)
├── requirements.txt         # Python package dependencies
├── README.md                # Comprehensive documentation, setup & deployment manual
│
├── data/                    # JSON Content Management & Database Storage
│   ├── personal_info.json   # Bio, headline, typing roles, social links, and metrics
│   ├── projects.json        # Featured engineering projects and case studies
│   ├── skills.json          # Categorized technical skills and proficiency badges
│   ├── achievements.json    # Leadership timeline, hackathons, and milestones
│   └── portfolio.db         # SQLite database file (created automatically on startup)
│
├── templates/
│   └── index.html           # Master semantic HTML5 template with Jinja2 placeholders
│
└── static/                  # Client-side static assets
    ├── css/
    │   └── style.css        # Pure CSS3 stylesheet with design system & responsive rules
    ├── js/
    │   └── main.js          # Pure Vanilla JavaScript (particles, typing, scroll, form)
    ├── images/
    │   ├── favicon.svg      # Geometric 'DT' brand icon
    │   ├── project-mobisense.svg   # Architectural schematic for MobiSense CityVision
    │   ├── project-watershed.svg   # Topographic flow schematic for Watershed Intelligence
    │   └── project-preschool.svg   # Responsive portal schematic for Preschool Platform
    └── assets/
        └── druva-teja-resume.pdf   # Downloadable curriculum vitae / resume
```

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have **Python 3.10 or newer** installed on your system. Check with:
```bash
python --version
```

### 2. Clone or Navigate to the Project Directory
```bash
cd "D:\Druva Portfolio"
```

### 3. Create a Virtual Environment (Recommended)
Creating an isolated virtual environment ensures packages don't conflict with other Python projects on your machine:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Development Server
You can start the server using Python directly:
```bash
python main.py
```
Or using Uvicorn with auto-reload enabled:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Open in Browser
- **Portfolio Website**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative API Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **System Health Endpoint**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## ⚙️ How to Configure FastAPI

Configuration settings are kept simple and transparent in `main.py` and `database.py`:

- **Host & Port**: Defined in `main.py` inside `if __name__ == "__main__":` block. Change `port=8000` to any desired port (e.g. `8080` or `5000`).
- **Database Location**: In `database.py`, SQLite points to `data/portfolio.db`. If you later switch to PostgreSQL or MySQL, simply change `SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"`.
- **CORS Settings**: Configured in `main.py` via `CORSMiddleware`. For production, replace `allow_origins=["*"]` with your exact custom domain (`["https://druvateja.dev"]`).

---

## 🏗️ Production Build & Optimization

Because this project uses vanilla HTML, CSS, and JavaScript, **no complex compilation or npm build step is required**.

To run in production mode with multiple worker processes:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🌐 Deployment Guide

### Option 1: Deploy on Render (Recommended — Free & Easy)

1. **Push your code to a GitHub repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Druva Teja digital portfolio"
   git branch -M main
   git remote add origin https://github.com/Druva-Teja03/druva-portfolio.git
   git push -u origin main
   ```
2. **Log into [Render.com](https://render.com)**.
3. Click **New +** -> **Web Service**.
4. Connect your GitHub repository.
5. Configure the service settings:
   - **Name**: `druva-teja-portfolio`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your audience (e.g., Singapore or Frankfurt)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click **Create Web Service**. Render will automatically clone, install dependencies, and publish your site with a free HTTPS URL (e.g., `https://druva-teja-portfolio.onrender.com`).

---

### Option 2: Deploy on Railway

1. Sign in to [Railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will automatically detect Python.
5. In the settings tab, set the Start Command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
6. Click **Generate Domain** in the Networking tab to get an active public link.

---

### Option 3: Deploy on a Linux VPS (Ubuntu / Debian with Nginx & Systemd)

1. **SSH into your VPS**:
   ```bash
   ssh root@your_vps_ip
   ```
2. **Install Python & Git**:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git nginx
   ```
3. **Clone project and create virtualenv**:
   ```bash
   git clone https://github.com/Druva-Teja03/druva-portfolio.git /var/www/portfolio
   cd /var/www/portfolio
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Create a Systemd Service** (`/etc/systemd/system/portfolio.service`):
   ```ini
   [Unit]
   Description=Druva Teja FastAPI Portfolio
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/portfolio
   ExecStart=/var/www/portfolio/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 3
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   Start and enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start portfolio
   sudo systemctl enable portfolio
   ```
5. **Configure Nginx as a Reverse Proxy** (`/etc/nginx/sites-available/portfolio`):
   ```nginx
   server {
       server_name druvateja.dev www.druvateja.dev;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   Enable site and obtain free SSL via Certbot:
   ```bash
   sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl restart nginx
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d druvateja.dev -d www.druvateja.dev
   ```

---

## 🔗 How to Connect a Custom Domain (e.g. druvateja.dev)

1. **Purchase your domain** from Namecheap, Cloudflare, GoDaddy, or Google Domains.
2. Go to your domain registrar's **DNS Management** dashboard.
3. Add the following records:
   - **Type `A`**: Name `@`, Value = IP address of your host (or the IP provided by Render/Railway).
   - **Type `CNAME`**: Name `www`, Value = your root domain (or your Render service domain e.g. `druva-portfolio.onrender.com`).
4. In your host (Render/Railway), go to **Custom Domains**, enter `druvateja.dev`, and click **Verify**.
5. Render/Cloudflare will automatically issue and renew a free Let's Encrypt SSL certificate.

---

## 📝 How to Update Content (Zero Code Changes!)

All portfolio content is decoupled from code and managed cleanly inside `data/`:

### 1. How to Add a New Project
Open `data/projects.json` and append a new JSON object to the list:
```json
{
  "id": "my-new-project",
  "title": "Smart Traffic Flow AI",
  "tagline": "Real-time Vehicle Density Optimization",
  "category": "AI & Computer Vision",
  "description": "Adaptive signal timing system using YOLOv8 video tracking.",
  "problem_statement": "Static traffic lights cause unnecessary congestion during non-peak hours.",
  "solution_architecture": "Built an asynchronous video feed processor that computes lane saturation and adjusts signal green-times dynamically.",
  "technologies": ["Python", "FastAPI", "OpenCV", "YOLOv8"],
  "github_url": "https://github.com/druvateja/smart-traffic-ai",
  "demo_url": "https://smarttraffic.example.com",
  "image": "/static/images/project-mobisense.svg",
  "featured": true,
  "highlights": [
    "35% reduction in intersection idle time",
    "Processed 4 concurrent 1080p camera feeds",
    "Exported telemetry to city dashboard via REST API"
  ]
}
```
Refresh your browser—the new project appears automatically with full styling!

---

### 2. How to Add New Skills
Open `data/skills.json`. Find the relevant category or add a new category object:
```json
{
  "name": "Docker",
  "level": "Intermediate",
  "highlight": "Containerizing FastAPI apps, multi-stage builds, Docker Compose"
}
```

---

### 3. How to Add New Leadership / Hackathon Milestones
Open `data/achievements.json` and add:
```json
{
  "id": "hackathon-winner-2025",
  "role": "Grand Prize Winner",
  "organization": "National AI Hackathon",
  "period": "2025",
  "category": "National Competition",
  "badge": "1st Place",
  "description": "Won first place out of 150 participating teams nationwide.",
  "highlights": [
    "Architected edge AI inference model running under 200MB memory footprint.",
    "Integrated automated SMS notifications via FastAPI webhooks."
  ]
}
```

---

### 4. How to Add Certificates, Internships, or Blog Posts (Future Expansion)
The architecture is pre-configured for future expansion:
1. Create `data/certificates.json` or `data/experience.json`.
2. In `routes.py`, read the file using `load_json_file("certificates.json")` and pass it to the Jinja2 context.
3. In `templates/index.html`, add a section loop:
   ```html
   {% for cert in certificates %}
     <div class="glass-card">{{ cert.title }} - {{ cert.issuer }}</div>
   {% endfor %}
   ```

---

## 🗄️ Database Explanation

The project uses **SQLAlchemy ORM** with **SQLite**:
- **Why SQLite?** Zero setup, fast, stores data in a single clean file (`data/portfolio.db`), and is completely portable.
- **Table Name**: `contact_submissions`
- **Columns**:
  - `id`: Unique integer primary key.
  - `name`: Full name of sender (max 100 characters).
  - `email`: Sender email address (indexed for rapid search).
  - `subject`: Subject of message (max 200 characters).
  - `message`: Text content.
  - `created_at`: UTC timestamp of submission.
  - `is_read`: Boolean status flag (defaults to False).

### How to View Stored Contact Submissions
You can inspect submissions directly using Python:
```bash
python -c "from database import SessionLocal; from models import ContactSubmission; db=SessionLocal(); print([(c.name, c.email, c.subject) for c in db.query(ContactSubmission).all()])"
```
Or open `data/portfolio.db` in any free tool like [DB Browser for SQLite](https://sqlitebrowser.org/) or the VS Code SQLite extension.

---

## 📡 API Endpoints

| Method | Endpoint | Description | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Renders the complete portfolio HTML page | None | `text/html` |
| `POST` | `/contact` | Accepts & validates contact form message | JSON `{name, email, subject, message}` | JSON `{success: true, message: ...}` |
| `GET` | `/api/health`| Health-check for uptime monitors | None | JSON `{status: "healthy"}` |
| `GET` | `/docs` | Interactive Swagger API documentation | None | `text/html` |

---

## 🎨 Frontend Architecture

- **`templates/index.html`**: Structured cleanly with semantic HTML5 landmarks. Uses Jinja2 expressions to iterate through the data loaded by FastAPI.
- **`static/css/style.css`**: Built on CSS variables for consistent design tokens. Employs CSS Grid for responsive alignment and subtle CSS keyframe animations for glowing pulses and typing blinks.
- **`static/js/main.js`**: Pure Vanilla JavaScript. Contains seven isolated, beginner-friendly functions:
  1. `initParticleCanvas()`: Renders interactive ambient particles.
  2. `initTypingEffect()`: Typewriter animation rotating through profile roles.
  3. `initNavigation()`: Sticky glassmorphism header & scroll-spy active link indicator.
  4. `initMobileMenu()`: Accessible mobile drawer menu toggle.
  5. `initScrollReveal()`: Progressive entrance animations with `IntersectionObserver`.
  6. `initContactForm()`: Asynchronous AJAX submission to FastAPI with live feedback banners.
  7. `initBackToTop()`: Smooth return to page header.

---

## 🔧 Troubleshooting Guide

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'fastapi'` | Dependencies not installed or virtual environment not active | Activate virtualenv (`.\.venv\Scripts\Activate.ps1`) and run `pip install -r requirements.txt`. |
| Port 8000 already in use | Another service is using port 8000 | Run on a different port: `uvicorn main:app --port 8080 --reload`. |
| Contact form returns 422 Unprocessable Entity | Pydantic validation failed (invalid email format or message too short) | Provide a valid email (e.g. `user@test.com`) and ensure message has at least 5 characters. |
| Changes in JSON files don't show up | Browser caching | Hard-refresh your browser (`Ctrl + F5` or `Cmd + Shift + R`). |

---

## 🔮 Future Improvements

1. **Blog Section**: Dedicated Markdown-based technical articles and engineering deep dives.
2. **Project Case Study Pages**: Multi-page route (`/projects/{project_id}`) for in-depth system architecture diagrams.
3. **Admin Dashboard**: Lightweight password-protected route (`/admin`) to read and mark contact messages as responded.
4. **Visitor Analytics**: Minimal privacy-preserving SQLite counter tracking weekly page hits.

---

## 👤 Author

**Druva Teja C**  
- **Title**: Backend & AI Developer (B.Tech CSE, NIAT, S-VYASA University)  
- **Location**: Bengaluru, Karnataka, India  
- **Email**: [druvateja08@gmail.com](mailto:druvateja08@gmail.com)  
- **GitHub**: [github.com/Druva-Teja03](https://github.com/Druva-Teja03)  
- **LinkedIn**: [linkedin.com/in/druva-teja-c](https://www.linkedin.com/in/druva-teja-c/)  

---
*All content comes from `data/*.json`. Edit those files to update the site.*
