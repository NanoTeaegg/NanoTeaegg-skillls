# 后端/API 测试参考

用于 REST/GraphQL/RPC API、服务端业务逻辑、任务队列和集成边界。

## 工具选择

- Python: pytest, pytest-asyncio, httpx/TestClient。
- Node.js: Jest/Vitest, Supertest, MSW/Nock。
- JVM: JUnit, Spring Boot Test, Testcontainers。
- Go: 标准 `testing`、httptest、testcontainers-go。

## 编写原则

- 单元测试覆盖纯业务规则、权限判定、输入校验和错误转换。
- 集成/API 测试覆盖路由、认证授权、状态码、错误结构、数据库约束、事务行为。
- 外部服务默认 mock;关键第三方接口可以做契约测试或 sandbox smoke。
- 数据库测试优先使用事务回滚、临时 schema、Testcontainers 或项目已有测试库。
- 测试数据要可重复,不要依赖生产数据或个人账号。

## 常见目录

- `tests/unit/`
- `tests/integration/`
- `tests/api/`
- `src/**/*.test.ts`

## 常见命令

- `pytest`
- `npm test`
- `go test ./...`
- `./gradlew test`
- `mvn test`
