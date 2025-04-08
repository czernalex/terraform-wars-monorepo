/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * Terraform Wars API
 * REST API for Terraform Wars application.<br><br>Authentication is managed by Django Allauth in headless mode. Open API specification is available <a href='http://localhost:8080/_allauth/openapi.html' target='_blank'>here</a>.<br><br><a href='/admin' class='btn'>Administration</a>
 * OpenAPI spec version: 0.0.1
 */
import type { TutorialGroupState } from './tutorialGroupState';

export interface TutorialGroupListSchema {
    id: string;
    state: TutorialGroupState;
    tutorial_count: number;
    /** @maxLength 255 */
    title: string;
    description: string;
}
