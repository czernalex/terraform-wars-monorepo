/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * Terraform Wars API
 * REST API for Terraform Wars application.<br><br>Authentication is managed by Django Allauth in headless mode. Open API specification is available <a href='http://localhost:8080/_allauth/openapi.html' target='_blank'>here</a>.<br><br><a href='/admin' class='btn'>Administration</a>
 * OpenAPI spec version: 0.0.1
 */
import { HttpResponse, delay, http } from 'msw';

export const getMainAppsApiAuthRoutersGetCsrfTokenMockHandler = (
    overrideResponse?: void | ((info: Parameters<Parameters<typeof http.post>[1]>[0]) => Promise<void> | void),
) => {
    return http.post('*/api/auth/csrf/', async (info) => {
        await delay(1000);
        if (typeof overrideResponse === 'function') {
            await overrideResponse(info);
        }
        return new HttpResponse(null, { status: 204 });
    });
};
export const getAuthMock = () => [getMainAppsApiAuthRoutersGetCsrfTokenMockHandler()];
