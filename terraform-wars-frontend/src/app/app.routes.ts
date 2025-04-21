import { Routes } from '@angular/router';
import { MainLayoutComponent } from '@app/core/layout/main-layout/main-layout.component';
import { AuthLayoutComponent } from '@app/core/layout/auth-layout/auth-layout.component';
import { canActivateAuthGuard } from '@app/core/guards/can-activate-auth.guard';
import { LoginComponent } from '@app/modules/auth/pages/login/login.component';
import { RequestPasswordResetComponent } from '@app/modules/auth/pages/request-password-reset/request-password-reset.component';
import { PasswordResetComponent } from '@app/modules/auth/pages/password-reset/password-reset.component';
import { PageNotFoundComponent } from '@app/core/pages/page-not-found/page-not-found.component';
import { VerifyEmailComponent } from '@app/modules/auth/pages/verify-email/verify-email.component';
import { DashboardComponent } from '@app/modules/dashboard/pages/dashboard/dashboard.component';
import { SignUpComponent } from '@app/modules/auth/pages/sign-up/sign-up.component';
import { canActivateUnauthGuard } from '@app/core/guards/can-activate-unauth.guard';
import { TutorialGroupsComponent } from '@app/modules/tutorials/pages/tutorial-groups/tutorial-groups.component';

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
                title: 'Dashboard',
                component: DashboardComponent,
            },
            {
                path: 'tutorial-groups',
                title: 'Tutorial Groups',
                component: TutorialGroupsComponent,
            },
        ],
    },
    {
        path: 'auth',
        component: AuthLayoutComponent,
        canActivate: [canActivateUnauthGuard],
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
