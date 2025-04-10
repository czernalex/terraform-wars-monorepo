import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '@app/core/services/auth.service';

export const sessionExpiredInterceptor: HttpInterceptorFn = (req, next) => {
    const authService = inject(AuthService);
    return next(req).pipe(
        catchError((error: HttpErrorResponse) => {
            if (authService.isSessionExpired(error, req.url)) {
                authService.setSessionExpired();
            }
            return throwError(() => error);
        }),
    );
};
