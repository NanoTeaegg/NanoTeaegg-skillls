# 性能与安全基线参考

用于把技术风险转成可执行的轻量检查。它不能替代专业压测、安全审计或渗透测试。

## 性能测试

- Smoke: 少量并发确认关键接口/页面在测试环境中可用。
- Load: 模拟预期负载,验证响应时间和错误率阈值。
- Stress: 逐步提高负载,观察系统何时退化。
- Soak: 长时间运行,观察内存泄漏、连接耗尽和稳定性。

第一版测试计划通常只生成 smoke 或小规模 load 脚本,并把真实容量压测列为非目标或开放问题。

## 安全基线

可以覆盖:

- 未登录/权限不足路径
- 越权访问关键资源
- 输入校验与错误信息泄漏
- CSRF/XSS/SQL injection 的基础回归用例(按项目类型选择)
- 敏感信息不出现在日志、响应或前端包中

不要承诺完整安全审计。需要专业安全测试时,在 TEST_PLAN 中列为下游动作。

## 参考来源

- k6 documentation: https://grafana.com/docs/k6/latest/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
