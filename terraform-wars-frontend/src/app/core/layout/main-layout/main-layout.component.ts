import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { BaseComponent } from '@app/core/components/base/base.component';
import { AuthService } from '@app/core/services/auth.service';
import { NzModalModule, NzModalService } from 'ng-zorro-antd/modal';
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { takeUntil } from 'rxjs';
import { SiderComponent } from '@app/core/layout/sider/sider.component';

@Component({
    selector: 'app-main-layout',
    imports: [RouterOutlet, NzModalModule, NzLayoutModule, SiderComponent],
    templateUrl: './main-layout.component.html',
    styleUrl: './main-layout.component.css',
})
export class MainLayoutComponent extends BaseComponent implements OnInit {
    protected authService = inject(AuthService);
    protected router = inject(Router);
    protected modalService = inject(NzModalService);

    ngOnInit(): void {
        this.authService.sessionExpired$.pipe(takeUntil(this.ngUnsubscribe$)).subscribe(() => {
            this.handleSessionExpired();
        });
    }

    handleSessionExpired() {
        this.modalService.warning({
            nzTitle: 'Your session has expired',
            nzContent: 'Your session has expired. Please log in again.',
            nzOkText: 'Log in',
            nzClosable: false,
            nzOnOk: () => {
                this.router.navigate(['/auth/login'], { queryParams: { nextUrl: this.router.url } });
            },
        });
    }
}
