# Portfolio Flask App  

This project is a personal portfolio web application built to demonstrate my ability to design, deploy, and manage end-to-end data-driven applications. It highlights my skills across **data engineering, infrastructure, and application deployment**.  

The app is built with **Flask**, connected to a **PostgreSQL database**, and deployed on **AWS EC2**. It is production-ready, running behind **Nginx** with **Gunicorn**, secured via **Let’s Encrypt (HTTPS)**, and automatically deployed using **GitHub Actions CI/CD**.  

---

## 💡 Key Highlights  

- **Application Design** -> Modular Flask application with templates, static assets, and configuration management.  
- **Data Layer** -> PostgreSQL database managed through **SQLAlchemy ORM**, demonstrating ability to design and interact with relational data models.  
- **Deployment & Infrastructure** -> Hosted on **AWS EC2** with Elastic IP, reverse-proxied through **Nginx**, and served via **Gunicorn + systemd**.  
- **Security & Reliability** -> HTTPS enabled with **Let’s Encrypt SSL**, automated service management with `systemd`.  
- **DevOps & Automation** -> **GitHub Actions** workflow with a **self-hosted EC2 runner** for automated deployments on pushes to main.  

---

## 🛠️ Tech Stack  

- **Programming:** Python (Flask, SQLAlchemy)
- **Database:** PostgreSQL (Amazon RDS)  
- **Infrastructure:** AWS EC2 (Ubuntu), Nginx, Gunicorn  
- **Security:** Let’s Encrypt TLS/SSL, AWS Secrets Manager  
- **Automation / CI/CD:** Github, GitHub Actions (self-hosted runner)  
- **Frontend:** HTML, CSS, JavaScript  

---

## 🎯 Why This Project?  

I built this project to:  
- Demonstrate **end-to-end ownership** of an application — from coding and database design to deployment and automation.  
- Show practical experience with **data infrastructure tools** (PostgreSQL, SQLAlchemy) and how they integrate into real applications.  
- Highlight **DevOps practices** (CI/CD, service orchestration, cloud deployment) that are increasingly relevant in **data engineering and data management roles**.  
- Create a flexible **portfolio site** that I can expand with analytics dashboards, data visualizations, and project showcases.  

---

## ✅ Current Status  

- Deployed live at: [https://hire-hunter.com](https://hire-hunter.com)  
- Running in production on AWS with full HTTPS support.  
- CI/CD pipeline automatically deploys changes on push.  

---

## 📈 Future Improvements  

To further demonstrate my data engineering and analytics expertise, I plan to:  

- **Data Visualizations** → Add dashboards (Plotly/D3.js/Chart.js) for interactive project results and portfolio analytics.  
- **Analytics Pipeline** → Ingest and process site interaction data with a small ETL pipeline (Airflow or AWS Lambda → PostgreSQL/Redshift).  
- **Monitoring & Logging** → Integrate **Grafana + Prometheus** for performance monitoring, error tracking, and uptime visibility.  

---

📌 This project serves as a **demonstration of technical breadth** (software + data + cloud + automation) while remaining practical and extensible for my future career in **data engineering, management, and analytics leadership**.  
