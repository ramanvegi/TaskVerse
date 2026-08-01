# Smart Employee & Task Management Frontend
Angular 20 frontend for the TaskVerse.
## Current Scope
Completed foundation flow:
- Standalone Angular app
- Lazy-loaded routes
- Login page
- Register page
- Protected dashboard page
- Main authenticated layout
- 404 page
- JWT token storage
- JWT auth interceptor
- Auth route guard
- Dashboard summary API integration
## API Base URL
The frontend uses:
```text
http://127.0.0.1:8000/api
```
Configured in:
```text
src/environments/environment.ts
```
## Install
```powershell
npm install
```
## Run
```powershell
npm start
```
Open:
```text
http://localhost:4200/
```
## Build
```powershell
npm run build
```
## Next Frontend Modules
- Departments CRUD page
- Employees CRUD page
- Projects CRUD page
- Tasks CRUD page
- Profile page
- Better reusable shared components
