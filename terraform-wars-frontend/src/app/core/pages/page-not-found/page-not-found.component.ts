import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';

@Component({
    selector: 'app-page-not-found',
    imports: [RouterModule, ButtonModule],
    templateUrl: './page-not-found.component.html',
    styleUrl: './page-not-found.component.css',
})
export class PageNotFoundComponent {}
