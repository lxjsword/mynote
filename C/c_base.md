---
title: C++基础
date: 2020-05-19 22:18:50
tags: C++
---
# C++基础
---
## C++基础
+ 有符号和无符号类型混用<br/>
有符号类型为负数时， 转化为无符号， 会变成变量值+无符号类型范围

```c++
//example:
int i = -1;
unsigned int ui = i;    // ui = -1 + unsigned int最大值
```

+ 声明和定义
1. 声明， 可以多次， 解决份文件编译问题
```c++
extern int i;
```
2. 定义， 只能一次
```c++
int i;      // 全局变量， 默认值为0
或 
int i = 0;
```

+ 初始化和赋值
1. 初始化， 给一个没有值的变量初始值<br/>
构造函数<br/>
拷贝构造函数<br/>
```c++
A a(1);
A b(a);
```
2. 赋值， 擦除旧值， 赋值新值<br/>
赋值构造函数
```c++
A a(1);
A b(2);
a = b;  //赋值构造函数
```

## C++编程中字符编码
+ 程序中编码分类
1. 源码文件编码<br/>
    在Windows下用VS2010新建的源码文件是GB2312编码格式。<br/>
    在Windows下用notepad++新建的源码文件是UTF-8编码格式。<br/>
    在Linux下用VI新建的源码文件是UTF-8格式。<br/><br/>
    确认文件编码： file main.c<br/>
    转换文件编码：iconv -f UTF-8 -t GB2312 main.c<br/>
2. 执行编码， 可执行文件中使用的编码, 也叫程序内码
3. 运行环境编码， 输出环境编码

+ 编码转换<br/>
![转换图](https://img-blog.csdn.net/20180925111753186?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0ZsdXNoSGlw/font/)

uincode：使用16位编码空间， 每个字符占用2个字节， 可以满足各种语言的使用， 一个字符的unicode编码是确定的，因此可以作为最为转换中间层<br/>
UTF-8: unicode的一种实现方式称为unicode转换格式, 是一种变长编码，一个字符可能占用1-3 个字节<br/>
ANSI：非unicode编码，不通国家和地区制定了不同标准, 如GB2312、GBK、GB18030、Big5、Shift_JIS 等<br/>

```c++
// UTF8<=>UNICODE
std::string UnicodeToUTF8(const std::wstring & wstr)
{
    std::string ret;
    try {
        std::wstring_convert< std::codecvt_utf8<wchar_t> > wcv;
        ret = wcv.to_bytes(wstr);
    } catch (const std::exception & e) {
        std::cerr << e.what() << std::endl;
    }
    return ret;
}

std::wstring UTF8ToUnicode(const std::string & str)
{
    std::wstring ret;
    try {
        std::wstring_convert< std::codecvt_utf8<wchar_t> > wcv;
        ret = wcv.from_bytes(str);
    } catch (const std::exception & e) {
        std::cerr << e.what() << std::endl;
    }
    return ret;
}
--------------------- 
作者：FlushHip 
来源：CSDN 
原文：https://blog.csdn.net/FlushHip/article/details/82836867 
版权声明：本文为博主原创文章，转载请附上博文链接！
```
```c++
UNICODE<=>ANSI
std::string UnicodeToANSI(const std::wstring & wstr)
{
    std::string ret;
    std::mbstate_t state = {};
    const wchar_t *src = wstr.data();
    size_t len = std::wcsrtombs(nullptr, &src, 0, &state);
    if (static_cast<size_t>(-1) != len) {
        std::unique_ptr< char [] > buff(new char[len + 1]);
        len = std::wcsrtombs(buff.get(), &src, len, &state);
        if (static_cast<size_t>(-1) != len) {
            ret.assign(buff.get(), len);
        }
    }
    return ret;
}

std::wstring ANSIToUnicode(const std::string & str)
{
    std::wstring ret;
    std::mbstate_t state = {};
    const char *src = str.data();
    size_t len = std::mbsrtowcs(nullptr, &src, 0, &state);
    if (static_cast<size_t>(-1) != len) {
        std::unique_ptr< wchar_t [] > buff(new wchar_t[len + 1]);
        len = std::mbsrtowcs(buff.get(), &src, len, &state);
        if (static_cast<size_t>(-1) != len) {
            ret.assign(buff.get(), len);
        }
    }
    return ret;
}
--------------------- 
作者：FlushHip 
来源：CSDN 
原文：https://blog.csdn.net/FlushHip/article/details/82836867 
版权声明：本文为博主原创文章，转载请附上博文链接！
```

```c++
UTF-8<=>ANSI
std::string UTF8ToANSI(const std::string & str)
{
    return UnicodeToANSI(UTF8ToUnicode(str));
}

std::string ANSIToUTF8(const std::string & str)
{
    return UnicodeToUTF8(ANSIToUnicode(str));
}
--------------------- 
作者：FlushHip 
来源：CSDN 
原文：https://blog.csdn.net/FlushHip/article/details/82836867 
版权声明：本文为博主原创文章，转载请附上博文链接！
```
<br/>

+ char和wchar_t<br/>
1. char是窄字符<br/>
2. wchar_t是宽字符， 通常以unicode(VC使用UTF-16BE，gcc使用UTF-32BE)存放