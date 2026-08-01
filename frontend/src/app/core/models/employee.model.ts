import { Department } from './department.model';
export type EmployeeStatus = 'ACTIVE' | 'INACTIVE' | 'ON_LEAVE';
export interface Employee {
  id: number;
  user: number | null;
  department: number;
  department_detail: Department;
  employee_code: string;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  phone_number: string;
  job_title: string;
  hire_date: string;
  status: EmployeeStatus;
  address: string;
  created_at: string;
  updated_at: string;
}
export interface EmployeePayload {
  department: number;
  employee_code: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  job_title: string;
  hire_date: string;
  status: EmployeeStatus;
  address: string;
}
export interface EmployeeListResponse {
  success: boolean;
  message: string;
  count: number;
  next: string | null;
  previous: string | null;
  results: Employee[];
}
