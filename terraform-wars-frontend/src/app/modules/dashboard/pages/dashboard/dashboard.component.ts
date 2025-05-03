import { Component } from '@angular/core';
import { BaseComponent } from '@app/core/components/base/base.component';
import { ButtonModule } from 'primeng/button';

@Component({
    selector: 'app-dashboard',
    imports: [ButtonModule],
    templateUrl: './dashboard.component.html',
    styleUrl: './dashboard.component.css',
})
export class DashboardComponent extends BaseComponent {}
