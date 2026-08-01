export interface Department {
  id: number;
  name: string;
  code: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
export interface DepartmentPayload {
  name: string;
  code: string;
  description: string;
  is_active: boolean;
}
export interface DepartmentListResponse {
  success: boolean;
  message: string;
  count: number;
  next: string | null;
  previous: string | null;
  results: Department[];
}
