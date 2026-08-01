import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { Project, ProjectListResponse, ProjectPayload, ProjectStatus } from '../models/project.model';
@Injectable({ providedIn: 'root' })
export class ProjectService {
  private readonly http = inject(HttpClient);
  list(search = '', status = ''): Observable<ProjectListResponse> {
    let params = new HttpParams();
    if (search.trim()) params = params.set('search', search.trim());
    if (status) params = params.set('status', status);
    return this.http.get<ProjectListResponse>(API_ENDPOINTS.projects.list, { params });
  }
  create(payload: ProjectPayload): Observable<Project> {
    return this.http.post<ApiResponse<Project>>(API_ENDPOINTS.projects.list, payload).pipe(map((response) => response.data));
  }
  update(id: number, payload: Partial<ProjectPayload>): Observable<Project> {
    return this.http.patch<ApiResponse<Project>>(API_ENDPOINTS.projects.detail(id), payload).pipe(map((response) => response.data));
  }
  delete(id: number): Observable<void> {
    return this.http.delete<void>(API_ENDPOINTS.projects.detail(id));
  }
  assignEmployees(id: number, employeeIds: number[]): Observable<Project> {
    return this.http.post<ApiResponse<Project>>(API_ENDPOINTS.projects.assignEmployees(id), { employee_ids: employeeIds }).pipe(map((response) => response.data));
  }
  changeStatus(id: number, status: ProjectStatus): Observable<Project> {
    return this.http.post<ApiResponse<Project>>(API_ENDPOINTS.projects.changeStatus(id), { status }).pipe(map((response) => response.data));
  }
}
