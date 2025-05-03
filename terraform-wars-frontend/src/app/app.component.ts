import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
@Component({
    selector: 'app-root',
    imports: [RouterOutlet, ToastModule],
    providers: [MessageService],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css',
})
export class AppComponent {
    title = 'terraform-wars';
}
