import { HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { UserDetailSchema } from '@app/api/api/schemas';
import { UsersService } from '@app/api/api/users/users.service';
import { Subject } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    private usersService = inject(UsersService);

    protected _authenticatedUser: UserDetailSchema | null = null;

    protected sessionExpiredSubject = new Subject<void>();
    sessionExpired$ = this.sessionExpiredSubject.asObservable();

    get authenticatedUser(): UserDetailSchema | null {
        if (!this._authenticatedUser) {
            const storedUser = localStorage.getItem('authenticatedUser');
            this._authenticatedUser = storedUser ? JSON.parse(storedUser) : null;
        }

        return this._authenticatedUser;
    }

    set authenticatedUser(user: UserDetailSchema | null) {
        this._authenticatedUser = user;

        if (user) {
            localStorage.setItem('authenticatedUser', JSON.stringify(user));
        } else {
            localStorage.removeItem('authenticatedUser');
        }
    }

    isAuthenticated(): boolean {
        return !!this.authenticatedUser;
    }

    isSessionExpired(error: HttpErrorResponse, requestUrl: string): boolean {
        const EXEMPT_ROUTES = [
            '/_allauth/browser/v1/auth/signup',
            '/_allauth/browser/v1/auth/email/verify',
            `/_allauth/browser/v1/auth/password/request`,
            `/_allauth/browser/v1/auth/password/reset`,
        ];
        return error.status === 401 && !EXEMPT_ROUTES.includes(requestUrl);
    }

    setSessionExpired() {
        this.sessionExpiredSubject.next();
    }

    fetchAuthenticatedUser() {
        return this.usersService.mainAppsUsersRoutersGetMe().subscribe({
            next: (user) => {
                this.authenticatedUser = user;
            },
            error: () => {
                this.authenticatedUser = null;
            },
        });
    }
}
