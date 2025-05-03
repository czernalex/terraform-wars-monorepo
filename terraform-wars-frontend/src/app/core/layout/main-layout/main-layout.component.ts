import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { BaseComponent } from '@app/core/components/base/base.component';
import { AuthService } from '@app/core/services/auth.service';
import { takeUntil } from 'rxjs';
import { ConfirmationService } from 'primeng/api';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
@Component({
    selector: 'app-main-layout',
    imports: [RouterOutlet, ConfirmDialogModule],
    providers: [ConfirmationService],
    templateUrl: './main-layout.component.html',
    styleUrl: './main-layout.component.css',
})
export class MainLayoutComponent extends BaseComponent implements OnInit {
    protected authService = inject(AuthService);
    protected router = inject(Router);
    protected confirmationsService = inject(ConfirmationService);

    ngOnInit(): void {
        this.authService.sessionExpired$.pipe(takeUntil(this.ngUnsubscribe$)).subscribe(() => {
            this.handleSessionExpired();
        });
    }

    handleSessionExpired() {
        this.confirmationsService.confirm({
            header: $localize`Session expired`,
            icon: 'pi pi-info-circle',
            message: $localize`Your session has expired. Please log in again.`,
            acceptLabel: $localize`Log in`,
            acceptIcon: 'pi pi-sign-in',
            acceptButtonStyleClass: 'p-button-primary',
            rejectVisible: false,
            closable: false,
            accept: () => {
                this.router.navigate(['/auth/login'], { queryParams: { nextUrl: this.router.url } });
            },
        });
    }
}
