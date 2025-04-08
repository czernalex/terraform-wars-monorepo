import { TestBed } from '@angular/core/testing';
import { HttpInterceptorFn } from '@angular/common/http';

import { apiUrlInterceptor } from './api-url.interceptor';

describe('apiInterceptorInterceptor', () => {
    const interceptor: HttpInterceptorFn = (req, next) =>
        TestBed.runInInjectionContext(() => apiUrlInterceptor(req, next));

    beforeEach(() => {
        TestBed.configureTestingModule({});
    });

    it('should be created', () => {
        expect(interceptor).toBeTruthy();
    });
});
