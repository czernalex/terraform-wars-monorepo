import { inject, Injectable } from '@angular/core';
import { environment } from '@env/environment';
import { CookieService } from './cookie.service';

const CSRF_SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'TRACE'];

@Injectable({
  providedIn: 'root'
})
export class CsrfTokenService {

  cookieService = inject(CookieService);

  getCSRFToken(): string | null {
    return this.cookieService.getCookie(environment.csrfCookieName);
  }

  isCSRFTokenRequired(method: string): boolean {
    return !CSRF_SAFE_METHODS.includes(method);
  }
}
