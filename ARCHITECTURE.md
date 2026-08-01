# TaskVerse Architecture & Flow Diagrams
Professional architecture diagrams for **TaskVerse**.
Style goal: clean, interview-friendly, Excalidraw-like system blocks with short labels and clear arrows.
> These diagrams use GitHub-compatible Mermaid syntax.
---
## 1. High-Level System Architecture
```mermaid
flowchart LR
    Client((User / Admin))
    subgraph Browser["Web Browser"]
        UI[Angular 20 UI]
        Components[Components]
        Services[Services]
        Interceptor[JWT Interceptor]
    end
    subgraph Backend["Django REST API"]
        API[API Router]
        Auth[Authentication]
        Dept[Departments]
        Emp[Employees]
        Proj[Projects]
        Tasks[Tasks]
        Dash[Dashboard / Reports]
    end
    subgraph Data["Database Layer"]
        DB[(MySQL / SQLite)]
    end
    subgraph Docs["API Documentation"]
        Swagger[Swagger UI]
        Schema[OpenAPI Schema]
    end
    Client --> UI
    UI --> Components
    Components --> Services
    Services --> Interceptor
    Interceptor --> API
    API --> Auth
    API --> Dept
    API --> Emp
    API --> Proj
    API --> Tasks
    API --> Dash
    Auth --> DB
    Dept --> DB
    Emp --> DB
    Proj --> DB
    Tasks --> DB
    Dash --> DB
    API --> Swagger
    API --> Schema
```
**Explanation:**
TaskVerse has an Angular frontend, a Django REST API backend, and a database layer. Angular talks to Django through services, the JWT interceptor attaches tokens, and Django apps handle business modules.
---
## 2. Application Flow
```mermaid
flowchart TD
    Start((Start)) --> Login[Login]
    Login --> Validate{Valid user?}
    Validate -- No --> Error[Show error]
    Error --> Login
    Validate -- Yes --> Token[Store JWT]
    Token --> Dashboard[Dashboard]
    Dashboard --> Dept[Departments]
    Dashboard --> Emp[Employees]
    Dashboard --> Proj[Projects]
    Dashboard --> Task[Tasks]
    Dashboard --> Reports[Reports]
    Dept --> ManageDept[Create / Edit / Delete]
    Emp --> ManageEmp[Create / Edit / Delete]
    Proj --> ManageProj[Assign Employees]
    Task --> ManageTask[Assign / Track / Comment]
    ManageDept --> Dashboard
    ManageEmp --> Dashboard
    ManageProj --> Dashboard
    ManageTask --> Dashboard
    Dashboard --> Logout[Logout]
    Logout --> Clear[Clear Token]
    Clear --> Login
```
**Explanation:**
Users log in first, then land on the Dashboard. From the Dashboard they can manage departments, employees, projects, tasks, comments, and reports. Logout clears the JWT session.
---
## 3. Database ER Diagram
```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email UK
        string role
        boolean is_staff
        boolean is_superuser
    }
    DEPARTMENT {
        int id PK
        string name
        string code
        boolean is_active
    }
    EMPLOYEE {
        int id PK
        int user_id FK
        int department_id FK
        string employee_code
        string email
        string job_title
        string status
    }
    PROJECT {
        int id PK
        string name
        string project_code
        string status
        boolean is_active
    }
    TASK {
        int id PK
        int project_id FK
        int assigned_to_id FK
        string title
        string priority
        string status
        date due_date
    }
    TASK_COMMENT {
        int id PK
        int task_id FK
        int author_id FK
        text message
    }
    USER ||--o| EMPLOYEE : profile
    DEPARTMENT ||--o{ EMPLOYEE : contains
    PROJECT }o--o{ EMPLOYEE : assigns
    PROJECT ||--o{ TASK : owns
    EMPLOYEE ||--o{ TASK : works_on
    TASK ||--o{ TASK_COMMENT : has
    USER ||--o{ TASK_COMMENT : writes
```
**Explanation:**
Departments contain employees. Projects can have many employees. Tasks belong to projects and can be assigned to employees. Users authenticate and can write task comments.
---
## 4. Authentication Flow
```mermaid
sequenceDiagram
    actor User
    participant Angular as Angular UI
    participant AuthService as AuthService
    participant API as Django Auth API
    participant DB as MySQL / SQLite
    participant JWT as JWT Token
    User->>Angular: Enter email + password
    Angular->>AuthService: Submit login form
    AuthService->>API: POST /api/auth/login/
    API->>DB: Check user credentials
    DB-->>API: User valid
    API->>JWT: Create access + refresh token
    JWT-->>API: Tokens
    API-->>AuthService: User + tokens
    AuthService-->>Angular: Save session
    Angular-->>User: Redirect to Dashboard
```
**Explanation:**
The login API validates the user and returns JWT tokens. Angular stores the token and uses it for protected pages and API calls.
---
## 5. Protected API Request Flow
```mermaid
sequenceDiagram
    participant C as Angular Component
    participant S as Angular Service
    participant I as JWT Interceptor
    participant V as DRF View
    participant Ser as Serializer
    participant BL as Service Layer
    participant M as Model
    participant DB as MySQL / SQLite
    C->>S: User action
    S->>I: HTTP request
    I->>I: Add Bearer token
    I->>V: REST API call
    V->>Ser: Validate input
    Ser-->>V: Valid data
    V->>BL: Business logic
    BL->>M: ORM operation
    M->>DB: Query database
    DB-->>M: Data result
    M-->>BL: Model result
    BL-->>V: Processed result
    V->>Ser: Serialize response
    Ser-->>V: JSON data
    V-->>C: API response
```
**Explanation:**
Angular components call services. Services call REST APIs. Django validates input using serializers, processes logic, updates models, queries the database, and returns JSON responses.
---
## 6. Module Relationship Diagram
```mermaid
flowchart LR
    subgraph Setup["Organization Setup"]
        Dept[Department]
        Emp[Employee]
    end
    subgraph Delivery["Delivery Management"]
        Proj[Project]
        Task[Task]
        Comment[Task Comment]
    end
    subgraph Platform["Platform"]
        User[User / Role]
        Dash[Dashboard]
        Reports[Reports]
    end
    Dept --> Emp
    Emp --> Proj
    Proj --> Task
    Task --> Comment
    User --> Emp
    User --> Task
    User --> Comment
    Dept --> Dash
    Emp --> Dash
    Proj --> Dash
    Task --> Dash
    Dash --> Reports
```
**Explanation:**
The main business flow starts from departments, then employees, then projects, then tasks. Dashboard and reports summarize data from all modules.
---
## 7. Task Workflow
```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> TODO: Save
    TODO --> IN_PROGRESS: Start
    IN_PROGRESS --> COMPLETED: Finish
    COMPLETED --> [*]
    TODO --> TODO: Edit
    IN_PROGRESS --> TODO: Move Back
    COMPLETED --> IN_PROGRESS: Reopen
```
**Explanation:**
A task starts as created, then moves to TODO, IN_PROGRESS, and COMPLETED. The workflow also supports editing, moving back, and reopening if required.
---
## 8. Backend & Frontend Folder Architecture
```mermaid
flowchart LR
    Root[TaskVerse]
    subgraph Backend["backend"]
        Config[config]
        Apps[apps]
        Common[common]
        Manage[manage.py]
        DBFile[db.sqlite3]
    end
    subgraph BackendApps["Django Apps"]
        Auth[authentication]
        Dept[departments]
        Emp[employees]
        Proj[projects]
        Tasks[tasks]
        Dash[dashboard]
    end
    subgraph Frontend["frontend"]
        Src[src]
        AngularJson[angular.json]
        Package[package.json]
    end
    subgraph AngularApp["src/app"]
        Core[core]
        Features[features]
        Layouts[layouts]
        Shared[shared]
    end
    Root --> Backend
    Root --> Frontend
    Backend --> Config
    Backend --> Apps
    Backend --> Common
    Backend --> Manage
    Backend --> DBFile
    Apps --> Auth
    Apps --> Dept
    Apps --> Emp
    Apps --> Proj
    Apps --> Tasks
    Apps --> Dash
    Frontend --> Src
    Frontend --> AngularJson
    Frontend --> Package
    Src --> AngularApp
    AngularApp --> Core
    AngularApp --> Features
    AngularApp --> Layouts
    AngularApp --> Shared
```
**Explanation:**
The backend is separated into Django apps and shared utilities. The frontend is separated into Angular core services, feature pages, layout components, and shared UI components.
---
## 9. Backend Folder Architecture
```mermaid
flowchart TD
    Backend[backend]
    Backend --> Config[config]
    Backend --> Apps[apps]
    Backend --> Common[common]
    Backend --> Req[requirements.txt]
    Backend --> Manage[manage.py]
    Config --> Settings[settings.py]
    Config --> URLs[urls.py]
    Config --> ASGI[asgi.py]
    Config --> WSGI[wsgi.py]
    Apps --> Auth[authentication]
    Apps --> Dept[departments]
    Apps --> Emp[employees]
    Apps --> Proj[projects]
    Apps --> Tasks[tasks]
    Apps --> Dash[dashboard]
    Auth --> AuthFiles[models / serializers / views / urls]
    Dept --> DeptFiles[models / serializers / views / urls]
    Emp --> EmpFiles[models / serializers / views / urls]
    Proj --> ProjFiles[models / serializers / views / urls]
    Tasks --> TaskFiles[models / serializers / views / urls]
    Common --> Response[responses]
    Common --> Exceptions[exceptions]
    Common --> Pagination[pagination]
    Common --> Health[health check]
```
**Explanation:**
The backend uses modular Django apps. Each module owns its API views, serializers, models, URLs, validations, and service logic.
---
## 10. Frontend Folder Architecture
```mermaid
flowchart TD
    Frontend[frontend]
    Frontend --> Src[src]
    Frontend --> AngularConfig[angular.json]
    Frontend --> Package[package.json]
    Src --> App[app]
    Src --> Env[environments]
    Src --> Styles[styles.scss]
    App --> Core[core]
    App --> Features[features]
    App --> Layouts[layouts]
    App --> Shared[shared]
    App --> Routes[app.routes.ts]
    App --> AppConfig[app.config.ts]
    Core --> Constants[constants]
    Core --> Models[models]
    Core --> Services[services]
    Core --> Guards[guards]
    Core --> Interceptors[interceptors]
    Features --> Auth[auth]
    Features --> Dashboard[dashboard]
    Features --> Departments[departments]
    Features --> Employees[employees]
    Features --> Projects[projects]
    Features --> Tasks[tasks]
    Layouts --> MainLayout[main-layout]
    Shared --> PageHeader[page-header]
```
**Explanation:**
The frontend follows Angular feature-based structure. Core contains API logic and shared infrastructure, while features contain the actual pages.
---
## 11. Admin Control Flow
```mermaid
flowchart LR
    Admin((Admin User)) --> Login[Login]
    Login --> JWT[JWT Token]
    JWT --> Dashboard[Admin Dashboard Panel]
    Dashboard --> Dept[Manage Departments]
    Dashboard --> Emp[Manage Employees]
    Dashboard --> Proj[Manage Projects]
    Dashboard --> Tasks[Manage Tasks]
    Dashboard --> DjangoAdmin[Django Admin]
    Dept --> DB[(Database)]
    Emp --> DB
    Proj --> DB
    Tasks --> DB
    DjangoAdmin --> DB
```
**Explanation:**
Admin users have full control. They can manage all business modules from the Angular dashboard and also access Django Admin for backend-level data management.
---
## 12. Interview-Friendly Summary
TaskVerse follows a clean full-stack architecture:
- **Angular 20** handles the UI.
- **Angular services** call REST APIs.
- **JWT interceptor** attaches access tokens.
- **Django REST Framework** exposes backend APIs.
- **Serializers** validate request and response data.
- **Service layer and models** handle business logic and database operations.
- **MySQL / SQLite** stores persistent data.
- **Swagger / OpenAPI** documents and tests backend APIs.
This architecture is modular, scalable, secure, and easy to explain in interviews.
