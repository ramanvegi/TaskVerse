import { Employee } from './employee.model';
import { Project } from './project.model';
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'COMPLETED';
export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH';
export interface Task {
  id: number;
  project: number;
  project_detail: Project;
  assigned_to: number | null;
  assigned_to_detail: Employee | null;
  title: string;
  description: string;
  due_date: string;
  priority: TaskPriority;
  status: TaskStatus;
  comments_count: number;
  is_overdue: boolean;
  created_by: number | null;
  created_at: string;
  updated_at: string;
}
export interface TaskPayload {
  project: number;
  assigned_to: number | null;
  title: string;
  description: string;
  due_date: string;
  priority: TaskPriority;
  status: TaskStatus;
}
export interface TaskComment {
  id: number;
  task: number;
  author: number | null;
  author_email: string;
  message: string;
  created_at: string;
  updated_at: string;
}
export interface TaskListResponse {
  success: boolean;
  message: string;
  count: number;
  next: string | null;
  previous: string | null;
  results: Task[];
}
