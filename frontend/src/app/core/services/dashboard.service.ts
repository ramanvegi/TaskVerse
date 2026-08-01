import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { DashboardSummary } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private readonly http = inject(HttpClient);

  getSummary(): Observable<DashboardSummary> {
    return this.http
      .get<ApiResponse<DashboardSummary>>(API_ENDPOINTS.dashboard.summary)
      .pipe(map((response) => response.data));
  }
}

