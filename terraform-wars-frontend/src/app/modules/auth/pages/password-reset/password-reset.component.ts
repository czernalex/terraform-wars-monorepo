import { Component, inject, Input } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthenticationPasswordResetService } from '@app/api/allauth/authentication-password-reset/authentication-password-reset.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzMessageService } from 'ng-zorro-antd/message';
import { finalize, takeUntil } from 'rxjs/operators';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzAlertModule } from 'ng-zorro-antd/alert';
import { passwordsMatchValidator } from '@app/core/validators/passwords-match-validator';

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
    NzAlertModule,
    RouterModule,
  ],
  templateUrl: './password-reset.component.html',
  styleUrl: './password-reset.component.css'
})
export class PasswordResetComponent extends BaseComponent {
  @Input() key: string = '';

  private router = inject(Router);
  private authenticationPasswordResetService = inject(AuthenticationPasswordResetService);
  private messageService = inject(NzMessageService);

  passwordResetForm = new FormGroup({
    password1: new FormControl<string>(
      '',
      { validators: [Validators.required, Validators.minLength(8)], nonNullable: true }
    ),
    password2: new FormControl<string>(
      '',
      { validators: [Validators.required, Validators.minLength(8)], nonNullable: true }
    ),
  }, { validators: [passwordsMatchValidator] });

  isRawPasswordVisible = false;
  loading = false;

  resetPassword(): void {
    if (!this.passwordResetForm.valid) {
      return;
    }

    const apiCall$ = this.authenticationPasswordResetService.postAllauthBrowserV1AuthPasswordReset({
      key: this.key,
      password: this.passwordResetForm.controls.password1.value
    });
    this.loading = true;

    apiCall$.pipe(
      takeUntil(this.ngUnsubscribe$),
      finalize(() => this.loading = false)
    ).subscribe({
      next: () => {
        this.messageService.success('Password reset successfully.');
        this.router.navigateByUrl('/auth/login');
      },
      error: (error) => {
        if (error.status === 401) {
          this.messageService.success('Password reset successfully. You can login now.');
          this.router.navigateByUrl('/auth/login');
          return;
        }

        const errorMessage = error.error?.errors?.[0]?.message || 'Failed to reset password';
        this.messageService.error(errorMessage);
      }
    });
  }
}
