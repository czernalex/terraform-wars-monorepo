import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { timer } from 'rxjs';
import { finalize, takeUntil } from 'rxjs/operators';
import { AuthenticationPasswordResetService } from '@app/api/allauth/authentication-password-reset/authentication-password-reset.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { MessageService } from 'primeng/api';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { Message } from 'primeng/message';
@Component({
    selector: 'app-password-reset',
    imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        InputTextModule,
        ButtonModule,
        Message,
    ],
    templateUrl: './request-password-reset.component.html',
    styleUrl: './request-password-reset.component.css',
})
export class RequestPasswordResetComponent extends BaseComponent {
    private router = inject(Router);
    private authenticationPasswordResetService = inject(AuthenticationPasswordResetService);
    private messageService = inject(MessageService);

    requestPasswordResetForm = new FormGroup({
        email: new FormControl<string>('', {
            validators: [Validators.required, Validators.email],
            nonNullable: true,
        }),
    });

    loading = false;

    requestResetPassword(): void {
        if (!this.requestPasswordResetForm.valid) {
            return;
        }

        const apiCall$ = this.authenticationPasswordResetService.postAllauthBrowserV1AuthPasswordRequest({
            email: this.requestPasswordResetForm.controls.email.value,
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
                        detail: $localize`Password reset email sent`,
                        life: messageLife,
                    });
                    timer(messageLife).subscribe(() => {
                        this.router.navigateByUrl('/auth/login');
                    });
                },
                error: (error) => {
                    if (error.status === 401) {
                        this.messageService.add({
                            severity: 'warn',
                            summary: $localize`Warning`,
                            detail: $localize`Your email needs to be verified. Check your email for a verification link.`,
                            life: messageLife,
                        });
                        timer(messageLife).subscribe(() => {
                            this.router.navigateByUrl('/auth/login');
                        });
                        return;
                    }

                    const errorMessage = error.error?.errors?.[0]?.message || $localize`Failed to request password reset`;
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
