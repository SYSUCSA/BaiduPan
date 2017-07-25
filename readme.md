# BaiduPan
## 项目说明
一个使用python操作百度网盘的项目，项目可能会大量参考已有代码，解决安全性等问题。本项目旨在实现上传、保存他人分享文件等主要功能，从而达到使用百度网盘作为数据服务器的目的，而非实现一个百度网盘客户端。

## 类似项目
存在较为成熟的项目，如
* [houtianze/bypy](https://github.com/houtianze/bypy)
* [ly0/baidupcsapi](https://github.com/ly0/baidupcsapi)

不直接使用的原因是
1. bypy使用的登录操作不可靠(如百度更改登录规则需要重新修改登录逻辑)
2. baidupcsapi会向作者的域名提交token，不确定是否安全。
