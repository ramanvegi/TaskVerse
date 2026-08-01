import { Injectable, signal } from '@angular/core';

import { JwtTokens, User } from '../models/auth.model';

const ACCESS_TOKEN_KEY = 'smart_employee_access_token';
const REFRESH_TOKEN_KEY = 'smart_employee_refresh_token';
const USER_KEY = 'smart_employee_user';

@Injectable({ providedIn: 'root' })
export class TokenStorageService {
  readonly currentUser = signal<User | null>(this.getUser());

  saveSession(tokens: JwtTokens, user: User): void {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    this.currentUser.set(user);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  getUser(): User | null {
    const storedUser = localStorage.getItem(USER_KEY);
    return storedUser ? (JSON.parse(storedUser) as User) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  clear(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUser.set(null);
  }
}

