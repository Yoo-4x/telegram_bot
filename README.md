## 安装依赖：
- [tdlib](https://github.com/tdlib/td)
    - apt-get install gcc g++ openssl zlib1g zlib1g-dev gperf cmake
    - git clone https://github.com/tdlib/td.git
    - cd cd td-*
    - mkdir build
    - cd build
    - cmake -DCMAKE_BUILD_TYPE=Release ..
        - gcc 需要 6G,解决方法二选一：
            1. Linux 可使用交换分区满足内存
            2. 换用 clang, clang++
                - apt-get install clang clang++
                - CXX=clang++ CC=clang
                - cmake -DCMAKE_BUILD_TYPE=Release ..
    - cmake --build .
    - make install
- [python-telegram](https://github.com/alexander-akhmetov/python-telegram)
    - pip3 install python-telegram(> 0.11.0), releases 编辑时最高 0.11.0，最新代码并未发行，可通过pip+github 安装，或直接替换 client.py 和 utils.py
- beautifulsoup4
    - pip3 install  beautifulsoup4

## 使用：
- 更新 config.py 内的空值
    - [登录电报](https://my.telegram.org) -> API development tools([原文](https://core.telegram.org/api/obtaining_api_id))
        - api_id
        - api_hash
        - phone
    - userId
        - python3 getUserId.py(需要将前三个数值填齐)
- 功能查询
    - 顶层功能 -> /
    - 自动回复 -> /echo
    - 小说订阅 -> /nov

## 功能：
- 自动回复
- 小说订阅(目前只支持一个网站)

在 config.py 内对功能进行增减：
- funs -> 顶层功能(增减还需要在 main.py 内增减对应的 import)
- echoFuns -> 自动回复的基础功能

## 其它：
如果有需要请直接issue
