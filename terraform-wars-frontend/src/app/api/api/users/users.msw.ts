/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * Terraform Wars API
 * REST API for Terraform Wars application.<br><br>Authentication is managed by Django Allauth in headless mode. Open API specification is available <a href='http://localhost:8080/_allauth/openapi.html' target='_blank'>here</a>.<br><br><a href='/admin' class='btn'>Administration</a>
 * OpenAPI spec version: 0.0.1
 */
import { faker } from '@faker-js/faker';

import { HttpResponse, delay, http } from 'msw';

import type { UserDetailSchema } from '.././schemas';

export const getMainAppsUsersRoutersGetMeResponseMock = (
    overrideResponse: Partial<UserDetailSchema> = {},
): UserDetailSchema => ({
    id: faker.string.uuid(),
    email: faker.string.alpha(20),
    first_name: faker.helpers.arrayElement([faker.string.alpha(20), null]),
    last_name: faker.helpers.arrayElement([faker.string.alpha(20), null]),
    full_name: faker.string.alpha(20),
    permissions: Array.from({ length: faker.number.int({ min: 1, max: 10 }) }, (_, i) => i + 1).map(() =>
        faker.string.alpha(20),
    ),
    ...overrideResponse,
});

export const getMainAppsUsersRoutersGetMeMockHandler = (
    overrideResponse?:
        | UserDetailSchema
        | ((info: Parameters<Parameters<typeof http.get>[1]>[0]) => Promise<UserDetailSchema> | UserDetailSchema),
) => {
    return http.get('*/api/users/me/', async (info) => {
        await delay(1000);

        return new HttpResponse(
            JSON.stringify(
                overrideResponse !== undefined
                    ? typeof overrideResponse === 'function'
                        ? await overrideResponse(info)
                        : overrideResponse
                    : getMainAppsUsersRoutersGetMeResponseMock(),
            ),
            { status: 200, headers: { 'Content-Type': 'application/json' } },
        );
    });
};
export const getUsersMock = () => [getMainAppsUsersRoutersGetMeMockHandler()];
