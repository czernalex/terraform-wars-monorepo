import { Routes } from '@angular/router';
import { canActivateAuthGuard } from './core/guards/can-activate-auth.guard';
import { LoginComponent } from './modules/auth/pages/login/login.component';
import { RequestPasswordResetComponent } from './modules/auth/pages/request-password-reset/request-password-reset.component';
import { PasswordResetComponent } from './modules/auth/pages/password-reset/password-reset.component';
import { PageNotFoundComponent } from './core/pages/page-not-found/page-not-found.component';
import { VerifyEmailComponent } from './modules/auth/pages/verify-email/verify-email.component';
import { DashboardComponent } from './modules/dashboard/pages/dashboard/dashboard.component';
import { SignUpComponent } from './modules/auth/pages/sign-up/sign-up.component';
import { canActivateUnauthGuard } from './core/guards/can-activate-unauth.guard';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full',
    },
    {
        path: 'auth/sign-up',
        title: 'Sign Up',
        component: SignUpComponent,
        canActivate: [canActivateUnauthGuard],
    },
    {
        path: 'auth/verify-email/:key',
        title: 'Verify Email',
        component: VerifyEmailComponent,
    },
    {
        path: 'auth/login',
        title: 'Login',
        component: LoginComponent,
        canActivate: [canActivateUnauthGuard],
    },
    {
        path: 'auth/password-reset',
        title: 'Request Password Reset',
        component: RequestPasswordResetComponent,
    },
    {
        path: 'auth/password-reset/:key',
        title: 'Password Reset',
        component: PasswordResetComponent,
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
        canActivate: [canActivateAuthGuard],
        title: 'Dashboard',
    },
    {
        path: '**',
        title: 'Page Not Found',
        component: PageNotFoundComponent,
    },
];
