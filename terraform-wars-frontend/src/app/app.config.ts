import {
    ApplicationConfig,
    provideZoneChangeDetection,
    importProvidersFrom,
    provideAppInitializer,
    inject,
    ErrorHandler,
} from '@angular/core';
import { provideRouter, Router, withComponentInputBinding } from '@angular/router';
import { registerLocaleData } from '@angular/common';
import { provideHttpClient, withFetch, withInterceptors, withXsrfConfiguration } from '@angular/common/http';
import en from '@angular/common/locales/en';
import { FormsModule } from '@angular/forms';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG} from 'primeng/config';
import { environment } from '@env/environment';
import { routes } from './app.routes';
import { apiUrlInterceptor } from './core/interceptors/api-url.interceptor';
import { withCredentialsInterceptor } from './core/interceptors/with-credentials.interceptor';
import { CsrfTokenService } from './core/services/csrf-token.service';
import * as Sentry from '@sentry/angular';
import { AuthService } from './core/services/auth.service';
import { sessionExpiredInterceptor } from './core/interceptors/session-expired.interceptor';
import { appThemePreset } from './app-theme-preset';
registerLocaleData(en);

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes, withComponentInputBinding()),
        importProvidersFrom(FormsModule),
        provideAnimationsAsync(),
        providePrimeNG({
            theme: {
                preset: appThemePreset,
            }
        }),
        provideHttpClient(
            withInterceptors([sessionExpiredInterceptor, apiUrlInterceptor, withCredentialsInterceptor]),
            withXsrfConfiguration({
                cookieName: environment.csrfCookieName,
                headerName: environment.csrfHeaderName,
            }),
            withFetch(),
        ),
        {
            provide: ErrorHandler,
            useValue: Sentry.createErrorHandler(),
        },
        {
            provide: Sentry.TraceService,
            deps: [Router],
        },
        provideAppInitializer(() => {
            const csrfTokenService = inject(CsrfTokenService);
            csrfTokenService.ensureCsrfToken();
        }),
        provideAppInitializer(() => {
            const authService = inject(AuthService);
            authService.fetchAuthenticatedUser();
        }),
    ],
};
