import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NzLayoutModule } from 'ng-zorro-antd/layout';

@Component({
    selector: 'app-auth-layout',
    imports: [RouterOutlet, NzLayoutModule],
    templateUrl: './auth-layout.component.html',
    styleUrl: './auth-layout.component.css',
})
export class AuthLayoutComponent {}
