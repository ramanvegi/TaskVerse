import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject } from '@angular/core';
import { Observable, map, tap } from 'rxjs';

import { API_ENDPOINTS } from '../constants/api.constants';
import { ApiResponse } from '../models/api-response.model';
import { AuthData, LoginRequest, RegisterRequest, User } from '../models/auth.model';
import { TokenStorageService } from './token-storage.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly tokenStorage = inject(TokenStorageService);

  readonly currentUser = this.tokenStorage.currentUser;
  readonly isAuthenticated = computed(() => this.tokenStorage.isAuthenticated());
  readonly isAdmin = computed(() => this.currentUser()?.role === 'ADMIN');

  hasAnyRole(roles: User['role'][]): boolean {
    const role = this.currentUser()?.role;
    return !!role && roles.includes(role);
  }

  login(payload: LoginRequest): Observable<AuthData> {
    return this.http.post<ApiResponse<AuthData>>(API_ENDPOINTS.auth.login, payload).pipe(
      map((response) => response.data),
      tap((data) => this.tokenStorage.saveSession(data.tokens, data.user)),
    );
  }

  register(payload: RegisterRequest): Observable<AuthData> {
    return this.http.post<ApiResponse<AuthData>>(API_ENDPOINTS.auth.register, payload).pipe(
      map((response) => response.data),
      tap((data) => this.tokenStorage.saveSession(data.tokens, data.user)),
    );
  }

  loadProfile(): Observable<User> {
    return this.http.get<ApiResponse<User>>(API_ENDPOINTS.auth.profile).pipe(map((response) => response.data));
  }

  logout(): void {
    this.tokenStorage.clear();
  }
}

