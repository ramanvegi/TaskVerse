import { Employee } from './employee.model';
export type ProjectStatus = 'PLANNED' | 'IN_PROGRESS' | 'ON_HOLD' | 'COMPLETED' | 'CANCELLED';
export interface Project {
  id: number;
  name: string;
  project_code: string;
  description: string;
  employees: number[];
  employee_details: Employee[];
  start_date: string;
  end_date: string | null;
  status: ProjectStatus;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
export interface ProjectPayload {
  name: string;
  project_code: string;
  description: string;
  employees: number[];
  start_date: string;
  end_date: string | null;
  status: ProjectStatus;
  is_active: boolean;
}
export interface ProjectListResponse {
  success: boolean;
  message: string;
  count: number;
  next: string | null;
  previous: string | null;
  results: Project[];
}
