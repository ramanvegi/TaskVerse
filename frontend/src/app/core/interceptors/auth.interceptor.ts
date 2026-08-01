import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

import { API_BASE_URL } from '../constants/api.constants';
import { TokenStorageService } from '../services/token-storage.service';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const tokenStorage = inject(TokenStorageService);
  const router = inject(Router);
  const accessToken = tokenStorage.getAccessToken();

  const authenticatedRequest = accessToken && request.url.startsWith(API_BASE_URL)
    ? request.clone({ setHeaders: { Authorization: `Bearer ${accessToken}` } })
    : request;

  return next(authenticatedRequest).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !request.url.includes('/auth/login/')) {
        tokenStorage.clear();
        void router.navigate(['/login']);
      }
      return throwError(() => error);
    }),
  );
};

