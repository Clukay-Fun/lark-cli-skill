# 常见问题排查

英文原版: [troubleshooting.md](troubleshooting.md)

## Node.js 未安装

- 现象：`node --version` 或 `npm --version` 执行失败。
- 处理：提示用户先安装 Node.js 16 及以上版本。
- 参考：[Node.js 下载页面](https://nodejs.org/en/download)

## npm 权限不足

- 现象：`npm install -g` 或 `npm update -g` 因权限报错。
- 处理：不要自动加 `sudo`。
- 建议：让用户自行选择修复 npm 全局 prefix 配置，或自行以更高权限重试。

## 网络超时

- 现象：`npm install`、`npm update` 或 `npx skills add` 超时。
- 处理：建议检查代理设置、稍后重试，或在有需要的环境下切换 npm 镜像源。

## `lark-cli` 已安装但不在 `PATH`

- 现象：安装成功后，`lark-cli --version` 依然失败。
- 处理：检查 npm global bin 路径，并告知用户如何把它加入 `PATH`。

## Skill 目录不存在

- 现象：检测出的 skill 目录不存在。
- 处理：复制文件前先执行 `mkdir -p <SKILLS_DIR>`。

## 找不到仓库目录

- 现象：当前工作目录下没有 `lark-setup/`、`lark-sheets-extra/` 等预期目录。
- 处理：提示用户从仓库根目录运行 setup，或提供本地 checkout 路径。

## 无法识别 CLI 环境

- 现象：现有环境检测规则都不匹配。
- 处理：不要猜测目录，应提示用户手动提供目标 skill 安装目录。
