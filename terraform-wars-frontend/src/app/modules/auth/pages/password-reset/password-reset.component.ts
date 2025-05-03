import { Component, inject, Input } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { finalize, takeUntil } from 'rxjs/operators';
import { MessageService } from 'primeng/api';
import { BaseComponent } from '@app/core/components/base/base.component';
import { passwordsMatchValidator } from '@app/core/validators/passwords-match-validator';
import { AuthenticationPasswordResetService } from '@app/api/allauth/authentication-password-reset/authentication-password-reset.service';
import { ButtonModule } from 'primeng/button';
import { PasswordModule } from 'primeng/password';
import { Message } from 'primeng/message';

@Component({
    selector: 'app-password-reset',
    imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        PasswordModule,
        ButtonModule,
        Message,
    ],
    templateUrl: './password-reset.component.html',
    styleUrl: './password-reset.component.css',
})
export class PasswordResetComponent extends BaseComponent {
    @Input() key = '';

    private router = inject(Router);
    private authenticationPasswordResetService = inject(AuthenticationPasswordResetService);
    private messageService = inject(MessageService);

    passwordResetForm = new FormGroup(
        {
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

    loading = false;

    resetPassword(): void {
        if (!this.passwordResetForm.valid) {
            return;
        }

        const apiCall$ = this.authenticationPasswordResetService.postAllauthBrowserV1AuthPasswordReset({
            key: this.key,
            password: this.passwordResetForm.controls.password1.value,
        });
        this.loading = true;

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
                        detail: $localize`Password reset successfully.`,
                    });
                    this.router.navigateByUrl('/auth/login');
                },
                error: (error) => {
                    if (error.status === 401) {
                        this.messageService.add({
                            severity: 'success',
                            summary: $localize`Success`,
                            detail: $localize`Password reset successfully. You can login now.`,
                        });
                        this.router.navigateByUrl('/auth/login');
                        return;
                    }

                    const errorMessage = error.error?.errors?.[0]?.message || 'Failed to reset password';
                    this.messageService.add({
                        severity: 'error',
                        summary: $localize`Error`,
                        detail: errorMessage,
                    });
                },
            });
    }
}
