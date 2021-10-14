# opensearch index rotate tool

#### 开发环境
```
Python  3.8.12
```
#### 编译
* 构建并推送镜像
```shell
docker build -t "<registry_address>/<app_name>:<tag>" .
docker push "<registry_address>/<app_name>:<tag>"
```
#### 运行
* 直接运行
```
python main.py --host opensearch.domain.com --days-ago 10 --index "pd*"
```
* on docker
```
docker run --rm <registry_address>/<app_name>:<tag> --host opensearch.domain.com --days-ago 10 --index "pd*"
```
#### 运行参数

| 参数 | 描述 |
| ------------- | ------------- |
| --host | opensaerch 域名 |
| --days-ago | 删除多少天以前的索引  |
| --index | 索引名称,支持通配符 |
#### 单元测试
```
python -m unittest test_main 
```