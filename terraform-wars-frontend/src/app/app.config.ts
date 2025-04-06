import { ApplicationConfig, provideZoneChangeDetection, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { en_US, provideNzI18n } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { FormsModule } from '@angular/forms';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { LockOutline, MailOutline } from '@ant-design/icons-angular/icons';
import { apiUrlInterceptor } from './core/interceptors/api-url.interceptor';
import { csrfTokenInterceptor } from './core/interceptors/csrf-token.interceptor';
import { withCredentialsInterceptor } from './core/interceptors/with-credentials.interceptor';
registerLocaleData(en);

const icons = [LockOutline, MailOutline];

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideNzI18n(en_US),
    importProvidersFrom(FormsModule),
    provideAnimationsAsync(),
    provideHttpClient(
      withFetch(),
      withInterceptors([
        apiUrlInterceptor,
        withCredentialsInterceptor,
        csrfTokenInterceptor,
      ])
    ),
    importProvidersFrom(NzIconModule.forRoot(icons)),
  ],
};
