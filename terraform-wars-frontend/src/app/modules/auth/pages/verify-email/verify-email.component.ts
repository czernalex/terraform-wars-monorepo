import { Component, inject, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { BaseComponent } from '@app/core/components/base/base.component';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { timer } from 'rxjs';
@Component({
    selector: 'app-verify-email',
    imports: [RouterModule, ButtonModule, ProgressSpinnerModule],
    templateUrl: './verify-email.component.html',
    styleUrl: './verify-email.component.css',
})
export class VerifyEmailComponent extends BaseComponent implements OnInit {
    @Input() key = '';

    private authenticationAccountService = inject(AuthenticationAccountService);
    private messageService = inject(MessageService);
    private router = inject(Router);

    state: 'loading' | 'success' | 'error' = 'loading';

    ngOnInit(): void {
        this.verifyEmail();
    }

    verifyEmail() {
        const apiCall$ = this.authenticationAccountService.postAllauthBrowserV1AuthEmailVerify({
            key: this.key,
        });

        const messageLife = 3000;

        apiCall$.pipe(takeUntil(this.ngUnsubscribe$)).subscribe({
            next: () => {
                this.state = 'success';
                this.messageService.add({
                    severity: 'success',
                    summary: $localize`Success`,
                    detail: $localize`Email verified successfully`,
                    life: messageLife,
                });
                timer(messageLife).subscribe(() => {
                    this.router.navigateByUrl('/');
                });
            },
            error: (error) => {
                if (error.status === 401) {
                    this.state = 'success';
                    this.messageService.add({
                        severity: 'success',
                        summary: $localize`Success`,
                        detail: $localize`Email verified successfully. You can login now.`,
                        life: messageLife,
                    });
                    timer(messageLife).subscribe(() => {
                        this.router.navigateByUrl('/auth/login');
                    });
                    return;
                }

                this.state = 'error';
                const errorMessage = error.error?.errors?.[0]?.message || $localize`Failed to verify email`;
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
