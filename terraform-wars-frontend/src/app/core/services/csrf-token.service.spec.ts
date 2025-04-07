import { TestBed } from '@angular/core/testing';

import { CsrfTokenService } from './csrf-token.service';

describe('CsrfTokenService', () => {
  let service: CsrfTokenService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CsrfTokenService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
