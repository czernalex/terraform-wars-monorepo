import { Injectable, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export abstract class BaseComponent implements OnDestroy {
  protected ngUnsubscribe$ = new Subject<void>();

  ngOnDestroy(): void {
    this.ngUnsubscribe$.next();
    this.ngUnsubscribe$.complete();
    this.ngUnsubscribe$.unsubscribe();
  }
}
