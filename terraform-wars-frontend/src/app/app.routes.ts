import { Routes } from '@angular/router';
import { MainLayoutComponent } from './core/layouts/main-layout/main-layout.component';
import { AuthLayoutComponent } from './core/layouts/auth-layout/auth-layout.component';
import { canActivateAuthGuard } from './core/guards/can-activate-auth.guard';
import { LoginComponent } from './modules/auth/pages/login/login.component';
import { RequestPasswordResetComponent } from './modules/auth/pages/request-password-reset/request-password-reset.component';
import { PasswordResetComponent } from './modules/auth/pages/password-reset/password-reset.component';
import { PageNotFoundComponent } from './core/pages/page-not-found/page-not-found.component';
import { VerifyEmailComponent } from './modules/auth/pages/verify-email/verify-email.component';
import { DashboardComponent } from './modules/dashboard/pages/dashboard/dashboard.component';
import { SignUpComponent } from './modules/auth/pages/sign-up/sign-up.component';

export const routes: Routes = [
    {
        path: '',
        component: MainLayoutComponent,
        canActivate: [canActivateAuthGuard],
        children: [
            {
                path: '',
                redirectTo: '/dashboard',
                pathMatch: 'full',
            },
            {
                path: 'dashboard',
                component: DashboardComponent,
            },
        ],
    },
    {
        path: 'auth',
        component: AuthLayoutComponent,
        children: [
            {
                path: 'sign-up',
                title: 'Sign Up',
                component: SignUpComponent,
            },
            {
                path: 'verify-email/:key',
                title: 'Verify Email',
                component: VerifyEmailComponent,
            },
            {
                path: 'login',
                title: 'Login',
                component: LoginComponent,
            },
            {
                path: 'password-reset',
                title: 'Request Password Reset',
                component: RequestPasswordResetComponent,
            },
            {
                path: 'password-reset/:key',
                title: 'Password Reset',
                component: PasswordResetComponent,
            },
        ],
    },
    {
        path: '**',
        title: 'Page Not Found',
        component: PageNotFoundComponent,
    },
];
