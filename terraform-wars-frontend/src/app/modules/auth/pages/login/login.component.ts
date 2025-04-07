import { Component, inject } from '@angular/core';
import { Validators, FormsModule, ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzCheckboxModule } from 'ng-zorro-antd/checkbox';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzMessageService } from 'ng-zorro-antd/message';
import { NzCardModule } from 'ng-zorro-antd/card';
import { AuthenticationAccountService } from '@app/api/allauth/authentication-account/authentication-account.service';
import { BaseComponent } from '@app/core/components/base/base.component';
import { finalize, takeUntil } from 'rxjs/operators';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { AuthService } from '@app/core/services/auth.service';
import { UsersService } from '@app/api/api/users/users.service';
@Component({
  selector: 'app-login',
  imports: [
    FormsModule,
    ReactiveFormsModule,
    NzFormModule,
    NzInputModule,
    NzButtonModule,
    NzCheckboxModule,
    NzTypographyModule,
    NzIconModule,
    NzCardModule,
    RouterModule,
    NzDividerModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent extends BaseComponent {
  private authenticationAccountService = inject(AuthenticationAccountService);
  private usersService = inject(UsersService);
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private messageService = inject(NzMessageService);

  loginForm = new FormGroup({
    email: new FormControl<string>('', { validators: [Validators.required, Validators.email], nonNullable: true }),
    password: new FormControl<string>('', { validators: [Validators.required, Validators.minLength(8)], nonNullable: true }),
    remember: new FormControl<boolean>(false, { nonNullable: true })
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
      // @ts-ignore
      remember: this.loginForm.controls.remember.value,
    });
    this.loading = true;

    apiCall$.pipe(
      takeUntil(this.ngUnsubscribe$),
      finalize(() => this.loading = false)
    ).subscribe({
      next: () => {
        this.messageService.success('You were successfully logged in', { nzDuration: 5000 });

        this.usersService.mainAppsUsersRoutersGetMe().subscribe({
          next: (user) => {
            this.authService.authenticatedUser = user;
            this.router.navigateByUrl(this.getNextUrl());
          },
          error: (error) => {
            this.messageService.error('Failed to get user details');
          }
        });
      },
      error: (error) => {
        if (error.status === 401) {
          this.messageService.warning('Your email needs to be verified. Check your email for a verification link.', { nzDuration: 5000 });
          return;
        }

        const errorMessage = error.error?.errors?.[0]?.message || 'Failed to log in';
        this.messageService.error(errorMessage);
      }
    });
  }
}
