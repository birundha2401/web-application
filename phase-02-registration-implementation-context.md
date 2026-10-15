# Phase 2 — User Registration: Implementation Context & Handoff

## 1. Phase Overview

### Objective
Design, implement, and verify an end-to-end **User Registration** feature for the web application boilerplate. The implementation extends the framework-free, single-origin architecture established in Step 1 to allow new users to register their details securely from a web form through to persistent MySQL storage.

### Requirements & Scope Boundaries
* **Required Input Fields**:
  1. Full Name (`name`, text)
  2. Phone Number (`phone`, tel)
  3. Email Address (`email`, email)
  4. Password (`password`, password)
* **Frontend Requirements**:
  * Clean, accessible HTML5 registration form (`frontend/register.html`).
  * Reusable CSS matching the existing typography, container, and badge design (`frontend/css/style.css`).
  * Vanilla JavaScript client (`frontend/js/register.js`) intercepting standard form submission with `event.preventDefault()`.
  * Client-side validation ensuring all 4 required fields are filled.
  * Asynchronous `fetch()` call targeting `POST /api/register` sending an `application/json` payload.
  * Inline visual feedback displaying green success alerts or red error alerts without page refreshes.
* **Backend API Requirements**:
  * Expose `POST /api/register` on the Java `HttpServer`.
  * Validate HTTP request method (`POST` only; others return `405 Method Not Allowed`).
  * Parse incoming JSON request body.
  * Perform server-side validation: reject payloads missing any of the 4 required fields with HTTP `400 Bad Request`.
  * Securely hash the plaintext password using **BCrypt** with salt before persistence.
  * Return HTTP `201 Created` with a confirmation message upon successful registration.
* **Database & Persistence Requirements**:
  * Expand `database/schema.sql` to include a `users` table with primary key `id`, `name`, `phone`, `email`, and `password`.
  * Enforce email uniqueness at the database engine level via a `UNIQUE` constraint on the `email` column.
  * Execute inserts using parameterized JDBC `PreparedStatement` to prevent SQL injection.
  * Catch database duplicate key violations (`SQLException`) and translate them cleanly to HTTP `409 Conflict`.
* **Explicitly Deferred / Out of Scope for Step 2**:
  * User login, session creation, cookies, or JWT tokens.
  * User logout or session revocation.
  * Password reset, email verification, or multi-factor authentication (MFA).
  * Role-based access control (RBAC), user profiles, or admin panels.

---

## 2. Starting State

Before the execution of Step 2, the repository was in the state established at the end of Step 1 (commit `4c1ffb7`):
* **HTTP Server**: Java built-in `HttpServer` listening on port `8080`, hosting `GET /api/health` and serving static files from `frontend/` at `/`.
* **Database**: MySQL `app_db` database initialized with zero tables.
* **Build System**: Plain `javac` compilation targeting `bin/` with MySQL Connector/J manually placed in `backend/lib/mysql-connector-j.jar`.
* **Frontend**: Basic landing page (`index.html`) displaying system health status.

---

## 3. Final Outcome

The user registration feature was fully built, debugged, and verified from the browser form down to MySQL.

### Summary of What Was Delivered and Verified
1. **Database Schema**: A relational `users` table initialized with an auto-incrementing primary key, UTF-8 character encoding, and a `UNIQUE` constraint on `email`.
2. **Domain & Data Access Layer**: `User.java` domain model and `UserRepository.java` executing parameterized `INSERT` queries.
3. **Password Security**: Cryptographic hashing via `org.mindrot:jbcrypt:0.4` with cost factor 12. Plaintext passwords are never stored, logged, or returned in API responses.
4. **Registration HTTP Handler**: `RegisterHandler.java` handling `POST /api/register`, validating fields, and dispatching HTTP `201`, `400`, `405`, or `409`.
5. **Modernized Build System**: Transitioned from manual JAR copying in `backend/lib/` to Gradle (`build.gradle`, `settings.gradle`, and the `gradlew` wrapper).
6. **Frontend UI**: Responsive registration page (`register.html`) with form validation and dynamic message banners (`register.js`).
7. **End-to-End Verification**: Achieved a 100% **COMPLETE** verdict across all 18 criteria of the strict architectural verification audit.

---

## 4. Implementation Journey & Debugging History

The implementation progressed through distinct development steps, resolving several technical challenges along the way:

### 1. Database Schema Creation
* Added the `users` table definition to `database/schema.sql`:
  ```sql
  CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      phone VARCHAR(50) NOT NULL,
      email VARCHAR(255) NOT NULL UNIQUE,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
* Executed the script against local MySQL Server 8.0 in `app_db`.

### 2. Domain Model & Repository (TDD)
* Created `backend/src/com/example/app/User.java` to encapsulate `id`, `name`, `phone`, `email`, and `password`.
* Created `backend/src/com/example/app/UserRepository.java` with method `saveUser(User user)`.
* Created `backend/test/com/example/app/UserRepositoryTest.java` verifying that:
  * A valid user is inserted into `users` successfully.
  * Inserting a duplicate email triggers an `SQLException` with `"Duplicate entry"`.

### 3. Password Hashing & The BCrypt Migration
* **Initial Implementation**: `PasswordHash.java` was initially written using standard Java JDK libraries implementing `PBKDF2WithHmacSHA256` (65,536 iterations, 256-bit key length, 16-byte random salt).
* **Verification Audit Finding**: The final architectural specification explicitly mandated **BCrypt** hashing (`org.mindrot:jbcrypt`), noting: *"The project uses PBKDF2 instead of BCrypt. Thus, BCrypt dependency and BCrypt hashing are definitively MISSING"*.
* **Resolution**:
  * Updated `build.gradle` dependencies to include `implementation 'org.mindrot:jbcrypt:0.4'`.
  * Refactored `PasswordHash.java` to use `BCrypt.hashpw(password, BCrypt.gensalt(12))` and `BCrypt.checkpw(password, storedHash)`.
  * Purged all existing test database records created during the PBKDF2 phase (`DELETE FROM app_db.users;`) to ensure all stored hashes in the database adhere to the standard `$2a$12$` BCrypt format.

### 4. HTTP API Endpoint Implementation
* Created `backend/src/com/example/app/RegisterHandler.java` implementing `com.sun.net.httpserver.HttpHandler`.
* Used regex-based string extraction (`extractJsonValue`) to avoid adding bulky JSON serialization libraries.
* Registered the endpoint in `backend/src/com/example/app/Server.java`:
  ```java
  server.createContext("/api/register", new RegisterHandler(db));
  ```
* Created `RegisterHandlerTest.java` asserting HTTP 201 on success, HTTP 409 on duplicate email, and HTTP 400 on missing required fields.

### 5. Frontend Registration Interface
* Created `frontend/register.html` including Name, Phone, Email, and Password inputs with HTML5 `required` constraints.
* Created `frontend/js/register.js` to handle form submission asynchronously, send JSON to `/api/register`, and display success or error banners.
* Updated `frontend/css/style.css` with card styles, form group controls, button utilities, and alert boxes (`.message.success`, `.message.error`).

### 6. Build Tooling Transition to Gradle
* Transitioned the project from raw `javac` compilation to Gradle to automate dependency resolution (e.g. `mysql-connector-j` and `jbcrypt`).
* **Encountered Issue 1 — Windows File Locking on JAR Deletion**:
  * When running `Remove-Item -Recurse -Force backend\lib`, PowerShell returned `IOException: The process cannot access the file 'mysql-connector-j.jar' because it is being used by another process`.
  * *Root Cause*: An active Java server background process was holding an open handle to the JAR.
  * *Fix*: Terminated the active background Java process before removing the directory.
* **Encountered Issue 2 — Missing Winget Package**:
  * The user attempted `winget install gradle` and `winget install Gradle.Gradle`, both returning `No package found matching input criteria`.
  * *Fix*: Bypassed global system installation by generating and using the project-local Gradle wrapper (`gradle wrapper`), producing `gradlew` and `gradlew.bat`.

---

## 5. Files and Components

### Files Created in Step 2
| File Path | Component | Responsibility |
|:---|:---|:---|
| `backend/src/com/example/app/User.java` | Backend (Model) | User entity representing database table columns. |
| `backend/src/com/example/app/UserRepository.java` | Backend (DAO) | JDBC repository performing parameterized inserts into `users`. |
| `backend/src/com/example/app/PasswordHash.java` | Backend (Security) | Hashes passwords with BCrypt (cost factor 12) and verifies hashes. |
| `backend/src/com/example/app/RegisterHandler.java` | Backend (API) | Handles `POST /api/register`, validates inputs, handles duplicate errors. |
| `backend/test/com/example/app/PasswordHashTest.java` | Test | Unit tests verifying salt uniqueness and password verification. |
| `backend/test/com/example/app/UserRepositoryTest.java` | Test | Integration test for user persistence and duplicate email constraints. |
| `backend/test/com/example/app/RegisterHandlerTest.java` | Test | Integration test for HTTP 201, 400, and 409 status responses. |
| `frontend/register.html` | Frontend | HTML5 registration form with input fields for Name, Phone, Email, Password. |
| `frontend/js/register.js` | Frontend | Form event listener, JSON serializer, fetch dispatcher, and DOM updater. |
| `build.gradle` | Build | Gradle build script managing dependencies and application execution. |
| `settings.gradle` | Build | Declares the project root name. |
| `gradlew` / `gradlew.bat` | Build | Cross-platform Gradle wrapper scripts. |

### Files Modified in Step 2
| File Path | Changes Made |
|:---|:---|
| `database/schema.sql` | Added `CREATE TABLE IF NOT EXISTS users (...)` with `UNIQUE (email)`. |
| `backend/src/com/example/app/Server.java` | Added `server.createContext("/api/register", new RegisterHandler(db));`. |
| `frontend/css/style.css` | Appended styles for `.form-container`, `.form-group`, `.btn-full`, `.message.success`, and `.message.error`. |

---

## 6. Technical Architecture

### Complete Data Flow Diagram
```text
HTML Registration Form (register.html)
        ↓
CSS Styling (style.css)
        ↓
Vanilla JavaScript (register.js)
        ↓  fetch() with JSON payload
HTTP POST /api/register
        ↓
Java HttpServer (Server.java:19)
        ↓
RegisterHandler (RegisterHandler.java)
        ↓  Server-side Validation (non-null check)
BCrypt Password Hashing (PasswordHash.java)
        ↓  BCrypt.hashpw(password, gensalt(12))
UserRepository (UserRepository.java)
        ↓  PreparedStatement.setString(...)
JDBC Connection (Database.java)
        ↓  mysql-connector-j 8.3.0
MySQL Database (app_db)
        ↓
users Table (schema.sql)
```

### Component Contracts & Responsibilities

#### 1. Frontend Contract (`register.js`)
* Form submission dispatches:
  * **Method**: `POST`
  * **Header**: `Content-Type: application/json`
  * **Body**:
    ```json
    {
      "name": "John Doe",
      "phone": "123-456-7890",
      "email": "john@example.com",
      "password": "secretpassword"
    }
    ```

#### 2. API Handler Contract (`RegisterHandler.java`)
* Inspects `exchange.getRequestMethod()`: if not `POST`, responds with HTTP `405`.
* Reads request body and extracts values via `extractJsonValue(body, key)`.
* If any field is `null`, sends HTTP `400`:
  ```json
  {"error":"Missing required fields"}
  ```
* Invokes `userRepo.saveUser(newUser)`.
* On success, returns HTTP `201 Created`:
  ```json
  {"message":"User registered successfully"}
  ```
* Catches `SQLException`: if `e.getMessage()` contains `"Duplicate entry"`, sends HTTP `409 Conflict`:
  ```json
  {"error":"Email already exists"}
  ```
* Any other server or database exception sends HTTP `500 Internal Server Error`.

#### 3. Security Contract (`PasswordHash.java`)
* Algorithm: BCrypt with 12 salt rounds (`BCrypt.gensalt(12)`).
* Produces standard 60-character BCrypt string starting with prefix `$2a$12$`.
* Plaintext passwords are never retained in memory longer than necessary and are never stored or returned.

---

## 7. Commands and Operations

### Build & Verification Commands
```powershell
# Compile and build the project using Gradle Wrapper
.\gradlew build

# Run unit and integration tests
.\gradlew test

# Start the application server
.\gradlew run
```

### Manual Database Verification Command
```powershell
# Inspect users table contents and verify BCrypt hashes ($2a$12$...)
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p app_db -e "SELECT id, name, email, password FROM users;"
```

### Resetting Test Data
```powershell
# Wipe registered test users to re-run end-to-end registration tests
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p app_db -e "DELETE FROM users;"
```

---

## 8. Verification Evidence

A comprehensive verification audit was conducted to confirm runtime correctness:

| Verification Target | Category | Actual Observed Evidence |
|:---|:---|:---|
| **Frontend Form** | VERIFIED | `register.html` contains Name, Phone, Email, and Password with HTML5 validation and success/error message containers. |
| **CSS Connection** | VERIFIED | Styles loaded from `css/style.css` without 404s. |
| **Vanilla JavaScript** | VERIFIED | `register.js` cancels default form reload and dispatches asynchronous `application/json` fetch payload. |
| **API Endpoint** | VERIFIED | `POST /api/register` exposed and responsive in `RegisterHandler.java`. |
| **Server-Side Validation** | VERIFIED | Requests missing `name`, `phone`, `email`, or `password` return HTTP `400 Bad Request`. |
| **BCrypt Password Hashing** | VERIFIED | `PasswordHash.java` uses `org.mindrot:jbcrypt:0.4`. Stored database records strictly begin with `$2a$12$`. |
| **Zero Plaintext Storage** | VERIFIED | Plaintext passwords never stored in MySQL, logged to terminal, or returned in API responses. |
| **JDBC Implementation** | VERIFIED | `UserRepository.java` connects via `Database.java` using parameterized `PreparedStatement`. |
| **MySQL `users` Table** | VERIFIED | Table schema includes `id`, `name`, `phone`, `email` (UNIQUE), `password`, and `created_at`. |
| **Duplicate Email Handling** | VERIFIED | Submitting an existing email triggers a database unique constraint violation, returning HTTP `409 Conflict`. |
| **Build & Test Suite** | VERIFIED | Executed `.\gradlew build` successfully in 7 seconds with 7 actionable tasks executed. |

---

## 9. Security and Reliability

1. **Password Storage Security**:
   * Passwords are never stored in plaintext.
   * Uses modern, industry-standard BCrypt hashing with an adaptive work factor of 12 rounds, providing robust defense against offline rainbow table and dictionary attacks.
2. **SQL Injection Prevention**:
   * Every parameter (`name`, `phone`, `email`, `password`) is bound strictly via `PreparedStatement.setString(index, value)`. No dynamic SQL string concatenation is used anywhere in the codebase.
3. **Information Leakage Prevention**:
   * When database errors occur, raw stack traces and internal schema details are logged only to the server console (`System.err.println`), returning generic JSON errors (`{"error":"Internal Server Error"}`) to the client.
4. **Duplicate Account Defense**:
   * Relies on the database engine's native `UNIQUE` index constraint on `email`, avoiding race conditions that can occur with application-level "check-then-insert" logic.

---

## 10. Deferred Work

The following features were intentionally excluded from Step 2 to keep the registration milestone tightly scoped and verifiable:
* **User Login**: `POST /api/login` and `login.html` (deferred to Step 3).
* **Session Management**: JWT tokens, cookies, or HTTP sessions.
* **Account Verification**: Email activation links or phone SMS OTPs.
* **Password Complexity Rules**: Enforcing special characters, uppercase, or length policies on the client/server.
* **User Management**: Viewing, editing, or deleting user profiles.

---

## 11. Commit and Repository State

* **Active Git Branch**: `main` (synchronized with `origin/main`).
* **Relevant Commits**:
  * `106c4ed31d9f0e7189671fef06ef9968efd56a4c` (*"commit2"*): Added initial User Registration implementation (PBKDF2 hashing, `RegisterHandler`, `register.html`, Gradle build).
  * `71f62c125191b40280ebdb2487e35b719ba1116b` (*"2ndcommmit"*): Added BCrypt hashing refactor, Gradle wrapper (`gradlew`), and subsequent Login feature files.
* **Current Working Tree Status**:
  * Clean with respect to registration implementation. All registration-related Java source files, tests, HTML, and CSS are fully committed.

---

## 12. Resume-From-Here (Handoff to Next Phase)

### Exact Implementation State at End of Step 2
* A fully functional user registration pipeline exists:
  * Database table `users` contains registered accounts with BCrypt hashes.
  * `POST /api/register` accepts new registrations and rejects duplicates.
  * `register.html` provides a user-facing registration interface.
  * The project builds cleanly with `.\gradlew build`.

### Guidelines for the Next Phase (User Login)
1. **Reuse Existing Identifiers**:
   * The database uniquely identifies users by their `email` column. The login interface should use `email` (or a username field mapping to email) as the user identifier.
2. **Preserve BCrypt Integration**:
   * Do not write custom password comparison logic. Use `PasswordHash.verify(password, storedHash)`, which calls `BCrypt.checkpw()`.
3. **Do Not Recreate Schema or Infrastructure**:
   * Do not alter the `users` table schema or create duplicate user tables.
   * Query the existing `users` table via `UserRepository` using `PreparedStatement`.
4. **Maintain Response Conventions**:
   * Return generic authentication failure messages (e.g. HTTP `401 Unauthorized` with `{"error":"Invalid email or password"}`) to prevent account enumeration.
