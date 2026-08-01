import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { Task, TaskComment, TaskListResponse, TaskPayload, TaskStatus } from '../models/task.model';
@Injectable({ providedIn: 'root' })
export class TaskService {
  private readonly http = inject(HttpClient);
  list(search = '', project = '', assignedTo = '', status = '', priority = ''): Observable<TaskListResponse> {
    let params = new HttpParams();
    if (search.trim()) params = params.set('search', search.trim());
    if (project) params = params.set('project', project);
    if (assignedTo) params = params.set('assigned_to', assignedTo);
    if (status) params = params.set('status', status);
    if (priority) params = params.set('priority', priority);
    return this.http.get<TaskListResponse>(API_ENDPOINTS.tasks.list, { params });
  }
  create(payload: TaskPayload): Observable<Task> {
    return this.http.post<ApiResponse<Task>>(API_ENDPOINTS.tasks.list, payload).pipe(map((response) => response.data));
  }
  update(id: number, payload: Partial<TaskPayload>): Observable<Task> {
    return this.http.patch<ApiResponse<Task>>(API_ENDPOINTS.tasks.detail(id), payload).pipe(map((response) => response.data));
  }
  delete(id: number): Observable<void> {
    return this.http.delete<void>(API_ENDPOINTS.tasks.detail(id));
  }
  assign(id: number, assignedTo: number | null): Observable<Task> {
    return this.http.post<ApiResponse<Task>>(API_ENDPOINTS.tasks.assign(id), { assigned_to: assignedTo }).pipe(map((response) => response.data));
  }
  changeStatus(id: number, status: TaskStatus): Observable<Task> {
    return this.http.post<ApiResponse<Task>>(API_ENDPOINTS.tasks.changeStatus(id), { status }).pipe(map((response) => response.data));
  }
  comments(id: number): Observable<TaskComment[]> {
    return this.http.get<ApiResponse<TaskComment[]>>(API_ENDPOINTS.tasks.comments(id)).pipe(map((response) => response.data));
  }
  addComment(id: number, message: string): Observable<TaskComment> {
    return this.http.post<ApiResponse<TaskComment>>(API_ENDPOINTS.tasks.comments(id), { message }).pipe(map((response) => response.data));
  }
}
