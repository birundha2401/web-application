# Domain-Independent Web Application Boilerplate

A clean, maintainable full-stack boilerplate built using Java's built-in HTTP server, MySQL JDBC, and Vanilla Web standards.

---

## 📁 Project Structure


---

## 🛠️ Technologies Used

* **Frontend**: HTML5, CSS3, Vanilla JavaScript (No frameworks)
* **Backend**: Java 11+ (`com.sun.net.httpserver.HttpServer`, No frameworks)
* **Database**: MySQL 8.x + JDBC (`mysql-connector-j`)

---

## 📋 Prerequisites

1. **Java Development Kit (JDK 11 or higher)**
2. **MySQL Server (version 8.0 or higher)**
3. **MySQL JDBC Driver JAR** (`backend/lib/mysql-connector-j.jar`)

---

## ⚙️ Configuration Setup

### 1. Database Setup
Run the initial schema script to create the database:
```powershell
Get-Content database/schema.sql | mysql -u root -p