import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzCheckboxModule } from 'ng-zorro-antd/checkbox';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzMessageService } from 'ng-zorro-antd/message';
import { AuthenticationAccountService } from '../../../api/allauth/authentication-account/authentication-account.service';
import { Router } from '@angular/router';
import { Login } from '../../../api/allauth/schemas';
import { AuthenticationCurrentSessionService } from '../../../api/allauth/authentication-current-session/authentication-current-session.service';
import { AuthService } from '../../../api/api/auth/auth.service';

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
    NzIconModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private authenticationAccountService = inject(AuthenticationAccountService);
  private router = inject(Router);
  private message = inject(NzMessageService);

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
    remember: [false]
  });

  passwordVisible = false;

  ngOnInit(): void {
    this.authService.mainAppsAllauthApiRoutersGetCsrfToken().subscribe();
  }

  login(): void {
    if (!this.loginForm.valid) {
      return;
    }

    this.authenticationAccountService.postAllauthBrowserV1AuthLogin(this.loginForm.value as Login).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: () => {
        this.message.error('Invalid email or password');
      }
    });
  }
}
