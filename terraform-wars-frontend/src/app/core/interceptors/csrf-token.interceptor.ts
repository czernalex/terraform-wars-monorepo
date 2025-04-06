import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { CsrfTokenService } from '../services/csrf-token.service';

export const csrfTokenInterceptor: HttpInterceptorFn = (req, next) => {
  const csrfTokenService = inject(CsrfTokenService);

  if (!csrfTokenService.isCSRFTokenRequired(req.method)) {
    return next(req);
  }

  const csrfToken = csrfTokenService.getCSRFToken();
  if (csrfToken) {
    req = req.clone({
      setHeaders: {
        'X-CSRFToken': csrfToken
      }
    });
  }

  return next(req);
};
