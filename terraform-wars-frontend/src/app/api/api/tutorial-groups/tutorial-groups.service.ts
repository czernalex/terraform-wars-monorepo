/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * Terraform Wars API
 * REST API for Terraform Wars application.<br><br>Authentication is managed by Django Allauth in headless mode. Open API specification is available <a href='http://localhost:8080/_allauth/openapi.html' target='_blank'>here</a>.<br><br><a href='/admin' class='btn'>Administration</a>
 * OpenAPI spec version: 0.0.1
 */
import { HttpClient } from '@angular/common/http';
import type {
    HttpContext,
    HttpEvent,
    HttpHeaders,
    HttpParams,
    HttpResponse as AngularHttpResponse,
} from '@angular/common/http';

import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import type {
    CreateTutorialGroupSchema,
    MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsParams,
    PagedTutorialGroupListSchema,
    TutorialGroupDetailSchema,
    UpdateTutorialGroupSchema,
} from '.././schemas';

interface HttpClientOptions {
    headers?: HttpHeaders | Record<string, string | string[]>;
    context?: HttpContext;
    observe?: any;
    params?: HttpParams | Record<string, string | number | boolean | readonly (string | number | boolean)[]>;
    reportProgress?: boolean;
    responseType?: any;
    withCredentials?: boolean;
}

@Injectable({ providedIn: 'root' })
export class TutorialGroupsService {
    constructor(private http: HttpClient) {} /**
     * Get the tutorial groups.
     * @summary Get Tutorial Groups
     */
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroups<TData = PagedTutorialGroupListSchema>(
        params?: MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsParams,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' },
    ): Observable<TData>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroups<TData = PagedTutorialGroupListSchema>(
        params?: MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsParams,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' },
    ): Observable<AngularHttpResponse<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroups<TData = PagedTutorialGroupListSchema>(
        params?: MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsParams,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' },
    ): Observable<HttpEvent<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroups<TData = PagedTutorialGroupListSchema>(
        params?: MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsParams,
        options?: HttpClientOptions,
    ): Observable<TData> {
        return this.http.get<TData>(`/api/tutorial-groups/`, {
            ...options,
            params: { ...params, ...options?.params },
        });
    }
    /**
     * Create a new tutorial group.
     * @summary Create Tutorial Group
     */
    mainAppsTutorialsRoutersTutorialGroupRouterCreateTutorialGroup<TData = TutorialGroupDetailSchema>(
        createTutorialGroupSchema: CreateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' },
    ): Observable<TData>;
    mainAppsTutorialsRoutersTutorialGroupRouterCreateTutorialGroup<TData = TutorialGroupDetailSchema>(
        createTutorialGroupSchema: CreateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' },
    ): Observable<AngularHttpResponse<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterCreateTutorialGroup<TData = TutorialGroupDetailSchema>(
        createTutorialGroupSchema: CreateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' },
    ): Observable<HttpEvent<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterCreateTutorialGroup<TData = TutorialGroupDetailSchema>(
        createTutorialGroupSchema: CreateTutorialGroupSchema,
        options?: HttpClientOptions,
    ): Observable<TData> {
        return this.http.post<TData>(`/api/tutorial-groups/`, createTutorialGroupSchema, options);
    }
    /**
     * Get the tutorial group by its ID.
     * @summary Get Tutorial Group
     */
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' },
    ): Observable<TData>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' },
    ): Observable<AngularHttpResponse<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' },
    ): Observable<HttpEvent<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        options?: HttpClientOptions,
    ): Observable<TData> {
        return this.http.get<TData>(`/api/tutorial-groups/${tutorialGroupId}/`, options);
    }
    /**
     * Update the tutorial group.
     * @summary Update Tutorial Group
     */
    mainAppsTutorialsRoutersTutorialGroupRouterUpdateTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        updateTutorialGroupSchema: UpdateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' },
    ): Observable<TData>;
    mainAppsTutorialsRoutersTutorialGroupRouterUpdateTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        updateTutorialGroupSchema: UpdateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' },
    ): Observable<AngularHttpResponse<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterUpdateTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        updateTutorialGroupSchema: UpdateTutorialGroupSchema,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' },
    ): Observable<HttpEvent<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterUpdateTutorialGroup<TData = TutorialGroupDetailSchema>(
        tutorialGroupId: string,
        updateTutorialGroupSchema: UpdateTutorialGroupSchema,
        options?: HttpClientOptions,
    ): Observable<TData> {
        return this.http.put<TData>(`/api/tutorial-groups/${tutorialGroupId}/`, updateTutorialGroupSchema, options);
    }
    /**
     * Delete the tutorial group.
     * @summary Delete Tutorial Group
     */
    mainAppsTutorialsRoutersTutorialGroupRouterDeleteTutorialGroup<TData = void>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'body' },
    ): Observable<TData>;
    mainAppsTutorialsRoutersTutorialGroupRouterDeleteTutorialGroup<TData = void>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'response' },
    ): Observable<AngularHttpResponse<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterDeleteTutorialGroup<TData = void>(
        tutorialGroupId: string,
        options?: Omit<HttpClientOptions, 'observe'> & { observe?: 'events' },
    ): Observable<HttpEvent<TData>>;
    mainAppsTutorialsRoutersTutorialGroupRouterDeleteTutorialGroup<TData = void>(
        tutorialGroupId: string,
        options?: HttpClientOptions,
    ): Observable<TData> {
        return this.http.delete<TData>(`/api/tutorial-groups/${tutorialGroupId}/`, options);
    }
}

export type MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupsClientResult =
    NonNullable<PagedTutorialGroupListSchema>;
export type MainAppsTutorialsRoutersTutorialGroupRouterCreateTutorialGroupClientResult =
    NonNullable<TutorialGroupDetailSchema>;
export type MainAppsTutorialsRoutersTutorialGroupRouterGetTutorialGroupClientResult =
    NonNullable<TutorialGroupDetailSchema>;
export type MainAppsTutorialsRoutersTutorialGroupRouterUpdateTutorialGroupClientResult =
    NonNullable<TutorialGroupDetailSchema>;
export type MainAppsTutorialsRoutersTutorialGroupRouterDeleteTutorialGroupClientResult = NonNullable<void>;
