import { inject, Injectable } from '@angular/core';
import { environment } from '@env/environment';
import { CookieService } from './cookie.service';
import { AuthService } from '@app/api/api/auth/auth.service';
import { NzMessageService } from 'ng-zorro-antd/message';

@Injectable({
  providedIn: 'root'
})
export class CsrfTokenService {
  private authService = inject(AuthService);
  private messageService = inject(NzMessageService);
  cookieService = inject(CookieService);

  ensureCsrfToken() {
    const csrfToken = this.cookieService.getCookie(environment.csrfCookieName);
    if (csrfToken) {
      return;
    }

    return this.authService.mainAppsApiAuthRoutersGetCsrfToken().subscribe({
      next: () => {},
      error: () => {
        this.messageService.error('Failed to connect to the server. Try refreshing the page.', {
          nzDuration: 0
        });
      }
    });
  }
}
