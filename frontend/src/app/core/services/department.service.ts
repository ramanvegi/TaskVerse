import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { Department, DepartmentListResponse, DepartmentPayload } from '../models/department.model';
@Injectable({ providedIn: 'root' })
export class DepartmentService {
  private readonly http = inject(HttpClient);
  list(search = ''): Observable<DepartmentListResponse> {
    let params = new HttpParams();
    if (search.trim()) {
      params = params.set('search', search.trim());
    }
    return this.http.get<DepartmentListResponse>(API_ENDPOINTS.departments.list, { params });
  }
  create(payload: DepartmentPayload): Observable<Department> {
    return this.http
      .post<ApiResponse<Department>>(API_ENDPOINTS.departments.list, payload)
      .pipe(map((response) => response.data));
  }
  update(id: number, payload: Partial<DepartmentPayload>): Observable<Department> {
    return this.http
      .patch<ApiResponse<Department>>(API_ENDPOINTS.departments.detail(id), payload)
      .pipe(map((response) => response.data));
  }
  delete(id: number): Observable<void> {
    return this.http.delete<void>(API_ENDPOINTS.departments.detail(id));
  }
}
