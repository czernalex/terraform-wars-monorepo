import { Component, inject } from '@angular/core';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { Router, RouterModule } from '@angular/router';
import { NzMessageService } from 'ng-zorro-antd/message';
import { FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { FormGroup } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { passwordsMatchValidator } from '@app/core/validators/passwords-match-validator';
import { finalize, takeUntil } from 'rxjs';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzDividerModule } from 'ng-zorro-antd/divider';

@Component({
    selector: 'app-sign-up',
    imports: [
        FormsModule,
        ReactiveFormsModule,
        NzFormModule,
        NzInputModule,
        NzButtonModule,
        NzCardModule,
        NzIconModule,
        NzDividerModule,
        RouterModule,
    ],
    templateUrl: './sign-up.component.html',
    styleUrl: './sign-up.component.css',
})
export class SignUpComponent extends BaseComponent {
    private authenticationAccountService = inject(AuthenticationAccountService);
    private router = inject(Router);
    private messageService = inject(NzMessageService);

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

        apiCall$
            .pipe(
                takeUntil(this.ngUnsubscribe$),
                finalize(() => (this.loading = false)),
            )
            .subscribe({
                next: () => {
                    this.messageService.success('You were successfully signed up', {
                        nzDuration: 5000,
                    });
                    this.router.navigateByUrl('/auth/login');
                },
                error: (error) => {
                    if (error.status === 401) {
                        this.messageService.success(
                            'You were successfully signed up. Check your email for a verification link.',
                            { nzDuration: 5000 },
                        );
                        this.router.navigateByUrl('/auth/login');
                        return;
                    }

                    const errorMessage = error.error?.errors?.[0]?.message || 'Failed to log in';
                    this.messageService.error(errorMessage);
                },
            });
    }
}
