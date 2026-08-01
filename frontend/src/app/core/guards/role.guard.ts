import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { User } from '../models/auth.model';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = (route.data?.['roles'] || []) as User['role'][];

  if (!allowedRoles.length || auth.hasAnyRole(allowedRoles)) {
    return true;
  }

  return router.createUrlTree(['/dashboard']);
};

