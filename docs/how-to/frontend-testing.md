---
title: How to Test the Frontend
tags: [testing, vitest, vue-test-utils, components]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# How to Test the Frontend

We use **Vitest** and **Vue Test Utils** for fast, reliable component testing.

## 1. Installation
Install the testing suite as development dependencies:
```bash
npm install -D vitest @vue/test-utils jsdom
```

## 2. Configuration (`vite.config.js`)
Ensure Vite is aware of the test environment:
```javascript
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true
  }
})
```

## 3. Writing a Component Test
Create a test file matching your component name (e.g., `tests/components/PokerCard.test.js`):

```javascript
import { mount } from '@vue/test-utils';
import { expect, test } from 'vitest';
import PokerCard from '../../src/components/atomic/PokerCard.vue';

test('renders card rank and suit', () => {
  const wrapper = mount(PokerCard, {
    props: {
      rank: 'A',
      suit: 's'
    }
  });

  expect(wrapper.text()).toContain('A');
  expect(wrapper.classes()).toContain('suit-spades');
});
```

## 4. Running Tests

### Run all tests
```bash
npm run test
```

### Watch mode (Re-runs on change)
```bash
npx vitest
```

### Coverage Report
To see which parts of your UI are untested:
```bash
npx vitest run --coverage
```
