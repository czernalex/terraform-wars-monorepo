import { Component, inject } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule, Validators, FormGroup, FormControl } from '@angular/forms';
import { finalize, takeUntil } from 'rxjs';
import { MessageService } from 'primeng/api';
import { Message } from 'primeng/message';
import { ButtonModule } from 'primeng/button';
import { PasswordModule } from 'primeng/password';
import { DividerModule } from 'primeng/divider';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { passwordsMatchValidator } from '@app/core/validators/passwords-match-validator';
import { InputTextModule } from 'primeng/inputtext';
@Component({
    selector: 'app-sign-up',
    imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        InputTextModule,
        Message,
        ButtonModule,
        PasswordModule,
        DividerModule,
    ],
    templateUrl: './sign-up.component.html',
    styleUrl: './sign-up.component.css',
})
export class SignUpComponent extends BaseComponent {
    private authenticationAccountService = inject(AuthenticationAccountService);
    private router = inject(Router);
    private messageService = inject(MessageService);

    signUpForm = new FormGroup(
        {
            email: new FormControl<string>('', {
                validators: [Validators.required, Validators.email],
                nonNullable: true,
            }),
            password1: new FormControl<string>('', {
                validators: [Validators.required, Validators.minLength(8)],
                nonNullable: true,
            }),
            password2: new FormControl<string>('', {
                validators: [Validators.required, Validators.minLength(8)],
                nonNullable: true,
            }),
        },
        { validators: [passwordsMatchValidator] },
    );

    isRawPasswordVisible = false;
    loading = false;

    signUp() {
        if (!this.signUpForm.valid) {
            return;
        }

        const apiCall$ = this.authenticationAccountService.postAllauthBrowserV1AuthSignup({
            email: this.signUpForm.controls.email.value,
            password: this.signUpForm.controls.password1.value,
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
                    this.messageService.add({
                        severity: 'success',
                        summary: $localize`Success`,
                        detail: $localize`You were successfully signed up.`,
                        life: messageLife,
                    });
                    this.router.navigateByUrl('/auth/login');
                },
                error: (error) => {
                    if (error.status === 401) {
                        this.messageService.add({
                            severity: 'success',
                            summary: $localize`Success`,
                            detail: $localize`You were successfully signed up. Check your email for a verification link.`,
                            life: messageLife,
                        });
                        this.router.navigateByUrl('/auth/login');
                        return;
                    }

                    const errorMessage = error.error?.errors?.[0]?.message || $localize`Failed to sign up`;
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
