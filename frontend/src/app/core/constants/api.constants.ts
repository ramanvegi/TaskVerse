import { environment } from '../../../environments/environment';

export const API_BASE_URL = environment.apiBaseUrl;

export const API_ENDPOINTS = {
  auth: {
    register: `${API_BASE_URL}/auth/register/`,
    login: `${API_BASE_URL}/auth/login/`,
    logout: `${API_BASE_URL}/auth/logout/`,
    profile: `${API_BASE_URL}/auth/profile/`,
    changePassword: `${API_BASE_URL}/auth/change-password/`,
    refresh: `${API_BASE_URL}/auth/token/refresh/`,
  },
  dashboard: {
    summary: `${API_BASE_URL}/dashboard/summary/`,
  },
  departments: {
    list: `${API_BASE_URL}/departments/`,
    detail: (id: number) => `${API_BASE_URL}/departments/${id}/`,
  },
  employees: {
    list: `${API_BASE_URL}/employees/`,
    detail: (id: number) => `${API_BASE_URL}/employees/${id}/`,
  },
  projects: {
    list: `${API_BASE_URL}/projects/`,
    detail: (id: number) => `${API_BASE_URL}/projects/${id}/`,
    assignEmployees: (id: number) => `${API_BASE_URL}/projects/${id}/assign-employees/`,
    changeStatus: (id: number) => `${API_BASE_URL}/projects/${id}/change-status/`,
  },
  tasks: {
    list: `${API_BASE_URL}/tasks/`,
    detail: (id: number) => `${API_BASE_URL}/tasks/${id}/`,
    assign: (id: number) => `${API_BASE_URL}/tasks/${id}/assign/`,
    changeStatus: (id: number) => `${API_BASE_URL}/tasks/${id}/change-status/`,
    comments: (id: number) => `${API_BASE_URL}/tasks/${id}/comments/`,
  },
} as const;

