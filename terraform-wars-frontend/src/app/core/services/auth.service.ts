import { Injectable, inject } from '@angular/core';
import { UserDetailSchema } from '@app/api/api/schemas';
import { UsersService } from '@app/api/api/users/users.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private usersService = inject(UsersService);

  _authenticatedUser: UserDetailSchema | null = null;

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

  fetchAuthenticatedUser() {
    console.log('fetching authenticated user');
    return this.usersService.mainAppsUsersRoutersGetMe().subscribe({
      next: (user) => {
        this.authenticatedUser = user;
      },
      error: () => {
        this.authenticatedUser = null;
      }
    });
  }
}
