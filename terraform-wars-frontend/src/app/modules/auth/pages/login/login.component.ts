import { Component, inject } from '@angular/core';
import { Validators, FormsModule, ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { finalize, takeUntil } from 'rxjs/operators';
import { AuthService } from '@app/core/services/auth.service';
import { UsersService } from '@app/api/api/users/users.service';
import { MessageService } from 'primeng/api';
import { Message } from 'primeng/message';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { PasswordModule } from 'primeng/password';
import { DividerModule } from 'primeng/divider';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { ToastModule } from 'primeng/toast';
@Component({
    selector: 'app-login',
    imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        Message,
        InputTextModule,
        ButtonModule,
        PasswordModule,
        DividerModule,
        ProgressSpinnerModule,
        ToastModule,
    ],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css',
})
export class LoginComponent extends BaseComponent {
    private authenticationAccountService = inject(AuthenticationAccountService);
    private usersService = inject(UsersService);
    private authService = inject(AuthService);
    private router = inject(Router);
    private route = inject(ActivatedRoute);
    private messageService = inject(MessageService);

    loginForm = new FormGroup({
        email: new FormControl<string>('', {
            validators: [Validators.required, Validators.email],
            nonNullable: true,
        }),
        password: new FormControl<string>('', {
            validators: [Validators.required, Validators.minLength(8)],
            nonNullable: true,
        }),
    });

    isRawPasswordVisible = false;
    loading = false;

    getNextUrl(): string {
        const nextUrl = this.route.snapshot.queryParams['nextUrl'];
        return nextUrl || '/';
    }

    login(): void {
        if (!this.loginForm.valid) {
            return;
        }

        const apiCall$ = this.authenticationAccountService.postAllauthBrowserV1AuthLogin({
            email: this.loginForm.controls.email.value,
            password: this.loginForm.controls.password.value,
        });
        this.loading = true;

        const messageLife = 3000;

        apiCall$
            .pipe(
                takeUntil(this.ngUnsubscribe$),
                finalize(() => (this.loading = false)),
            )
            .subscribe({
                next: () => {
                    this.usersService.mainAppsUsersRoutersGetMe().subscribe({
                        next: (user) => {
                            this.messageService.add({
                                severity: 'success',
                                summary: $localize`Success`,
                                detail: $localize`You were successfully logged in`,
                                life: messageLife,
                            });
                            this.authService.authenticatedUser = user;
                            this.router.navigateByUrl(this.getNextUrl());
                        },
                        error: () => {
                            this.messageService.add({
                                severity: 'error',
                                summary: $localize`Error`,
                                detail: $localize`Failed to get user details`,
                                life: messageLife,
                            });
                        },
                    });
                },
                error: (error) => {
                    if (error.status === 401) {
                        this.loginForm.controls.password.setErrors({ email: true });
                        this.messageService.add({
                            severity: 'warn',
                            summary: $localize`Warning`,
                            detail: $localize`Your email needs to be verified. Check your email for a verification link.`,
                            life: messageLife,
                        });
                        return;
                    }

                    this.loginForm.controls.password.setErrors({ password: true });
                    const errorMessage = error.error?.errors?.[0]?.message || $localize`Failed to log in`;
                    this.messageService.add({
                        severity: 'error',
                        summary: $localize`Error`,
                        detail: errorMessage,
                        life: messageLife,
                    });
                },
            });
    }
}
