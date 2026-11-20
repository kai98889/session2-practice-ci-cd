# 自动训练与发布：GitHub Actions CI/CD

本项目用工作年限与工资数据训练线性回归模型。修改数据并推送到 `main` 后，GitHub Actions 自动测试、训练，将参数保存到 `release` 分支，并发布可下载的新版本。

## 文件

- `training_data.csv`：课程提供的 30 条训练数据，加 1 条用于验证自动更新的教学示例数据（11 年、126000）。
- `train_model.py`：训练并生成 `linear_model.txt` 和 `linear_model.pkl`。
- `requirements.txt`：Python 依赖。
- `test_train_model.py`：验证训练结果、模型导出和错误数据处理。
- `.github/workflows/ci-cd.yml`：自动训练与发布流程。

## 本地运行

需要 Python 3.12：

```bash
python -m pip install -r requirements.txt
python -m unittest -v
python train_model.py
```

## 自动流程

1. 首次推送，以及修改数据、训练代码、测试、依赖或工作流后推送到 `main`，自动测试并训练。
2. Pull Request 运行测试和训练；发布在推送到 `main` 后执行。
3. 训练产物先保存为 Actions artifact。
4. 发布任务自动创建或更新 `release` 分支，其中只有 `linear_model.txt`。
5. 创建对应发布提交的版本标签，Release 附带参数文件和模型文件。
6. 同一次运行重试使用新的版本后缀，避免标签冲突。

也可从 **Actions → CI/CD Pipeline → Run workflow** 手动执行。

## 验收

修改 `training_data.csv`，例如追加一行 `11.0,126000.00`，提交并推送到 `main`。检查：

- **Actions**：训练和发布任务均成功。
- **release 分支**：包含新的 `linear_model.txt`。
- **Releases**：包含自动生成的版本，以及 `linear_model.txt`、`linear_model.pkl` 附件。

完成后提交自己的 GitHub 仓库链接。

## 相对课程示例的修正

使用路径过滤触发数据相关更新，避免首次推送和 Pull Request 中不存在的比较提交导致跳过训练。发布任务仅在 `main` 上运行并单独申请写权限；自动创建发布分支，保留发布历史；版本标签明确指向发布提交。Python 使用 3.12，适配当前依赖。
