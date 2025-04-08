module.exports = {
    allauth: {
        output: {
            mode: 'tags-split',
            target: './src/app/api/allauth',
            schemas: './src/app/api/allauth/schemas',
            client: 'angular',
            mock: true,
        },
        input: {
            target: 'http://127.0.0.1:8080/_allauth/openapi.json',
        },
    },
    api: {
        output: {
            mode: 'tags-split',
            target: './src/app/api/api',
            schemas: './src/app/api/api/schemas',
            client: 'angular',
            mock: true,
        },
        input: {
            target: 'http://127.0.0.1:8080/api/openapi.json',
        },
    },
};
