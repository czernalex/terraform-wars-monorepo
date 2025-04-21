import { Component } from '@angular/core';
import { BaseComponent } from '@app/core/components/base/base.component';
import { NzMenuModule } from 'ng-zorro-antd/menu';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { NzSelectModule } from 'ng-zorro-antd/select';

@Component({
    selector: 'app-sider',
    imports: [NzMenuModule, NzIconModule, NzLayoutModule, NzSelectModule],
    templateUrl: './sider.component.html',
    styleUrl: './sider.component.css',
})
export class SiderComponent extends BaseComponent {}
