## Frontend Unit Testing (.test.js) with Jest
### Goal:
This document explains how to set up and run frontend unit tests for like-toggle.js and modal.js using Jest.
Only the steps that were successfully tested are included.

## Install Node.js
Download and install Node.js from the official website:
https://nodejs.org/

Verify installation:

```
node -v
npm -v
```

## Initialize npm project
In your project root directory:

```
npm init -y
```

This will create a package.json file.

## Install Required Packages

```
npm install --save-dev jest @testing-library/dom @testing-library/jest-dom jest-environment-jsdom babel-jest @babel/preset-env
```

## (Optional but recommended) Initialize Jest configuration wizard

If this is your first Jest setup, you can use the official initialization wizard:

```
npx jest --init
```

Suggested answers:

Question	Recommended Answer
Would you like to use Typescript?	No
Use Babel for JavaScript files?	Yes
Test environment	jsdom
Add coverage reports?	Yes
Automatically clear mocks between tests?	Yes

This will create a jest.config.js file.

## Configure Babel
Create a file babel.config.js in the root:

```
module.exports = {
  presets: [['@babel/preset-env', { targets: { node: 'current' } }]],
};
```

## Configure Babel manually
Even if you used jest --init, you must add Babel config for import/export syntax:

```
npm install --save-dev babel-jest @babel/preset-env
```

Create babel.config.js:

```
module.exports = {
  presets: [['@babel/preset-env', { targets: { node: 'current' } }]],
};
```

## Configure Jest
Create a file jest.config.js in the root:

```
module.exports = {
  testEnvironment: 'jsdom',
  clearMocks: true,
  coverageDirectory: 'coverage'
};
```

## Update package.json Scripts
In your package.json, add:

```
"scripts": {
  "test": "jest --watchAll"
}
```

## Folder Reference
This section outlines the relevant frontend-related folders and configuration files used for testing interactive JavaScript features.

```
project-root/
├── static/
│   └── js/
│       ├── like-toggle.js     # Handles AJAX like/unlike
│       ├── modal.js           # Fullscreen image modal with navigation
│       ├── post-menu.js       # Post dropdown toggle
│       └── post-time.js       # Formats UTC timestamps to local time
│
├── tests/
│   └── frontend/              # Optional location for Jest unit tests
│
├── jest.config.js             # Jest configuration file
├── babel.config.js            # Transpiles ES6+ JavaScript for Jest
├── package.json               # Includes test scripts and dependencies
```

#### Notes

- static/js/ contains standalone scripts directly used in templates via <script> tags.
- All JavaScript is written in modular, testable form (Vanilla JS + DOM APIs).
- You can group Jest tests under tests/frontend/ or collocate them (e.g., like-toggle.test.js next to the source file).
- babel.config.js ensures compatibility with Jest by transpiling ES6+ syntax.

## Specific Adjustments That Worked

like-toggle.test.js
Mock fetch.

Handle csrftoken.

Simulate button clicks.

Trigger DOMContentLoaded manually to initialize event listeners:

```
document.dispatchEvent(new Event('DOMContentLoaded'));
```

Silence console.error in the error test:

```
jest.spyOn(console, 'error').mockImplementation(() => {});
modal.test.js
Mock MicroModal.show() and MicroModal.close().
```

Ensure correct import path:

```
require('../../static/js/modal.js');
```

Trigger DOMContentLoaded after require:

```
require('../../static/js/modal.js');
document.dispatchEvent(new Event('DOMContentLoaded'));
```

## Running Tests
To run the unit tests:

```
npm run test 
```

## Generating Coverage Report
For code coverage results:

```
npm run test -- --coverage
```

### Open HTML Coverage Report (Visual)
Jest also generates a visual HTML report with highlighted uncovered lines.

To open it:

```
start coverage/lcov-report/index.html
```
