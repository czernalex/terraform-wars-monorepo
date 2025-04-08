import { HttpEvent, HttpRequest, HttpHandlerFn } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@env/environment';

export function apiUrlInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
    req = req.clone({
        url: `${environment.baseApiUrl}${req.url}`,
    });

    return next(req);
}
