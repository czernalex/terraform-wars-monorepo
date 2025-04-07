import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { finalize, takeUntil } from 'rxjs/operators';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzMessageService } from 'ng-zorro-antd/message';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzCardModule } from 'ng-zorro-antd/card';
import { AuthenticationPasswordResetService } from '@app/api/allauth/authentication-password-reset/authentication-password-reset.service';
import { BaseComponent } from '@app/core/components/base/base.component';

@Component({
  selector: 'app-password-reset',
  imports: [
    FormsModule,
    ReactiveFormsModule,
    NzFormModule,
    NzInputModule,
    NzButtonModule,
    NzTypographyModule,
    NzIconModule,
    NzCardModule,
    RouterModule,
  ],
  templateUrl: './request-password-reset.component.html',
  styleUrl: './request-password-reset.component.css'
})
export class RequestPasswordResetComponent extends BaseComponent {
  private router = inject(Router);
  private authenticationPasswordResetService = inject(AuthenticationPasswordResetService);
  private messageService = inject(NzMessageService);

  requestPasswordResetForm = new FormGroup({
    email: new FormControl<string>(
      '',
      { validators: [Validators.required, Validators.email], nonNullable: true }
    ),
  });

  loading = false;

  requestResetPassword(): void {
    if (!this.requestPasswordResetForm.valid) {
      return;
    }

    const apiCall$ = this.authenticationPasswordResetService.postAllauthBrowserV1AuthPasswordRequest({
      email: this.requestPasswordResetForm.controls.email.value
    });
    this.loading = true;

    apiCall$.pipe(
      takeUntil(this.ngUnsubscribe$),
      finalize(() => this.loading = false)
    ).subscribe({
      next: () => {
        this.messageService.success('Password reset email sent');
        setTimeout(() => {
          this.router.navigateByUrl('/auth/login');
        }, 3000);
      },
      error: (error) => {
        if (error.status === 401) {
          this.messageService.warning('Your email needs to be verified. Check your email for a verification link.');

          setTimeout(() => {
            this.router.navigateByUrl('/auth/login');
          }, 3000);
          return;
        }

        const errorMessage = error.error?.errors?.[0]?.message || 'Failed to request password reset';
        this.messageService.error(errorMessage);
      }
    })
  }
}
