import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  {
	path: 'login',
	loadComponent: () => import('./features/auth/login/login.component').then((m) => m.LoginComponent),
  },
  {
	path: 'register',
	loadComponent: () => import('./features/auth/register/register.component').then((m) => m.RegisterComponent),
  },
  {
	path: '',
	canActivate: [authGuard],
	loadComponent: () => import('./layouts/main-layout/main-layout.component').then((m) => m.MainLayoutComponent),
	children: [
	  {
		path: 'dashboard',
		loadComponent: () => import('./features/dashboard/dashboard.component').then((m) => m.DashboardComponent),
	  },
	  {
		path: 'departments',
		loadComponent: () => import('./features/departments/departments.component').then((m) => m.DepartmentsComponent),
	  },
	  {
		path: 'employees',
		loadComponent: () => import('./features/employees/employees.component').then((m) => m.EmployeesComponent),
	  },
	  {
		path: 'projects',
		loadComponent: () => import('./features/projects/projects.component').then((m) => m.ProjectsComponent),
	  },
	  {
		path: 'tasks',
		loadComponent: () => import('./features/tasks/tasks.component').then((m) => m.TasksComponent),
	  },
	],
  },
  {
	path: '**',
	loadComponent: () => import('./features/not-found/not-found.component').then((m) => m.NotFoundComponent),
  },
];
