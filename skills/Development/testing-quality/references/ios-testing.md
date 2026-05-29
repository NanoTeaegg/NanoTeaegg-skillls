# iOS 测试参考

用于 Swift/Objective-C iOS app、SwiftUI/UIKit 项目。

## 工具选择

- 单元测试: XCTest 或 Swift Testing(如果项目已采用)。
- UI 测试: XCUITest。
- 自动化运行: `xcodebuild test` 或 fastlane `scan`(如果项目已有 fastlane)。

## 编写原则

- 单元测试覆盖领域逻辑、格式化、校验、ViewModel/Reducer 等不依赖 UI 的逻辑。
- UI 测试覆盖 P0 用户路径,例如登录、核心提交、关键错误态。
- 使用 accessibility identifier/label 作为稳定定位;必要时在 TEST_PLAN 中记录需要开发补充的可访问性标识,不要擅自改业务代码。
- 控制模拟器矩阵:至少覆盖当前最低支持版本和主流版本;不要在 PR 上跑过大的设备矩阵。
- 外部网络请求用 mock server、URLProtocol stub 或项目已有测试 doubles。

## 常见目录

- `<AppName>Tests/` -> 单元测试
- `<AppName>UITests/` -> XCUITest

## 常见命令

- `xcodebuild test -scheme <Scheme> -destination 'platform=iOS Simulator,name=iPhone 15'`
- `bundle exec fastlane scan`(如果项目已有 fastlane)
