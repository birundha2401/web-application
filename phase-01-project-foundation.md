# Phase 1 — Project Foundation & Web Application Boilerplate Context

## 1. Phase Objective and Scope

### Objective
Establish a clean, robust, and extensible full-stack foundation for a domain-independent web application using **strictly Vanilla Java and Web standards without third-party frameworks**. 

This foundation acts as a lightweight, framework-free baseline designed to support upcoming iterations (such as authentication and domain-specific business features) without assuming or locking into any specific application domain upfront.

### Scope Boundaries for Step 1
* **In Scope**:
  * Project directory structure and Git environment configuration (`.gitignore`).
  * Configuration management loader (`config/db.properties.example` and `config/db.properties`).
  * MySQL database initialization script (`database/schema.sql`).
  * JDBC connection manager (`Database.java`) using the official MySQL Connector/J driver.
  * Standalone Java HTTP Server (`com.sun.net.httpserver.HttpServer`) listening on port `8080`.
  * Core JSON health check endpoint (`GET /api/health`) returning server status and live JDBC database connectivity.
  * Static file HTTP handler (`StaticFileHandler.java`) serving frontend assets with MIME type resolution and path traversal protection.
  * Vanilla frontend landing page (`index.html`, `style.css`, `app.js`) rendering live system health badges with dynamic refresh capability.
  * Test-Driven Development (TDD) verification test runners (`DatabaseTest.java`, `HealthHandlerTest.java`, `StaticFileHandlerTest.java`).
  * Project documentation (`README.md`).
* **Explicitly Excluded from Step 1**:
  * User registration, login, logout, and password management.
  * Cryptographic password hashing (BCrypt, PBKDF2, Argon2, etc.).
  * Session management, cookies, OAuth, or JSON Web Tokens (JWT).
  * Database user tables (`users`), role tables, permission tables, or session tables.
  * Domain-specific business logic or data entities.
  * Third-party web, ORM, or testing frameworks (Spring, Hibernate, Express, React, etc.).

---

## 2. Starting State and Initial Requirements

* **Initial Workspace State**: The workspace at `C:\Users\ADMIN\Desktop\Project` was initially empty.
* **Operating System**: Windows 11 with PowerShell shell environment.
* **Core Runtime Requirements**:
  * Java Development Kit (JDK 11+; specifically compiled/tested with Java 17 / OpenLogic JDK 17).
  * MySQL Server 8.0+ running on `localhost:3306`.
  * Standalone MySQL JDBC driver JAR (`mysql-connector-j-8.3.0.jar`).
* **Design Requirements**:
  1. No external application frameworks (no Spring Boot, Jakarta EE, or MicroProfile).
  2. Zero hardcoded database credentials in Java source code.
  3. Single-origin architecture (the Java HTTP server serves both the static web frontend and API endpoints to prevent CORS issues).
  4. Explicit error handling and fail-safe behavior when the database is unavailable.

---

## 3. Final Implementation Outcome

Step 1 was successfully implemented, verified, and captured in Git commit `4c1ffb7` (*"1st commit"*).

The outcome delivered:
1. A fully functioning, single-port (`8080`) Java HTTP server.
2. An automated `GET /api/health` JSON API verifying backend responsiveness and live database pinging.
3. A safe static asset server serving HTML, CSS, JavaScript, and images with directory-traversal protection.
4. A responsive, modern frontend UI displaying live status indicators for the backend server and database.
5. Externalized configuration isolating database credentials from version control.
6. A verified suite of standalone TDD integration tests executing via standard Java without requiring external test runners.

---

## 4. Implementation Journey in Chronological Order

The development of Step 1 was executed in 6 distinct phases:

1. **Phase 1: Project Foundation & Security Configuration**
   * Configured `.gitignore` to prevent sensitive credentials (`config/db.properties`), compiled bytecode (`*.class`, `bin/`), and editor metadata (`.vscode/`, `.idea/`) from entering Git.
   * Established `config/db.properties.example` as a version-controlled configuration template.
   * Created local `config/db.properties` with database connection keys.
   * Created `database/schema.sql` to define the database character set and collation.

2. **Phase 2: Database Configuration & JDBC Layer (TDD)**
   * Set up MySQL client access and established the `app_db` database in MySQL.
   * Acquired `mysql-connector-j-8.3.0.jar` and placed it into `backend/lib/`.
   * Wrote `DatabaseTest.java` to test configuration parsing and JDBC connection validation.
   * Implemented `Database.java` using `java.util.Properties` and `java.sql.DriverManager`.
   * Verified successful database connection test execution.

3. **Phase 3: Backend HTTP Server & Health Check API (TDD)**
   * Wrote `HealthHandlerTest.java` to assert HTTP 200 response codes, `application/json` Content-Type headers, JSON payload structure, and rejection of non-GET methods with HTTP 405.
   * Implemented `HealthHandler.java` implementing `com.sun.net.httpserver.HttpHandler`.
   * Created `Server.java` entry point, configuring port `8080` and registering `/api/health`.
   * Verified that requests to `/api/health` returned `{"status":"UP","database":"CONNECTED"}`.

4. **Phase 4: Static File Serving & Path Security (TDD)**
   * Wrote `StaticFileHandlerTest.java` to assert serving of default `index.html`, correct MIME types, HTTP 404 for missing files, and path validation.
   * Implemented `StaticFileHandler.java` with path normalization (`Path.normalize()`) and prefix verification (`targetPath.startsWith(basePath)`) to prevent directory traversal attacks (`../`).
   * Registered `StaticFileHandler` at root path `/` in `Server.java`.

5. **Phase 5: Frontend Landing Page & Health Dashboard**
   * Built `frontend/index.html` with a card-based responsive layout, title, description, and status indicator elements.
   * Created `frontend/css/style.css` defining CSS custom styling, modern typography, container layout, and color-coded status badges (`badge-success`, `badge-danger`, `badge-pending`).
   * Implemented `frontend/js/app.js` using the standard `fetch()` API to query `/api/health` upon page load and on manual button refresh.

6. **Phase 6: Project Documentation & Verification**
   * Created `README.md` providing prerequisites, setup instructions, compilation commands, and execution steps.
   * Compiled all classes into `bin/` and verified full end-to-end operation in the browser.

---

## 5. Final Project Directory Structure (Step 1 Baseline)

At the completion of Step 1 (commit `4c1ffb7`), the repository structure was organized as follows:

```text
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

> **Note on Evolutionary Changes:** In subsequent phases (Step 2 & Step 3), the build mechanism transitioned from manual `javac` with `backend/lib/` to Gradle (`build.gradle` and the Gradle wrapper). The legacy `backend/lib/` JAR and `bin/` folder were superseded by Gradle's automated dependency cache and `build/` directory.

---

## 6. Important Files and Their Responsibilities

| File Path | Component | Responsibility |
|:---|:---|:---|
| `.gitignore` | Configuration | Excludes sensitive credentials (`config/db.properties`), build artifacts (`bin/`, `build/`, `*.class`), and IDE metadata. |
| `config/db.properties.example` | Configuration | Version-controlled template showing required database property keys without revealing real secrets. |
| `config/db.properties` | Configuration | Local, git-ignored configuration containing active database URL, username, and password. |
| `database/schema.sql` | Database | DDL script to create the `app_db` database with `utf8mb4` character set. |
| `backend/src/com/example/app/Database.java` | Backend (JDBC) | Reads database properties, establishes JDBC connections, and provides a health verification ping. |
| `backend/src/com/example/app/HealthHandler.java` | Backend (API) | Handles `GET /api/health`, returning JSON representing application and database status. |
| `backend/src/com/example/app/StaticFileHandler.java` | Backend (Web) | Serves static assets from `frontend/`, determines MIME types, and prevents directory traversal attacks. |
| `backend/src/com/example/app/Server.java` | Backend (Core) | Main entry point; initializes `Database`, instantiates `HttpServer`, mounts routes, and binds to port `8080`. |
| `backend/test/com/example/app/DatabaseTest.java` | Testing | Standalone test runner verifying configuration loading and live JDBC connectivity. |
| `backend/test/com/example/app/HealthHandlerTest.java` | Testing | Starts a temporary test HTTP server (port 8089) and asserts `/api/health` status, headers, and payload. |
| `backend/test/com/example/app/StaticFileHandlerTest.java` | Testing | Starts a temporary test HTTP server (port 8088) and asserts static file delivery and HTTP 404 responses. |
| `frontend/index.html` | Frontend | Single-page UI containing the health dashboard, status grid, and refresh trigger. |
| `frontend/css/style.css` | Frontend | Clean responsive stylesheet specifying typography, card containers, and color-coded status badges. |
| `frontend/js/app.js` | Frontend | Vanilla JavaScript invoking `/api/health` via `fetch()` and dynamically updating DOM badge classes and text. |
| `README.md` | Documentation | High-level overview, prerequisites, build instructions, and operational commands. |

---

## 7. Frontend Implementation Details

### HTML Architecture (`frontend/index.html`)
* Standard HTML5 document structure with responsive viewport configuration (`<meta name="viewport" content="width=device-width, initial-scale=1.0">`).
* Linked to `css/style.css` in the `<head>` and `js/app.js` at the bottom of the `<body>` to ensure non-blocking rendering.
* Structured around a centralized `.container` holding:
  1. `<header class="header">`: Displays application title and architectural subtitle.
  2. `<main class="main-content">`: Houses the `status-card` containing a flexbox status grid (`.status-grid`).
  3. Status Items: Dedicated target spans for dynamic injection (`#backend-status`, `#db-status`, `#last-checked`).
  4. Action Button: `#refresh-btn` wired to trigger `checkHealth()`.
  5. Foundation Information Card: Outlines the extensible boilerplate philosophy.
  6. `<footer>`: Architectural credits.

### Styling Architecture (`frontend/css/style.css`)
* Implements a modern CSS reset (`box-sizing: border-box`, zero margin/padding).
* System font stack prioritizing performance and cross-platform native rendering (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto...`).
* Subtle slate palette: Dark slate headers (`#1e293b`), neutral light backgrounds (`#f4f6f9`, `#f8fafc`), and distinct status badge indicators:
  * `.badge-success`: Light green background (`#dcfce7`) with dark green text (`#166534`).
  * `.badge-danger`: Light red background (`#fee2e2`) with dark red text (`#991b1b`).
  * `.badge-pending`: Light amber background (`#fef3c7`) with dark amber text (`#92400e`).

### JavaScript Logic (`frontend/js/app.js`)
* Executes automatically upon page load via `document.addEventListener('DOMContentLoaded', ...)`.
* Function `checkHealth()`:
  1. Immediately sets both badges to "Checking..." (`badge-pending`) for immediate visual feedback.
  2. Dispatches asynchronous `fetch('/api/health')` request to the same origin.
  3. Verifies `response.ok`; throws an error if status is non-2xx.
  4. Parses the JSON body and applies conditional DOM updates:
     * If `data.status === 'UP'`, updates `#backend-status` to `"Online - UP"` with `badge-success`.
     * If `data.database === 'CONNECTED'`, updates `#db-status` to `"CONNECTED"` with `badge-success`.
     * Otherwise, applies `badge-danger` and failure labels.
  5. Catches network failures (e.g. backend offline) gracefully, marking backend status as `"Offline / Error"` and database as `"Unavailable"`.
  6. Updates `#last-checked` with the local timestamp via `new Date().toLocaleTimeString()`.

---

## 8. Java Backend Implementation Details

### Server Initialization (`backend/src/com/example/app/Server.java`)
* Entry point method: `public static void main(String[] args)`.
* Default listen port: `8080` (`private static final int PORT = 8080;`).
* Creates the built-in HTTP server instance:
  ```java
  HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
  ```
  The second argument (`backlog = 0`) delegates system socket queue sizing to system defaults.
* Instantiates `Database` loading configuration from `config/db.properties`.
* Registers request handlers with the server instance:
  ```java
  server.createContext("/api/health", new HealthHandler(db));
  server.createContext("/", new StaticFileHandler("frontend"));
  ```
* Sets default executor: `server.setExecutor(null);` (uses the default single-threaded dispatching model within the server).
* Prints an informative terminal banner detailing listening URLs.
* Starts socket listening via `server.start();`.

---

## 9. HTTP Server, Handlers, and Endpoints

### 1. Health Check Endpoint (`HealthHandler.java`)
* **Context Path**: `/api/health`
* **Allowed HTTP Method**: Strictly `GET`. Any other method triggers:
  ```java
  exchange.sendResponseHeaders(405, -1); // 405 Method Not Allowed
  ```
* **Database Verification**: Calls `db.checkConnection()`.
* **Response Payload Generation**: Formats JSON without third-party serializers:
  ```java
  String jsonResponse = String.format("{\"status\":\"UP\",\"database\":\"%s\"}", dbStatus);
  ```
* **Headers**: Sets `Content-Type: application/json; charset=UTF-8`.
* **Status Code**: Returns HTTP `200 OK` (even if database is DISCONNECTED, allowing the frontend to distinguish between server health and database status).

### 2. Static File Handler (`StaticFileHandler.java`)
* **Context Path**: `/` (root fallback)
* **Allowed HTTP Method**: Strictly `GET`. Other methods return `405 Method Not Allowed`.
* **Default Page Mapping**: If path is `/` or empty, resolves to `/index.html`.
* **Path Traversal Security**:
  ```java
  Path basePath = Paths.get(baseDir).toAbsolutePath().normalize();
  Path targetPath = basePath.resolve(requestPath.substring(1)).normalize();
  if (!targetPath.startsWith(basePath)) {
      sendResponse(exchange, 403, "403 Forbidden", "text/plain");
      return;
  }
  ```
  Any request attempting to traverse out of the base directory via `../` is intercepted and rejected with HTTP `403 Forbidden`.
* **File Existence Check**: If the target file does not exist or is a directory, returns HTTP `404 Not Found`.
* **MIME Type Mapping**:
  * `.html`, `.htm` → `text/html; charset=UTF-8`
  * `.css` → `text/css; charset=UTF-8`
  * `.js` → `application/javascript; charset=UTF-8`
  * `.json` → `application/json; charset=UTF-8`
  * `.png` → `image/png`
  * `.jpg`, `.jpeg` → `image/jpeg`
  * `.ico` → `image/x-icon`
  * Fallback → `application/octet-stream`
* **Streaming Delivery**: Streams file bytes using a 4KB buffer (`byte[4096]`) to optimize memory consumption.

---

## 10. MySQL and JDBC Implementation

### Database Configuration (`Database.java`)
* **Class**: `com.example.app.Database`
* **Constructor**: `public Database(String configPath)`
* **Configuration Loading**: Uses standard `java.util.Properties` loaded via `FileInputStream(configPath)`:
  * Key `db.url`: JDBC connection string.
  * Key `db.user`: MySQL database user.
  * Key `db.password`: MySQL database user password.
* **Connection Provider**:
  ```java
  public Connection getConnection() throws SQLException {
      if (url == null || url.isEmpty()) {
          throw new SQLException("Database URL is not configured");
      }
      return DriverManager.getConnection(url, user, password);
  }
  ```
* **Liveness Check**:
  ```java
  public boolean checkConnection() {
      try (Connection conn = getConnection()) {
          return conn != null && !conn.isClosed();
      } catch (SQLException e) {
          return false;
      }
  }
  ```

### Database Initialization Script (`database/schema.sql`)
The initial schema file established in Step 1 strictly creates the database envelope without application tables:
```sql
-- Initial Database Creation Script
CREATE DATABASE IF NOT EXISTS app_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE app_db;
```
* **Database Name**: `app_db`
* **Character Encoding**: `utf8mb4` (full 4-byte UTF-8 support including international characters and emojis).
* **Collation**: `utf8mb4_unicode_ci`.
* **Tables in Step 1**: Exactly **0 tables**. (User and domain tables were intentionally deferred to subsequent steps).

---

## 11. Configuration and Dependency Details

### Runtime & Configuration Keys
* **Configuration File**: `config/db.properties`
* **Active Keys**:
  * `db.url`: `jdbc:mysql://localhost:3306/app_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC`
  * `db.user`: `root`
  * `db.password`: `<configured_local_password>`
* **Server Port**: `8080`
* **Test Ports**: `8088` (`StaticFileHandlerTest`), `8089` (`HealthHandlerTest`)

### Dependencies
* **JDK Version**: OpenLogic OpenJDK 17 (`17.0.15+6`) / Java 11+ compatible.
* **MySQL JDBC Driver**: `com.mysql:mysql-connector-j:8.3.0` (originally placed in `backend/lib/mysql-connector-j.jar`).
* **External Frameworks**: None. All HTTP server, file handling, and serialization code relies strictly on built-in Java standard library packages:
  * `com.sun.net.httpserver.*`
  * `java.net.*`
  * `java.io.*`
  * `java.nio.file.*`
  * `java.sql.*`
  * `java.util.*`

---

## 12. Important Commands and Operational Instructions

### Step 1 Native Compilation (Manual `javac`)
```powershell
# Compile production source code and test runners
javac -d bin -cp "backend/lib/*" backend/src/com/example/app/*.java backend/test/com/example/app/*.java
```

### Running Step 1 Automated TDD Tests
```powershell
# Execute DatabaseTest
java -cp "bin;backend/lib/*" com.example.app.DatabaseTest

# Execute HealthHandlerTest
java -cp "bin;backend/lib/*" com.example.app.HealthHandlerTest

# Execute StaticFileHandlerTest
java -cp "bin;backend/lib/*" com.example.app.StaticFileHandlerTest
```

### Executing Step 1 Production Server
```powershell
java -cp "bin;backend/lib/*" com.example.app.Server
```

### Modern Equivalent (Using Gradle Wrapper)
```powershell
# Build and execute all tests
.\gradlew test

# Start the application server
.\gradlew run
```

### Database Initialization Command
```powershell
# Execute schema.sql against local MySQL server
Get-Content database/schema.sql | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

---

## 13. Tests and Verification Results

All three original test suites for Step 1 were executed and passed during implementation:

| Test Suite | Purpose / Scope | Execution Method | Observed Result | Evidence / Log Output |
|:---|:---|:---|:---|:---|
| `DatabaseTest` | Config file parsing & JDBC connection test | Standalone `main()` | **PASSED** | `[PASS] Database configuration loaded successfully.`<br>`[PASS] Database connection verified successfully!` |
| `HealthHandlerTest` | HTTP 200, `application/json`, payload validation, HTTP 405 rejection | Embedded `HttpServer` (Port 8089) | **PASSED** | `[PASS] Health endpoint returned HTTP 200 OK with valid JSON: {"status":"UP","database":"CONNECTED"}`<br>`[PASS] Non-GET method correctly returned HTTP 405.` |
| `StaticFileHandlerTest` | Root `/` index serving, 404 missing files, Content-Type headers | Embedded `HttpServer` (Port 8088) | **PASSED** | `[PASS] Root URL correctly serves index.html with HTTP 200.`<br>`[PASS] Missing file request correctly returns HTTP 404.` |

---

## 14. Errors, Debugging Attempts, and Fixes During Step 1

During the initial Step 1 implementation, several operational hurdles were diagnosed and resolved:

### 1. PowerShell Input Redirection Syntax Error (`<`)
* **Error**: `The '<' operator is reserved for future use.`
* **Cause**: PowerShell syntax does not support the CMD-style `<` standard input redirection operator.
* **Resolution**: Replaced command with PowerShell pipeline syntax: `Get-Content database/schema.sql | mysql -u root -p` (or `cmd /c "mysql -u root -p < database/schema.sql"`).

### 2. MySQL Command Not Recognized in PATH
* **Error**: `The term 'mysql' is not recognized as the name of a cmdlet, function, script file, or operable program.`
* **Cause**: MySQL Server was installed, but its `bin` directory (`C:\Program Files\MySQL\MySQL Server 8.0\bin`) was not present in the system environment `PATH`.
* **Resolution**: Invoked the client directly using its full path: `& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"`.

### 3. Directory vs File Collision on `backend/lib`
* **Error**: `Could not find a part of the path '.../backend/lib/mysql-connector-j.jar'`.
* **Cause**: An automated download command created a 0-byte file named `backend/lib` instead of creating `backend/lib/` as a directory.
* **Resolution**: Removed the erroneous file (`Remove-Item backend\lib -Force`) and recreated it explicitly as a directory (`New-Item -ItemType Directory -Path backend\lib`).

### 4. Java Class Declaration Nismatch
* **Error**: `backend\test\com\example\app\DatabaseTest.java:3: error: class Database is public, should be declared in a file named Database.java`.
* **Cause**: A copy-paste error inside `DatabaseTest.java` named the public class `Database` instead of `DatabaseTest`.
* **Resolution**: Renamed class declaration to `public class DatabaseTest`.

---

## 15. Architectural Decisions and Rationale

1. **Framework-Free Java (`com.sun.net.httpserver`)**
   * *Rationale*: Built directly into standard Java runtime. Eliminates heavyweight dependencies (like Spring Boot with hundreds of transitive JARs), reduces startup time to under 1 second, and provides a clear, transparent mental model for request/response handling.
2. **Single-Origin Deployment**
   * *Rationale*: Serving static HTML/CSS/JS assets directly from the same Java HTTP server on port `8080` removes the need for CORS headers, proxy configurations, or separate Node.js development servers.
3. **Pure JDBC over ORM**
   * *Rationale*: Frameworks like Hibernate/JPA introduce significant configuration overhead, caching anomalies, and abstraction layers. Plain JDBC with explicit `PreparedStatement` usage provides transparent query execution and optimal performance.
4. **Externalized Credentials via `.properties`**
   * *Rationale*: Keeps database credentials strictly out of version control by ignoring `config/db.properties` in Git, while providing `config/db.properties.example` for developers to set up their own environments.
5. **Path Traversal Security by Design**
   * *Rationale*: Custom static file servers are notoriously vulnerable to `../` path traversal attacks. Implementing strict path normalization (`toAbsolutePath().normalize()`) and prefix boundary validation (`targetPath.startsWith(basePath)`) prevents access to system or sensitive application files.

---

## 16. Security Considerations

* **Credential Protection**: Real passwords never exist in committed files. `config/db.properties` is explicitly listed in `.gitignore`.
* **Directory Traversal Protection**: Implemented in `StaticFileHandler` line 35. Requests attempting to escape `frontend/` are rejected with HTTP 403 Forbidden.
* **Resource Leak Prevention**: All database connections and file input/output streams use Java's `try-with-resources` construct to guarantee immediate socket and file descriptor cleanup.
* **Safe Health Probing**: The `/api/health` check only indicates `"CONNECTED"` or `"DISCONNECTED"` without exposing database table names, hostnames, usernames, or internal stack traces to the public web client.

---

## 17. Known Limitations and Unresolved Issues in Step 1

* **Single-Threaded Default Executor**: `server.setExecutor(null)` runs requests synchronously. For high-concurrency production workloads, a thread pool executor (`Executors.newFixedThreadPool(...)`) would be required.
* **Manual MIME Type Mapping**: `StaticFileHandler` uses an explicit `if-else` map for common extensions. Unrecognized file extensions fall back to `application/octet-stream`.
* **Database Dependency for Health Status**: The health check endpoint requires the local MySQL daemon to be running. If MySQL is stopped, `/api/health` gracefully returns `"database":"DISCONNECTED"`.

---

## 18. Features Explicitly Excluded from Step 1

To maintain strict architectural boundaries, the following capabilities were deliberately excluded from Step 1:
* User registration (`/api/register`, registration form, user entity).
* User login and authentication (`/api/login`, login form, session validation).
* Password hashing and credential storage.
* Session tokens, JWT, cookies, or authorization headers.
* Database tables (`users`, `roles`, `permissions`, `sessions`).
* Application business workflows.

---

## 19. Git Branch, Commit Information, and Working-Tree Status

* **Branch**: `main` (synchronized with `origin/main`).
* **Commit Tracking for Step 1**:
  * **Commit Hash**: `4c1ffb72f1a71370e557f60b266213925035560f`
  * **Commit Message**: `1st commit`
  * **Commit Date**: `Wed Oct 7 22:34:39 2026 +0530`
  * **Author**: `birundha-kprcas <birundha2426@gmail.com>`
* **Subsequent Evolution**:
  * `106c4ed` (*"commit2"*): Added Step 2 (User Registration, `users` table in `schema.sql`, PBKDF2 hashing, Gradle setup) and deleted the original `phase-01-boilerplate-foundation.md`.
  * `71f62c1` (*"2ndcommmit"*): Added Step 3 (Login feature, BCrypt password hashing, Gradle wrapper).
* **Current Working-Tree Status**:
  * Clean regarding code changes; several legacy files from prior presentation/data experiments remain unstaged or deleted.

---

## 20. Resume-From-Here: Exact Final State of Step 1

If checking out or resetting to the end of Step 1 (`git checkout 4c1ffb7`), the developer is equipped with:
1. **Compilable Backend**: 4 Java source classes in `backend/src/com/example/app/` (`Server`, `Database`, `HealthHandler`, `StaticFileHandler`).
2. **Passing Test Suites**: 3 standalone test runners in `backend/test/com/example/app/` (`DatabaseTest`, `HealthHandlerTest`, `StaticFileHandlerTest`).
3. **Frontend Dashboard**: 3 static frontend assets in `frontend/` (`index.html`, `style.css`, `app.js`).
4. **Database Envelope**: Schema script in `database/schema.sql` creating `app_db`.
5. **Configuration**: `config/db.properties` template and local configuration.
6. **Next Logical Step**: Implementation of user data storage and registration (Phase 2), without needing to rewrite any of the server, routing, database management, or static asset delivery infrastructure.
