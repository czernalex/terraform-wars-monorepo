import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NzResultModule } from 'ng-zorro-antd/result';
import { NzButtonModule } from 'ng-zorro-antd/button';

@Component({
  selector: 'app-page-not-found',
  imports: [NzResultModule, NzButtonModule, RouterModule],
  templateUrl: './page-not-found.component.html',
  styleUrl: './page-not-found.component.css'
})
export class PageNotFoundComponent {
}
