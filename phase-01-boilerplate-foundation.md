# Phase 1 — Project Foundation & Web Application Boilerplate Context

## 1. Purpose and Scope

### Purpose
Establish a clean, maintainable, full-stack boilerplate for a domain-independent web application using **strictly Vanilla Java and Web standards without any third-party frameworks**. This foundation will later support an authentication system and a business domain application (whose specific requirements are not yet determined).

### Current Scope Boundaries
* **In Scope**:
  * Java HTTP Server (`com.sun.net.httpserver.HttpServer`) listening on port `8080`.
  * Endpoint `GET /api/health` returning JSON health status (`{"status":"UP","database":"CONNECTED"}`).
  * Static file handler serving frontend files (`index.html`, `style.css`, `app.js`) directly from the Java server.
  * Database configuration loader (`config/db.properties`) and JDBC connectivity manager (`Database.java`).
  * Initial MySQL database schema script (`database/schema.sql`).
  * Vanilla HTML/CSS/JS landing page displaying live system health.
  * Standalone TDD unit test suites (`DatabaseTest`, `HealthHandlerTest`, `StaticFileHandlerTest`).
* **Explicitly Out of Scope / Deferred**:
  * User registration, login, logout flows.
  * Password hashing (BCrypt, Argon2, etc.).
  * Session management, JWT, or cookies.
  * User, session, role, or permission database tables.
  * Application business logic.

---

## 2. Starting State

* **Initial Workspace**: `C:\Users\ADMIN\Desktop\Project` was completely empty at the start of Phase 1.
* **Environment**: Windows OS with PowerShell environment.

---

## 3. Technologies and Constraints

| Layer | Technology Selected | Explicitly Avoided / Forbidden |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, CSS3, Vanilla JavaScript | React, Angular, Vue, Bootstrap, Tailwind, SASS |
| **Backend Server** | Java JDK Built-in (`com.sun.net.httpserver.HttpServer`) | Spring, Spring Boot, Express, Jersey, Micronaut, Quarkus |
| **Database ORM/Driver** | MySQL 8.x + Java Database Connectivity (JDBC) | Hibernate, JPA, MyBatis, JOOQ |
| **Build/Test** | Plain `javac` / `java` with custom main test runners | Maven, Gradle, Spring Test (Vanilla JDK only) |

---

## 4. Architecture

The application is structured as a unified, single-origin architecture where the Java backend handles both API endpoints and static file serving to eliminate CORS complexity.

```
+-----------------------------------------------------------------------+
|                             Browser Client                            |
|                     (frontend/index.html + app.js)                    |
+-----------------------------------+-----------------------------------+
                                    |
            HTTP GET / (Static Files) | HTTP GET /api/health (JSON API)
                                    v
+-----------------------------------------------------------------------+
|                    Java JDK HttpServer (Port 8080)                    |
|                                                                       |
|  +----------------------------+  +---------------------------------+  |
|  |     StaticFileHandler      |  |          HealthHandler          |  |
|  |   (Serves frontend/ assets)|  |      (Serves /api/health)       |  |
|  +----------------------------+  +----------------+----------------+  |
|                                                   |                   |
|                                                   v                   |
|                                   +--------------------------------+  |
|                                   |         Database.java          |  |
|                                   |    (Loads db.properties & DB)  |  |
|                                   +---------------+----------------+  |
+---------------------------------------------------|-------------------+
                                                    | JDBC (MySQL Driver)
                                                    v
                                    +--------------------------------+  |
                                    |       MySQL Database (3306)    |  |
                                    |            (app_db)            |  |
                                    +--------------------------------+  |
```

---

## 5. Project Structure

Exact project file tree established in Phase 1:

```
C:\Users\ADMIN\Desktop\Project\
├── .gitignore
├── README.md
├── phase-01-boilerplate-foundation.md
├── config/
│   ├── db.properties.example
│   └── db.properties
├── database/
│   └── schema.sql
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── backend/
│   ├── lib/
│   │   └── mysql-connector-j.jar
│   ├── src/
│   │   └── com/example/app/
│   │       ├── Database.java
│   │       ├── HealthHandler.java
│   │       ├── StaticFileHandler.java
│   │       └── Server.java
│   └── test/
│       └── com/example/app/
│           ├── DatabaseTest.java
│           ├── HealthHandlerTest.java
│           └── StaticFileHandlerTest.java
└── bin/
    └── com/example/app/
        ├── Database.class
        ├── DatabaseTest.class
        ├── HealthHandler.class
        ├── HealthHandlerTest.class
        ├── Server.class
        ├── StaticFileHandler.class
        └── StaticFileHandlerTest.class
```

---

## 6. Implementation Journey

1. **Phase 1 — Project Foundation & Security Configuration**:
   * Created `.gitignore` to protect credentials (`config/db.properties`), bytecode (`*.class`, `bin/`), and IDE metadata.
   * Created `config/db.properties.example` as a version-controlled configuration template.
   * Created local `config/db.properties`.
   * Created `database/schema.sql` to initialize `app_db`.

2. **Phase 2 — Database Configuration & JDBC Layer**:
   * Resolved MySQL client pathing and PowerShell input redirection syntax.
   * Downloaded `mysql-connector-j-8.3.0.jar` into `backend/lib/mysql-connector-j.jar`.
   * Created `DatabaseTest.java` (TDD test runner) and `Database.java` (JDBC connection manager).
   * Verified JDBC database connectivity.

3. **Phase 3 — Backend HTTP Server & `/api/health` Endpoint**:
   * Created `HealthHandlerTest.java` to test `/api/health` HTTP 200 responses, `application/json` headers, JSON payload formatting, and HTTP 405 method restrictions.
   * Created `HealthHandler.java` implementing `com.sun.net.httpserver.HttpHandler`.
   * Created `Server.java` main entry point listening on port `8080`.
   * Verified `/api/health` returned `{"status":"UP","database":"CONNECTED"}`.

4. **Phase 4 — Static File Handler**:
   * Created `StaticFileHandlerTest.java` to test serving `index.html`, MIME type resolution, HTTP 404 missing file behavior, and HTTP 403 path traversal security.
   * Created `StaticFileHandler.java` implementing security path normalization (`targetPath.startsWith(basePath)`).
   * Updated `Server.java` to mount `StaticFileHandler` at `/`.

5. **Phase 5 — Frontend Landing Page**:
   * Created `frontend/index.html` with responsive layout, title, description, and status card.
   * Created `frontend/css/style.css` with clean modern styling and color badges.
   * Created `frontend/js/app.js` using Vanilla `fetch('/api/health')` to dynamically update system status badges.

6. **Phase 6 — Documentation & Final Verification**:
   * Created `README.md` containing build, configuration, startup instructions, and explicit scope boundaries.

---

## 7. Implemented Features

* **GET `/api/health` API**: Returns HTTP 200 OK with `Content-Type: application/json; charset=UTF-8` and JSON body `{"status":"UP","database":"CONNECTED"}` (or `DISCONNECTED`). Non-GET requests return HTTP 405 Method Not Allowed.
* **Static Asset Server**: Serves frontend files at `http://localhost:8080/`. Handles MIME types for HTML, CSS, JS, JSON, PNG, JPG, ICO.
* **Path Traversal Protection**: `StaticFileHandler` blocks requests containing `..` or attempting to access files outside the `frontend/` directory, returning HTTP 403.
* **JDBC Connectivity & Config**: Externalized configuration reading `db.url`, `db.user`, and `db.password` from `config/db.properties`.
* **Frontend Health UI**: Landing page displaying live backend server and database connection status with a manual refresh button.

---

## 8. Important Code and Configuration Behavior

### `Database.java`
* Class: `com.example.app.Database`
* Constructor: `public Database(String configPath)`
* Key methods: `getConnection()` (returns `java.sql.Connection`), `checkConnection()` (returns `boolean`).
* Uses `java.util.Properties` and `java.io.FileInputStream`.

### `HealthHandler.java`
* Class: `com.example.app.HealthHandler implements HttpHandler`
* Enforces HTTP GET method restriction (`exchange.sendResponseHeaders(405, -1)`).
* Formats JSON payload manually using `String.format`.

### `StaticFileHandler.java`
* Class: `com.example.app.StaticFileHandler implements HttpHandler`
* Path resolution: `Paths.get(baseDir).toAbsolutePath().normalize().resolve(requestPath.substring(1)).normalize()`.
* Path traversal validation: `if (!targetPath.startsWith(basePath))`.

---

## 9. Database

* **Database Name**: `app_db`
* **Character Set**: `utf8mb4`, Collation: `utf8mb4_unicode_ci`
* **Schema File**: `database/schema.sql`
* **Content**:
```sql
CREATE DATABASE IF NOT EXISTS app_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE app_db;
```
* **Tables Implemented**: **0 tables**. (No user, session, role, or application tables exist in Phase 1).

---

## 10. Authentication

* **Status**: **Explicitly NOT Implemented**.
* No registration, login, logout, password hashing, JWT, session, or cookie logic exists.

---

## 11. Commands and Operations

### Compilation Command (PowerShell)
```powershell
javac -d bin -cp "backend/lib/*" backend/src/com/example/app/*.java backend/test/com/example/app/*.java
```

### Running Test Suites
```powershell
java -cp "bin;backend/lib/*" com.example.app.DatabaseTest
java -cp "bin;backend/lib/*" com.example.app.HealthHandlerTest
java -cp "bin;backend/lib/*" com.example.app.StaticFileHandlerTest
```

### Starting Backend Server
```powershell
java -cp "bin;backend/lib/*" com.example.app.Server
```

### Database Initialization Command (PowerShell)
```powershell
Get-Content database/schema.sql | mysql -u root -p
```
*Or via CMD*:
```cmd
cmd /c "mysql -u root -p < database/schema.sql"
```

---

## 12. Tests and Verification

| Test Suite | Purpose / Scope | Result | Output Evidence |
| :--- | :--- | :--- | :--- |
| `DatabaseTest` | Config loading & JDBC connection | **PASSED** | `[PASS] Database configuration loaded successfully.`<br>`[PASS] Database connection verified successfully!` |
| `HealthHandlerTest` | HTTP 200, `application/json`, JSON payload, HTTP 405 restriction | **PASSED** | `[PASS] Health endpoint returned HTTP 200 OK with valid JSON: {"status":"UP","database":"CONNECTED"}`<br>`[PASS] Non-GET method correctly returned HTTP 405.` |
| `StaticFileHandlerTest` | Root GET `/` index serving, 404 missing files | **PASSED** | `[PASS] Root URL correctly serves index.html with HTTP 200.`<br>`[PASS] Missing file request correctly returns HTTP 404.` |

---

## 13. Failures, Root Causes, and Fixes

### 1. PowerShell Input Redirection Error (`<`)
* **Error**: `The '<' operator is reserved for future use.`
* **Root Cause**: PowerShell does not support `<` for piping files to command stdin.
* **Fix**: Used `Get-Content database/schema.sql | mysql -u root -p` or `cmd /c "mysql -u root -p < database/schema.sql"`.

### 2. MySQL Command Not Recognized
* **Error**: `The term 'mysql' is not recognized as the name of a cmdlet...`
* **Root Cause**: MySQL client was either not installed or not added to system `PATH`.
* **Fix**: Provided full path options (`C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`) and installation instructions.

### 3. `Invoke-WebRequest` DirectoryNotFoundException for `lib`
* **Error**: `Could not find a part of the path '.../backend/lib/mysql-connector-j.jar'`.
* **Root Cause**: `backend/lib` was accidentally created as a 0-byte file (`-a----`) instead of a folder (`d-----`).
* **Fix**: Removed file via `Remove-Item backend\lib -Force` and re-created folder via `New-Item -ItemType Directory -Path "backend\lib" -Force`.

### 4. Java Class Name Mismatch Compilation Error
* **Error**: `backend\test\com\example\app\DatabaseTest.java:3: error: class Database is public, should be declared in a file named Database.java`.
* **Root Cause**: Class inside `DatabaseTest.java` was accidentally declared as `public class Database`.
* **Fix**: Updated class declaration to `public class DatabaseTest`.

---

## 14. Important Architectural Decisions

* **Vanilla Standard Architecture**: Strictly no frameworks used. Ensures maximum portability, minimal footprint, and direct understanding of standard Java & Web APIs.
* **Single-Origin Deployment**: Frontend served directly by Java `HttpServer` via `StaticFileHandler`. Eliminates CORS headers and simplifies local development.
* **Externalized Credentials**: `config/db.properties` is ignored by Git, preventing secret exposure.

---

## 15. Dependencies and Versions

* **Java JDK**: 11+ (tested on Java 21 / Windows)
* **MySQL Server**: 8.0+
* **JDBC Driver**: `mysql-connector-j-8.3.0.jar` (Location: `backend/lib/mysql-connector-j.jar`)

---

## 16. Configuration and Environment

* **HTTP Port**: `8080`
* **Test Ports**: `8088`, `8089` (used during test runner execution)
* **Configuration File**: `config/db.properties`
* **Keys**:
  * `db.url`: `jdbc:mysql://localhost:3306/app_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC`
  * `db.user`: `root`
  * `db.password`: `<user_local_password>`

---

## 17. Security / Operational Considerations

* **Secrets Management**: `config/db.properties` is listed in `.gitignore`. `config/db.properties.example` contains dummy placeholder credentials.
* **Path Traversal**: `StaticFileHandler` normalizes paths and verifies `targetPath.startsWith(basePath)`.

---

## 18. Final Repository State

* All 4 backend classes (`Database`, `HealthHandler`, `StaticFileHandler`, `Server`) compiled cleanly in `bin/com/example/app/`.
* All 3 test classes (`DatabaseTest`, `HealthHandlerTest`, `StaticFileHandlerTest`) compiled and passed execution.
* Frontend files (`index.html`, `style.css`, `app.js`) verified and communicating with `/api/health`.

---

## 19. Deferred / Out-of-Scope Work

* User Authentication (Registration, Login, Logout, Sessions, JWT, Cookies).
* Database tables (`users`, `sessions`, `roles`).
* Domain-specific business logic and endpoints.

---

## 20. Known Limitations / Unresolved Questions

* **MySQL Server Runtime**: Local MySQL Server must be active for `DatabaseTest` and `/api/health` database check to return `CONNECTED`. If MySQL is stopped, `/api/health` returns HTTP 200 with `"database":"DISCONNECTED"`.

---

## 21. Git / Commit Information

* **Git Status**: The workspace directory `C:\Users\ADMIN\Desktop\Project` has **not** been initialized as a Git repository yet (`.git` directory does not exist).
* **Commit History**: No commits exist.
* **Action Item**: Initialize repository (`git init`) and create initial commit when ready.

---

## 22. Resume From Here

### Baseline Available Right Now
* The full-stack boilerplate is complete, compiled, tested, and ready.
* Server entry point: `com.example.app.Server` on port `8080`.
* Config file: `config/db.properties`.
* Database: `app_db`.

### Instructions for Next Phase Implementation Agent
1. **Do NOT rebuild** the Java HTTP Server, static file handler, database connection manager, or project structure.
2. **Preserve Constraints**:
   * Do NOT introduce Spring Boot, Hibernate, React, Vue, Angular, or CSS frameworks unless explicitly instructed by the user.
   * Maintain zero hardcoded credentials in Java files.
3. **Next Steps for Future Phases**:
   * Build authentication database schema (`users` table, etc.) in `database/schema.sql` or migration scripts.
   * Implement authentication endpoints (e.g. `POST /api/auth/register`, `POST /api/auth/login`) in `com.example.app`.
   * Add password hashing (e.g. PBKDF2 / SHA-256 with salt in standard JDK `java.security`).
   * Add frontend authentication forms and session token storage.
