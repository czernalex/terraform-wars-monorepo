import { HttpInterceptorFn } from '@angular/common/http';

export const apiErrorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req);
};
