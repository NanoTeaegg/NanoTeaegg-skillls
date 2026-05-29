# Web 测试参考

用于 Web 前端、全栈 Web、管理后台、SaaS 产品。

## 工具选择

- 已有 Vitest/Jest/Testing Library 时,优先沿用做单元/组件测试。
- 已有 Playwright/Cypress 时,优先沿用做 E2E;新建时优先 Playwright,因为它自带自动等待、trace 和多浏览器能力。
- 需要轻量性能 smoke/load 时,优先 k6;需要页面级交互性能时,可以补 Playwright trace 或 Lighthouse 类检查。

## 编写原则

- 以用户行为为中心:优先使用 role、label、text、test id 等稳定定位,避免依赖 CSS 层级。
- E2E 只覆盖 P0 主路径和高风险异常路径,不要把所有分支都塞进 UI 自动化。
- 组件测试覆盖表单校验、权限展示、空态/错误态、关键交互反馈。
- API/集成测试覆盖认证、授权、错误码、幂等、数据边界。
- 外部服务(支付、短信、邮件、第三方 API)默认 mock;如有测试环境,保留少量契约/冒烟验证。

## 常见目录

- `src/**/*.test.ts(x)` 或 `__tests__/` -> 单元/组件测试
- `tests/` -> API/集成测试
- `e2e/*.spec.ts` 或 `tests/e2e/*.spec.ts` -> Playwright E2E
- `performance/*.js` 或 `tests/performance/*.js` -> k6 脚本

## 常见命令

- `npm test` / `pnpm test` / `yarn test`
- `npm run test:unit`
- `npm run test:e2e`
- `npx playwright test`
- `k6 run tests/performance/*.js`

## 参考来源

- Playwright best practices: https://playwright.dev/docs/best-practices
- Testing Library guiding principles: https://testing-library.com/docs/guiding-principles
