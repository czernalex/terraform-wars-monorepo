/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * Terraform Wars API
 * REST API for Terraform Wars application.<br><br>Authentication is managed by Django Allauth in headless mode. Open API specification is available <a href='http://127.0.0.1:8080/_allauth/openapi.html' target='_blank'>here</a>.<br><br><a href='/admin' class='btn'>Administration</a>
 * OpenAPI spec version: 0.0.1
 */
import {
  HttpClient
} from '@angular/common/http';
import type {
  HttpContext,
  HttpEvent,
  HttpHeaders,
  HttpParams,
  HttpResponse as AngularHttpResponse
} from '@angular/common/http';

import {
  Injectable
} from '@angular/core';

import {
  Observable
} from 'rxjs';

import type {
  UserDetailSchema
} from '.././schemas';



type HttpClientOptions = {
  headers?: HttpHeaders | {
      [header: string]: string | string[];
  };
  context?: HttpContext;
  observe?: any;
  params?: HttpParams | {
    [param: string]: string | number | boolean | ReadonlyArray<string | number | boolean>;
  };
  reportProgress?: boolean;
  responseType?: any;
  withCredentials?: boolean;
};



@Injectable({ providedIn: 'root' })
export class UsersService {
  constructor(
    private http: HttpClient,
  ) {}/**
 * Get the current user
 * @summary Get Me
 */
 mainAppsUsersRoutersGetMe<TData = UserDetailSchema>(
     options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' }
  ): Observable<TData>;
    mainAppsUsersRoutersGetMe<TData = UserDetailSchema>(
     options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' }
  ): Observable<AngularHttpResponse<TData>>;
    mainAppsUsersRoutersGetMe<TData = UserDetailSchema>(
     options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' }
  ): Observable<HttpEvent<TData>>;mainAppsUsersRoutersGetMe<TData = UserDetailSchema>(
     options?: HttpClientOptions
  ): Observable<TData>  {
    return this.http.get<TData>(
      `/api/users/me/`,options
    );
  }
};

export type MainAppsUsersRoutersGetMeClientResult = NonNullable<UserDetailSchema>
