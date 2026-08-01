import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { Employee, EmployeeListResponse, EmployeePayload } from '../models/employee.model';
@Injectable({ providedIn: 'root' })
export class EmployeeService {
  private readonly http = inject(HttpClient);
  list(search = '', department = '', status = ''): Observable<EmployeeListResponse> {
    let params = new HttpParams();
    if (search.trim()) params = params.set('search', search.trim());
    if (department) params = params.set('department', department);
    if (status) params = params.set('status', status);
    return this.http.get<EmployeeListResponse>(API_ENDPOINTS.employees.list, { params });
  }
  create(payload: EmployeePayload): Observable<Employee> {
    return this.http.post<ApiResponse<Employee>>(API_ENDPOINTS.employees.list, payload).pipe(map((response) => response.data));
  }
  update(id: number, payload: Partial<EmployeePayload>): Observable<Employee> {
    return this.http.patch<ApiResponse<Employee>>(API_ENDPOINTS.employees.detail(id), payload).pipe(map((response) => response.data));
  }
  delete(id: number): Observable<void> {
    return this.http.delete<void>(API_ENDPOINTS.employees.detail(id));
  }
}
