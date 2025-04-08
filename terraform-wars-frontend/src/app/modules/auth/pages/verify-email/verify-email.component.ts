import { Component, inject, Input, OnInit } from '@angular/core';
import { BaseComponent } from '@app/core/components/base/base.component';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { NzResultModule } from 'ng-zorro-antd/result';
import { NzSpinModule } from 'ng-zorro-antd/spin';
import { takeUntil } from 'rxjs/operators';
import { NzMessageService } from 'ng-zorro-antd/message';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-verify-email',
    imports: [NzResultModule, NzSpinModule, RouterModule],
    templateUrl: './verify-email.component.html',
    styleUrl: './verify-email.component.css',
})
export class VerifyEmailComponent extends BaseComponent implements OnInit {
    @Input() key = '';

    private authenticationAccountService = inject(AuthenticationAccountService);
    private messageService = inject(NzMessageService);
    private router = inject(Router);

    state: 'loading' | 'success' | 'error' = 'loading';

    ngOnInit(): void {
        this.verifyEmail();
    }

    verifyEmail() {
        const apiCall$ = this.authenticationAccountService.postAllauthBrowserV1AuthEmailVerify({
            key: this.key,
        });

        apiCall$.pipe(takeUntil(this.ngUnsubscribe$)).subscribe({
            next: () => {
                this.state = 'success';
                this.messageService.success('Email verified successfully');
                this.router.navigateByUrl('/');
            },
            error: (error) => {
                if (error.status === 401) {
                    this.state = 'success';
                    this.messageService.success('Email verified successfully. You can login now.');
                    this.router.navigateByUrl('/auth/login');
                    return;
                }

                this.state = 'error';
                const errorMessage = error.error?.errors?.[0]?.message || 'Failed to verify email';
                this.messageService.error(errorMessage);
            },
        });
    }
}
