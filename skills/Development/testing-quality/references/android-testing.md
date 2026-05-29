# Android 测试参考

用于 Kotlin/Java Android app、Jetpack Compose 或传统 View 项目。

## 工具选择

- 单元测试: JUnit、MockK/Mockito、Robolectric(需要 Android framework 行为时)。
- UI/仪器化测试: Espresso 或 Compose UI Test。
- 自动化运行: Gradle `test`、`connectedAndroidTest`、CI 设备池(如已有)。

## 编写原则

- 单元测试覆盖领域逻辑、ViewModel、校验、状态 reducer。
- UI 测试覆盖 P0 用户路径和高风险错误态。
- Compose 项目优先使用 semantic matcher/test tag;传统 View 项目使用 resource id/content description。
- 外部服务通过 fake repository、mock web server 或依赖注入替换。
- PR 阶段优先跑 JVM 单元测试和少量关键仪器化测试;完整设备矩阵放到 nightly 或发布前。

## 常见目录

- `app/src/test/` -> JVM 单元测试
- `app/src/androidTest/` -> 仪器化/UI 测试

## 常见命令

- `./gradlew test`
- `./gradlew testDebugUnitTest`
- `./gradlew connectedDebugAndroidTest`
