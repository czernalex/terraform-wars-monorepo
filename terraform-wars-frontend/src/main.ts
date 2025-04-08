import { bootstrapApplication } from '@angular/platform-browser';
import * as Sentry from '@sentry/angular';

import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

Sentry.init({
    dsn: 'https://d3ed2738471fef968a98973b58726394@o4507624653520896.ingest.de.sentry.io/4509112592171088',
});

bootstrapApplication(AppComponent, appConfig).catch((err) => console.error(err));
