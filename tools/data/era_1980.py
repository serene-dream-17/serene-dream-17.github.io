# -*- coding: utf-8 -*-
"""第二批 · 1980s：9 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"cpp": {
    "tagline": "C 加上类、模板与异常，成为性能与复杂度并存的那门语言。",
    "intro": [
        "1979 年，Bjarne Stroustrup 在贝尔实验室开始给 C 加「带类的 C」；1983 年它被命名为 C++，1985 年第一版商业实现与《The C++ Programming Language》一起出现。它的目标很直接：保留 C 的布局与性能，同时支持抽象。",
        "C++ 的产物链在 C 的五个阶段上多了两样东西：名字修饰（name mangling）与静态初始化。同一个 hello 程序，目标文件里会出现被修饰的 operator<< 符号、异常展开表 .eh_frame，以及一个在 main 之前运行的全局构造函数。",
        "1998 年的 ISO 标准把 STL、模板、异常、RTTI 固定下来；此后的 C++11/14/17/20 继续往语言里加东西。C++ 的复杂度，基本都能在这条产物链上找到对应物。",
    ],
    "lineage": {
        "from": ["C", "Simula 67", "ALGOL 68"],
        "to": ["Java", "C#", "Rust", "Go（部分设计反思）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.cpp",
            "cmd": "$ cat hello.cpp",
            "code": r"""#include <iostream>

int main() {
    std::cout << "Hello, world\n";
    return 0;
}""",
            "format": [
                ("扩展名", ".cpp / .cc / .cxx"),
                ("头文件", "<iostream>，标准库模板"),
                ("命名空间", "std::"),
                ("入口", "main，由 C++ 运行时调用"),
            ],
            "note": "iostream 不是一个函数库，而是一组模板与全局对象。`std::cout` 是一个在程序启动前构造出来的 ostream 实例。",
        },
        {
            "label": "预处理",
            "file": "hello.ii",
            "cmd": "$ g++ -E hello.cpp -o hello.ii",
            "code": r"""# 1 "hello.cpp"
# 1 "/usr/include/c++/13/iostream" 1 3
# 1 "/usr/include/c++/13/bits/c++config.h" 1 3
...
namespace std _GLIBCXX_VISIBILITY(default)
{
...
  extern ostream cout;
...
}
# 3 "hello.cpp" 2

int main() {
    std::cout << "Hello, world\n";
    return 0;
}""",
            "format": [
                ("扩展名", ".ii，预处理后的 C++ 文本"),
                ("体量", "一个 hello 可展开到 1 MB 以上"),
                ("内容", "模板定义、内联函数、声明全部就位"),
                ("行标记", "指回原始头文件与行号"),
            ],
            "note": "C++ 的编译单元比 C 大得多，因为标准库头文件里有大量模板与内联代码。预处理器仍然是文本替换，不理解模板。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "$ g++ -S -O0 hello.cpp -o hello.s",
            "code": r"""    .section    .rodata
.LC0:
    .string "Hello, world"
    .text
    .globl  main
    .type   main, @function
main:
    pushq   %rbp
    movq    %rsp, %rbp
    leaq    .LC0(%rip), %rsi
    leaq    _ZSt4cout(%rip), %rdi
    call    _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
    movl    $0, %eax
    popq    %rbp
    ret
    .section    .init_array,"aw"
    .quad   _GLOBAL__sub_I_main""",
            "format": [
                ("名字修饰", "operator<< 被编码成 _ZStlsISt11..."),
                ("结果", "返回 ostream 引用，可继续 <<"),
                ("静态初始化", ".init_array 指向全局构造函数"),
                ("异常", "汇编里还会生成 .eh_frame 展开表"),
            ],
            "note": "`_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc` 是 `std::operator<<(std::ostream&, char const*)` 的 Itanium ABI 名字。链接器靠它找到 libstdc++ 里的实现。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ g++ -c hello.cpp && nm -C hello.o",
            "code": r"""$ nm -C hello.o
0000000000000000 T main
                 U std::basic_ostream<char, std::char_traits<char> >&
                   std::operator<< <std::char_traits<char> >(
                     std::basic_ostream<char, ...>&, char const*)
                 U std::ios_base::Init::Init()
                 U __cxa_atexit

$ readelf -S hello.o | grep -E 'eh_frame|init_array|rela'
  [ 5] .rela.text   RELA
  [ 8] .eh_frame   PROGBITS
  [10] .init_array INIT_ARRAY""",
            "format": [
                ("符号", "main 已定义，operator<< 未定义（U）"),
                ("异常表", ".eh_frame 记录栈展开信息"),
                ("静态初始化", ".init_array 调用全局构造"),
                ("重定位", ".rela.text 交给链接器解析"),
            ],
            "note": "C++ 目标文件比 C 多了异常展开表与静态初始化数组。`std::ios_base::Init` 保证 iostream 在被使用前已初始化。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ g++ -o hello hello.cpp && ldd hello",
            "code": r"""$ ldd hello
  libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6
  libgcc_s.so.1  => /lib/x86_64-linux-gnu/libgcc_s.so.1
  libc.so.6      => /lib/x86_64-linux-gnu/libc.so.6

$ readelf -d hello | grep NEEDED
  NEEDED  libstdc++.so.6
  NEEDED  libgcc_s.so.1
  NEEDED  libc.so.6

$ ./hello
Hello, world""",
            "format": [
                ("类型", "ELF64 · ET_DYN（PIE）"),
                ("依赖", "libstdc++ / libgcc_s / libc"),
                ("启动", "_start → __libc_start_main → main"),
                ("全局构造", "main 之前执行 .init_array"),
            ],
            "note": "C++ 程序在 main 之前已经跑过一段代码：全局对象构造、iostream 初始化、异常运行时注册。这些都由链接进来的运行时完成。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "vi / Emacs", "compiler": "cfront（C++ → C）", "build": "make", "pkg": "—", "debug": "adb"},
        {"era": "1990s", "editor": "Emacs / Visual C++ IDE", "compiler": "g++ / MSVC", "build": "make / nmake", "pkg": "—", "debug": "gdb / MSVC debugger"},
        {"era": "2000s", "editor": "Eclipse CDT / vim", "compiler": "g++ / clang++", "build": "make / CMake", "pkg": "pkg-config", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + clangd", "compiler": "clang++ / g++ / MSVC", "build": "CMake / Bazel", "pkg": "vcpkg / Conan", "debug": "lldb / gdb"},
    ],
    "hello": {
        "file": "hello.cpp",
        "code": r"""#include <iostream>

int main() {
    std::cout << "Hello, world\n";
}""",
        "footprint": [
            {"stage": "hello.cpp", "size": "≈ 100 B", "w": 4},
            {"stage": "hello.ii", "size": "≈ 1.1 MB", "w": 80},
            {"stage": "hello.s", "size": "≈ 2.3 KB", "w": 12},
            {"stage": "hello.o", "size": "≈ 3.1 KB", "w": 14},
            {"stage": "hello", "size": "≈ 18 KB", "w": 28},
            {"stage": "+ libstdc++", "size": "≈ 2 MB", "w": 100},
        ],
        "why": [
            "<strong>头文件与模板</strong>：iostream 的实现大量在头文件里，预处理器把它们全部倒进编译单元。",
            "<strong>名字修饰</strong>：重载、命名空间、模板需要把类型信息编码进符号名，链接器才能区分。",
            "<strong>静态初始化</strong>：全局对象必须在 main 之前构造，编译器生成 .init_array 项。",
            "<strong>异常与 RTTI</strong>：.eh_frame、类型信息表让栈展开与 dynamic_cast 成为可能。",
        ],
    },
},

# ============================================================
"objectivec": {
    "tagline": "把 Smalltalk 的消息发送缝进 C，成了 NeXT 与 Apple 的底座。",
    "intro": [
        "Objective-C 由 Brad Cox 与 Tom Love 在 1980 年代初设计，1984 年随 Stepstone 产品出现。它没有另造语法，而是在 C 上加了 `@interface`、`@implementation` 与方括号消息：`[obj method]`。",
        "它的核心不是类，而是运行时。方法调用被编译成 `objc_msgSend`，接收者、选择器、参数在运行时决定；类、方法、协议都是运行时可查询的对象。这来自 Smalltalk，而不是 C++ 的静态绑定。",
        "NeXT 在 1988 年采用它，Apple 在 1996 年收购 NeXT 后把它变成 macOS / iOS 的主力语言。今天它仍在大量系统框架与老项目中运行，与 Swift 并存。",
    ],
    "lineage": {
        "from": ["C", "Smalltalk-80"],
        "to": ["Swift（互操作）", "Cocoa / Cocoa Touch 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.m",
            "cmd": "$ cat hello.m",
            "code": r"""#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *msg = [NSString stringWithFormat:@"Hello, %@", @"world"];
        NSLog(@"%@", msg);
    }
    return 0;
}""",
            "format": [
                ("扩展名", ".m；Objective-C++ 用 .mm"),
                ("消息", "[receiver selector:arg]"),
                ("字符串", "@\"...\" 是 NSString 字面量"),
                ("内存", "ARC 或手动 retain/release"),
            ],
            "note": "`@autoreleasepool` 是编译器指令，不是函数调用。它会在作用域结束时排空自动释放池，管理临时对象生命周期。",
        },
        {
            "label": "预处理",
            "file": "hello.mi",
            "cmd": "$ clang -E hello.m -o hello.mi",
            "code": r"""# 1 "hello.m"
# 1 "/System/Library/Frameworks/Foundation.framework/Headers/Foundation.h" 1 3
...
@interface NSString : NSObject <NSCopying, NSMutableCopying, ...>
...
+ (instancetype)stringWithFormat:(NSString *)format, ...;
...
@end
# 2 "hello.m" 2

int main(void) {
    @autoreleasepool {
        NSString *msg = [NSString stringWithFormat:@"Hello, %@", @"world"];
        NSLog(@"%@", msg);
    }
}""",
            "format": [
                ("扩展名", ".mi（预处理后文本）"),
                ("头文件", "Foundation 框架的全部声明"),
                ("宏", "#import 保证只包含一次"),
                ("产物", "仍然是 Objective-C 语法，不是纯 C"),
            ],
            "note": "预处理只做文本展开，`@interface`、方括号消息原样保留，交给 clang 的 Objective-C 前端。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "$ clang -S hello.m -o hello.s",
            "code": r"""    .section    __TEXT,__text,regular,pure_instructions
_main:
    ...
    movq    _OBJC_CLASS_$_NSString(%rip), %rdi
    leaq    L_OBJC_SELECTOR_REFERENCES_(%rip), %rsi
    call    _objc_msgSend

    ; NSLog(@"%@", msg)
    leaq    .L_format(%rip), %rdi
    movq    -8(%rbp), %rsi
    call    _NSLog

    .section    __DATA,__objc_selrefs
L_OBJC_SELECTOR_REFERENCES_:
    .quad   "stringWithFormat:"

    .section    __DATA,__objc_classrefs
    .quad   _OBJC_CLASS_$_NSString""",
            "format": [
                ("消息发送", "objc_msgSend(receiver, selector, args…)"),
                ("选择器", "stringWithFormat: 存进 __objc_selrefs"),
                ("类引用", "类对象地址存进 __objc_classrefs"),
                ("平台", "Mach-O 段名，如 __TEXT/__DATA"),
            ],
            "note": "所有方括号消息最终都是一次 objc_msgSend 调用。选择器是运行时注册的字符串，方法查找发生在调用那一刻。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ clang -c hello.m && otool -h hello.o",
            "code": r"""$ otool -h hello.o
Mach header
      magic cputype cpusubtype  caps    filetype ncmds
 0xfeedfacf 16777228          0  0x00           1     5

$ otool -l hello.o | grep -A3 -E '__objc|__text'
  sectname __text
   segname __TEXT
  sectname __objc_data
   segname __DATA""",
            "format": [
                ("格式", "Mach-O 64 位目标文件"),
                ("魔数", "0xfeedfacf（小端 64 位）"),
                ("段", "__TEXT,__text / __DATA,__objc_*"),
                ("符号", "_main 已定义，objc_msgSend 未定义"),
            ],
            "note": "Objective-C 的元数据（类、方法、协议、选择器）都被放进专用的 __objc_* 段，由运行时在加载时注册。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ clang -framework Foundation -o hello hello.m",
            "code": r"""$ otool -L hello
hello:
    /System/Library/Frameworks/Foundation.framework/Foundation
    /usr/lib/libobjc.A.dylib
    /usr/lib/libSystem.B.dylib

$ file hello
hello: Mach-O 64-bit executable arm64

$ ./hello
2026-10-27 10:00:00.000 hello[1234:5678] Hello, world""",
            "format": [
                ("格式", "Mach-O 可执行文件"),
                ("依赖", "Foundation / libobjc / libSystem"),
                ("加载", "dyld 注册类与方法，再调 main"),
                ("签名", "macOS / iOS 要求代码签名"),
            ],
            "note": "程序启动时，Objective-C 运行时先把所有类、方法、选择器注册进表，然后才执行 main。消息发送之所以能工作，靠的是这一步。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "vi / Emacs", "compiler": "Stepstone / NeXT 编译器", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "1990s", "editor": "Project Builder", "compiler": "GCC (objc)", "build": "make / PB", "pkg": "框架", "debug": "gdb"},
        {"era": "2000s", "editor": "Xcode", "compiler": "GCC → clang", "build": "Xcode build", "pkg": "CocoaPods", "debug": "lldb"},
        {"era": "2020s", "editor": "Xcode", "compiler": "clang", "build": "Xcode / SwiftPM", "pkg": "CocoaPods / SPM", "debug": "lldb"},
    ],
    "hello": {
        "file": "hello.m",
        "code": r"""#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSLog(@"Hello, world");
    }
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 130 B", "w": 5},
            {"stage": "预处理", "size": "≈ 90 KB", "w": 60},
            {"stage": "汇编", "size": "≈ 2.4 KB", "w": 14},
            {"stage": "目标 .o", "size": "≈ 4 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 40 KB", "w": 30},
            {"stage": "+ Foundation", "size": "≈ 30 MB", "w": 100},
        ],
        "why": [
            "<strong>消息发送</strong>：调用点只保存接收者与选择器，方法查找推迟到运行时。",
            "<strong>运行时元数据</strong>：类、方法、协议、选择器都在 __objc_* 段里。",
            "<strong>Foundation</strong>：字符串、集合、日志、autoreleasepool 都由框架提供。",
            "<strong>动态派发</strong>：可以在运行时替换方法实现（swizzling），这是 Cocoa 很多机制的基础。",
        ],
    },
},

# ============================================================
"perl": {
    "tagline": "「条条大路通罗马」的文本处理语言，CGI 时代最忙的胶水。",
    "intro": [
        "Perl 由 Larry Wall 在 1987 年发布，最初是给 UNIX 文本处理写报表的工具。它把正则表达式、文件句柄、哈希、列表全部塞进语法，目标不是优雅，而是「把活干完」。",
        "Perl 没有可移植的字节码文件。源码被解析成一棵操作树（optree），解释器直接在这棵树上执行；`perl -c` 做语法检查，B::Concise 可以把它打印出来。需要独立可执行文件时，人们用 B::C 把 optree 编译成 C，或把解释器与脚本打包。",
        "CPAN 让 Perl 在 1990 年代成为 Web 后端的主力：CGI、mod_perl、模板、数据库驱动。它的文化也影响了 Ruby、Python 与后来的脚本语言。",
    ],
    "lineage": {
        "from": ["awk", "sed", "shell", "C"],
        "to": ["PHP（部分）", "Ruby（部分）", "Raku"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.pl",
            "cmd": "$ cat hello.pl",
            "code": r"""#!/usr/bin/perl
use strict;
use warnings;

my $name = 'world';
print "Hello, $name\n";""",
            "format": [
                ("扩展名", ".pl / .pm / .t"),
                ("变量", "$ 标量 · @ 数组 · % 哈希"),
                ("正则", "/pattern/ 是语法的一部分"),
                ("shebang", "#!/usr/bin/perl 交给内核选择解释器"),
            ],
            "note": "`use strict` 与 `use warnings` 是 Perl 5 之后的标准做法：前者禁止未声明变量，后者打开诊断。",
        },
        {
            "label": "操作树",
            "file": "optree",
            "cmd": "$ perl -MO=Concise,-exec hello.pl",
            "code": r"""$ perl -MO=Concise,-exec hello.pl
1  <0> enter
2  <;> nextstate(main 2 hello.pl:5) v
3  <0> pushmark s
4  <$> const[PV "Hello, world\n"] s
5  <1> print vK
6  <1> leave

; optree 是解释器真正执行的结构
; 每个节点是一个 op，如 const / print / leave""",
            "format": [
                ("形态", "操作树（optree）"),
                ("节点", "op（操作符）+ 子节点 + 标志位"),
                ("执行", "解释器遍历 optree，递归求值"),
                ("查看", "B::Concise / B::Terse"),
            ],
            "note": "Perl 的「编译」主要发生在解析与 optree 构造阶段。没有中间文件，下一次运行还要重新解析。",
        },
        {
            "label": "生成 C",
            "file": "hello.c",
            "cmd": "$ perl -MO=C,-ohello.c hello.pl",
            "code": r"""/* B::C 输出片段（示意） */
#include "EXTERN.h"
#include "perl.h"

static const char *script =
    "use strict;\nuse warnings;\n"
    "my $name = 'world';\n"
    "print \"Hello, $name\\n\";\n";

int main(int argc, char **argv) {
    PerlInterpreter *my_perl = perl_alloc();
    perl_construct(my_perl);
    perl_parse(my_perl, NULL, argc, argv, NULL);
    perl_run(my_perl);
    perl_destruct(my_perl);
    perl_free(my_perl);
}""",
            "format": [
                ("工具", "B::C / B::CC"),
                ("策略", "把 optree 或脚本嵌入 C 程序"),
                ("运行时", "仍然需要 libperl"),
                ("体积", "生成 C 可能上百 KB"),
            ],
            "note": "B::C 不是把 Perl 编译成机器码，而是把解释器、optree 与脚本打包进一个 C 程序。启动仍然要初始化 Perl 运行时。",
        },
        {
            "label": "打包可执行",
            "file": "hello",
            "cmd": "$ pp -o hello hello.pl",
            "code": r"""$ pp -o hello hello.pl
$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ls -lh hello
-rwxr-xr-x 1 user user 2.6M ... hello

$ ./hello
Hello, world

; 内部：Perl 解释器 + 脚本 + 依赖模块
; 运行时解压到临时目录（PAR）""",
            "format": [
                ("工具", "PAR::Packer / pp"),
                ("内容", "解释器 + 脚本 + 模块"),
                ("体积", "通常 2–10 MB"),
                ("运行", "解包到临时目录后启动"),
            ],
            "note": "打包不是编译：它把整个 Perl 运行时和脚本一起塞进可执行文件，用户不需要另外安装 Perl。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "vi / Emacs", "compiler": "perl 解释器", "build": "Makefile.PL", "pkg": "—", "debug": "perl -d"},
        {"era": "1990s", "editor": "Emacs / vim", "compiler": "perl 5", "build": "Makefile.PL", "pkg": "CPAN", "debug": "perl -d"},
        {"era": "2000s", "editor": "Padre / vim", "compiler": "perl 5", "build": "Module::Build", "pkg": "CPAN", "debug": "Devel::NYTProf"},
        {"era": "2020s", "editor": "VS Code + Perl", "compiler": "perl 5.40", "build": "cpanm / Dist::Zilla", "pkg": "CPAN", "debug": "perl -d"},
    ],
    "hello": {
        "file": "hello.pl",
        "code": r"""print "Hello, world\n";""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "optree", "size": "≈ 300 B", "w": 10},
            {"stage": "生成 C", "size": "≈ 200 KB", "w": 45},
            {"stage": "打包 exe", "size": "≈ 2.6 MB", "w": 80},
            {"stage": "+ libperl", "size": "≈ 8 MB", "w": 100},
        ],
        "why": [
            "<strong>optree</strong>：解释器执行的结构，不是源码文本，也不是机器码。",
            "<strong>无字节码文件</strong>：每次运行都重新解析，除非用打包工具缓存。",
            "<strong>B::C</strong>：把解释器与 optree 嵌进 C，换取独立分发。",
            "<strong>PAR</strong>：把解释器与脚本压进一个可执行文件，运行时解包。",
        ],
    },
},

# ============================================================
"erlang": {
    "tagline": "为电信交换机设计的语言：进程、消息、崩溃，然后自动重启。",
    "intro": [
        "Erlang 由 Joe Armstrong、Robert Virding 与 Mike Williams 在爱立信设计，1986 年形成第一版。它要解决的问题很具体：电话交换机必须长时间运行，不能因为一个进程出错就整体停机。",
        "Erlang 的并发单位是轻量进程，进程之间只通过消息通信，不共享内存。一个进程崩溃不会影响其他进程；监督树（supervision tree）负责重启。这套模型后来被称为「let it crash」。",
        "它的编译产物是 `.beam` 文件：BEAM 字节码 + 模块元数据。BEAM 虚拟机按模块加载，支持热代码替换——不停止系统就能升级一个模块。",
    ],
    "lineage": {
        "from": ["Prolog（语法）", "telecom 容错需求", "并发演算"],
        "to": ["Elixir", "Gleam", "Akka（思想）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.erl",
            "cmd": "$ cat hello.erl",
            "code": r"""-module(hello).
-export([world/0]).

world() ->
    io:format("Hello, world~n").""",
            "format": [
                ("模块", "-module(hello) 必须与文件名一致"),
                ("导出", "-export([world/0])"),
                ("函数", "world/0 表示零个参数"),
                ("结束", "每个子句以句号结束"),
            ],
            "note": "Erlang 的模块是编译与热加载的单位。`world/0` 里的 `/0` 是元数（arity），Erlang 用名字 + 元数标识函数。",
        },
        {
            "label": "Core Erlang",
            "file": "hello.core",
            "cmd": "$ erlc +to_core hello.erl",
            "code": r"""module 'hello' ['world'/0]
    attributes []

'world'/0 =
    fun () ->
        call 'io':'format'(<"Hello, world~n">)

; 语法为结构示意
; Core Erlang 是去糖后的中间语言
; 模式匹配、守卫、异常都已展开""",
            "format": [
                ("中间语言", "Core Erlang"),
                ("作用", "优化与代码生成的稳定输入"),
                ("形式", "模块 + 函数 + 表达式"),
                ("查看", "erlc +to_core"),
            ],
            "note": "Core Erlang 把语法糖去掉了，但仍是函数式语言。优化器与 BEAM 代码生成器都从这里读取程序。",
        },
        {
            "label": "BEAM 文件",
            "file": "hello.beam",
            "cmd": "$ erlc hello.erl && xxd -l 32 hello.beam",
            "code": r"""$ xxd -l 32 hello.beam
00000000: 464f 5231 0000 032c 4245 414d 0000 02f4  FOR1...,BEAM....
00000010: 436f 6465 0000 01a0 4174 6f6d 0000 0068  Code....Atom...h

; 块结构：
;   FOR1 + 总长度
;   BEAM / Code / Atom / StrT / ImpT / ExpT / LitT / Attr
; Code 块 = BEAM 字节码
; Atom 块 = 原子表（模块名、函数名、字符串）""",
            "format": [
                ("魔数", "FOR1（IFF 风格容器）"),
                ("块", "BEAM / Code / Atom / LitT / Attr …"),
                ("字节码", "Code 块中的 BEAM 指令"),
                ("单元", "一个模块一个 .beam"),
            ],
            "note": "`.beam` 不是链接后的可执行文件，而是等待被虚拟机加载的模块。BEAM 可以热加载，也可以同时存在两个版本。",
        },
        {
            "label": "发布包",
            "file": "hello.tar.gz",
            "cmd": "$ rebar3 release && ls _build/default/rel/hello",
            "code": r"""$ ls _build/default/rel/hello
bin/ erts-15.0/  lib/  releases/  start.sh

$ ./bin/hello console
Eshell V15.0
1> hello:world().
Hello, world
ok

; 发布包 = ERTS 运行时 + 所有 .beam + 启动脚本
; 目标机器不需要预装 Erlang""",
            "format": [
                ("发布", "ERTS + 应用 + 启动脚本"),
                ("体积", "通常 20–80 MB（含运行时）"),
                ("启动", "boot 脚本按顺序加载模块"),
                ("热升级", "release_handler 替换模块"),
            ],
            "note": "Erlang 的「可执行产物」通常不是一个二进制，而是一个自包含的 release 目录：虚拟机、.beam、配置与启动脚本。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "Emacs", "compiler": "erlc", "build": "make", "pkg": "—", "debug": "dbg / io:format"},
        {"era": "1990s", "editor": "Emacs", "compiler": "erlc", "build": "make", "pkg": "—", "debug": "dbg"},
        {"era": "2000s", "editor": "Emacs + Distel", "compiler": "erlc", "build": "rebar", "pkg": "CEAN", "debug": "observer"},
        {"era": "2020s", "editor": "VS Code + Erlang LS", "compiler": "erlc", "build": "rebar3", "pkg": "hex", "debug": "observer / dbg"},
    ],
    "hello": {
        "file": "hello.erl",
        "code": r"""-module(hello).
-export([world/0]).

world() -> io:format("Hello, world~n").""",
        "footprint": [
            {"stage": "源码", "size": "≈ 90 B", "w": 5},
            {"stage": "Core", "size": "≈ 220 B", "w": 9},
            {"stage": ".beam", "size": "≈ 1.2 KB", "w": 16},
            {"stage": "release", "size": "≈ 25 MB", "w": 75},
            {"stage": "+ ERTS", "size": "≈ 40 MB", "w": 100},
        ],
        "why": [
            "<strong>模块</strong>：编译、加载、热替换都以模块为单位。",
            "<strong>BEAM 文件</strong>：容器里同时装着字节码、原子表、导出表与调试信息。",
            "<strong>轻量进程</strong>：虚拟机调度，不依赖操作系统线程。",
            "<strong>release</strong>：把运行时与所有模块打包，目标机器无需安装 Erlang。",
        ],
    },
},

# ============================================================
"ada": {
    "tagline": "为关键系统设计的语言：强类型、运行时检查、包与任务。",
    "intro": [
        "Ada 由 Jean Ichbiah 领导的 CII Honeywell Bull 团队为美国国防部设计，1980 年成为 MIL-STD-1815。目标是取代当时数百种军用语言，给嵌入式与实时系统一套统一、可验证的工具。",
        "Ada 的包（package）把规范（.ads）与实现（.adb）分开，编译器为每个编译单元生成 ALI（Ada Library Information）文件，记录依赖、版本与检查结果。`gnatbind` 读取 ALI 决定初始化顺序，`gnatlink` 生成最终程序。",
        "它的运行时检查（数组越界、范围、除以零）可以按需保留或关闭。这种「默认安全、可审计」的取向，让 Ada 长期活跃在航空、铁路、卫星与军工系统里。",
    ],
    "lineage": {
        "from": ["Pascal", "ALGOL 60", "Modula-2"],
        "to": ["SPARK", "Rust（部分安全理念）", "实时系统语言"],
    },
    "chain": [
        {
            "label": "包规范",
            "file": "hello.ads",
            "cmd": "$ cat hello.ads",
            "code": r"""package Hello is
   procedure Say;
end Hello;""",
            "format": [
                ("扩展名", ".ads（spec）"),
                ("内容", "只写接口与类型"),
                ("可见性", "包外可见的过程/类型"),
                ("对应物", "C 头文件 / Modula-2 .def"),
            ],
            "note": "包规范是客户唯一需要看到的文件。它不含实现，也不含可执行代码。",
        },
        {
            "label": "包体",
            "file": "hello.adb",
            "cmd": "$ cat hello.adb",
            "code": r"""with Ada.Text_IO; use Ada.Text_IO;

package body Hello is
   procedure Say is
   begin
      Put_Line ("Hello, world");
   end Say;
end Hello;""",
            "format": [
                ("扩展名", ".adb（body）"),
                ("with", "显式依赖其他包"),
                ("实现", "必须匹配规范中的签名"),
                ("检查", "编译器插入范围/越界检查"),
            ],
            "note": "`with Ada.Text_IO` 是编译期依赖；`use` 只是把名字放进当前作用域，不改变依赖关系。",
        },
        {
            "label": "ALI 与目标",
            "file": "hello.ali / hello.o",
            "cmd": "$ gnatmake main.adb",
            "code": r"""$ gnatmake main.adb
gcc -c hello.ads
gcc -c hello.adb
gcc -c main.adb
gnatbind -x main.ali
gnatlink main.ali

$ head -8 hello.ali
V "GNAT Lib v13.2"
A "hello.ads"
A "hello.adb"
...
; ALI = Ada Library Information
; 记录依赖、校验和、编译选项、检查结果""",
            "format": [
                ("ALI", "Ada Library Information，文本"),
                ("作用", "依赖、版本、检查、初始化顺序"),
                ("目标", "平台对象文件（ELF/COFF）"),
                ("绑定", "gnatbind 读 ALI 生成 b~main.adb"),
            ],
            "note": "ALI 文件让 Ada 的独立编译可审计：编译器知道每个单元依赖谁、用什么选项编译、是否一致。",
        },
        {
            "label": "可执行",
            "file": "main",
            "cmd": "$ ./main",
            "code": r"""$ ./main
Hello, world

$ file main
main: ELF 64-bit LSB pie executable, x86-64 ...

; 链接了 Ada 运行时：
;   任务调度、异常、检查、最终化
; 可用 -gnatp 关闭运行时检查（需谨慎）""",
            "format": [
                ("链接", "gnatlink + Ada 运行时"),
                ("运行时", "任务、异常、检查、受控类型"),
                ("产物", "原生可执行文件"),
                ("裁剪", "嵌入式可用 Ravenscar / ZFP"),
            ],
            "note": "Ada 程序默认带运行时检查。对实时系统，这些检查的代价与可预测性需要单独评估，因此有 Ravenscar 等受限配置。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "行编辑器", "compiler": "Ada 编译器（DEC/Alsyd）", "build": "make / ACL", "pkg": "—", "debug": "符号调试器"},
        {"era": "1990s", "editor": "Emacs / GPS 前身", "compiler": "GNAT", "build": "gnatmake", "pkg": "—", "debug": "gdb"},
        {"era": "2000s", "editor": "GPS", "compiler": "GNAT", "build": "gnatmake / gprbuild", "pkg": "GPR", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + Ada", "compiler": "GNAT / GNAT Pro", "build": "gprbuild", "pkg": "Alire", "debug": "gdb"},
    ],
    "hello": {
        "file": "main.adb",
        "code": r"""with Ada.Text_IO; use Ada.Text_IO;
procedure Main is
begin
   Put_Line ("Hello, world");
end Main;""",
        "footprint": [
            {"stage": "规范 .ads", "size": "≈ 45 B", "w": 4},
            {"stage": "包体 .adb", "size": "≈ 120 B", "w": 7},
            {"stage": "ALI", "size": "≈ 1.8 KB", "w": 14},
            {"stage": "目标 .o", "size": "≈ 3 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 220 KB", "w": 55},
            {"stage": "+ 运行时", "size": "≈ 1 MB", "w": 80},
        ],
        "why": [
            "<strong>规范/实现分离</strong>：客户只依赖 .ads，实现可以替换。",
            "<strong>ALI</strong>：把依赖、版本与检查结果写进可审计的文本文件。",
            "<strong>绑定</strong>：gnatbind 根据 ALI 决定包的初始化顺序。",
            "<strong>默认检查</strong>：越界、范围、空指针在运行时被捕获，而不是静默未定义行为。",
        ],
    },
},

# ============================================================
"eiffel": {
    "tagline": "把「契约」写进语言：前置条件、后置条件、类不变式。",
    "intro": [
        "Eiffel 由 Bertrand Meyer 在 1986 年发布，最著名的贡献是 Design by Contract：每个例程可以声明 `require`（前置条件）、`ensure`（后置条件），每个类可以声明 `invariant`（不变式）。这些不是注释，而是可执行的断言。",
        "Eiffel 是纯面向对象的：一切皆对象，没有全局变量，没有静态方法。它的编译器先把 Eiffel 翻译成 C，再交给系统 C 编译器，因此产物链中间会看到一层生成 C。",
        "契约在开发期被编译成运行时检查，在发布版可以关闭。EiffelStudio 还提供「melting ice」：只重新编译受影响的类，其余保留目标代码。",
    ],
    "lineage": {
        "from": ["Simula 67", "ALGOL W", "Z 规格说明"],
        "to": ["D 的契约", "Rust 的 debug_assert", "现代 API 契约设计"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.e",
            "cmd": "$ cat hello.e",
            "code": r"""class
    HELLO
create
    make
feature
    make
        do
            io.put_string ("Hello, world%N")
        end
end""",
            "format": [
                ("扩展名", ".e"),
                ("类", "class … end，一切皆类"),
                ("创建", "create make 指定构造过程"),
                ("换行", "%N 是 Eiffel 的换行转义"),
            ],
            "note": "Eiffel 的类没有全局函数；`io` 是一个可用的对象，`put_string` 是它的 feature。",
        },
        {
            "label": "契约",
            "file": "stack.e",
            "cmd": "require / ensure / invariant",
            "code": r"""class
    STACK [G]
feature
    push (x: G)
        require
            not_full: count < capacity
        do
            ...
        ensure
            one_more: count = old count + 1
            top_is_x: item = x
        end
invariant
    non_negative: count >= 0
    bounded: count <= capacity
end""",
            "format": [
                ("require", "前置条件，调用方责任"),
                ("ensure", "后置条件，实现方责任"),
                ("invariant", "类不变式，每个公开操作前后成立"),
                ("old", "引用进入例程前的值"),
            ],
            "note": "契约是 Eiffel 的核心：它把「调用者该保证什么」「实现者该保证什么」写成可执行、可继承、可检查的代码。",
        },
        {
            "label": "生成 C",
            "file": "hello.c",
            "cmd": "$ ec -config hello.ecf -target hello",
            "code": r"""/* EiffelStudio 生成的 C（片段，示意） */
EIF_REFERENCE _make (EIF_REFERENCE Current)
{
    EIF_REFERENCE Result = (EIF_REFERENCE) 0;
    eif_put_string (Current, "Hello, world\n");
    return Result;
}

/* 契约检查会生成类似：
   if (!(count < capacity)) eif_contract_violation(...);
*/""",
            "format": [
                ("策略", "Eiffel → C → 本机编译器"),
                ("运行时", "EIF_REFERENCE、GC、异常"),
                ("契约", "require/ensure 生成检查代码"),
                ("项目", ".ecf 描述目标与库"),
            ],
            "note": "生成 C 让 Eiffel 可以复用各平台的 C 工具链；代价是调试时需要同时理解两层代码。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; 链接了 Eiffel 运行时：
;   垃圾回收、契约检查、异常、类型信息
; 发布时可关闭检查：
;   ec -config hello.ecf -finalize""",
            "format": [
                ("产物", "原生可执行文件"),
                ("运行时", "GC、契约、异常、类型"),
                ("finalize", "关闭检查、优化、冻结系统"),
                ("melting", "只重编译改动过的类"),
            ],
            "note": "finalize 之后契约检查通常被移除；这正是「开发期严格、发布期轻量」的取舍。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "行编辑器", "compiler": "Eiffel 编译器（C 后端）", "build": "make", "pkg": "—", "debug": "—"},
        {"era": "1990s", "editor": "EiffelStudio", "compiler": "EiffelStudio", "build": "ec", "pkg": "库簇", "debug": "EiffelStudio 调试器"},
        {"era": "2000s", "editor": "EiffelStudio", "compiler": "EiffelStudio", "build": "ec", "pkg": "EiffelStore", "debug": "调试器"},
        {"era": "2020s", "editor": "VS Code + Eiffel", "compiler": "EiffelStudio / LibertyEiffel", "build": "ec / finish_freezing", "pkg": "iron", "debug": "调试器"},
    ],
    "hello": {
        "file": "hello.e",
        "code": r"""class
    HELLO
create
    make
feature
    make
        do
            io.put_string ("Hello, world%N")
        end
end""",
        "footprint": [
            {"stage": "源码", "size": "≈ 120 B", "w": 5},
            {"stage": "生成 C", "size": "≈ 6 KB", "w": 18},
            {"stage": "目标 .o", "size": "≈ 9 KB", "w": 22},
            {"stage": "可执行", "size": "≈ 1.2 MB", "w": 55},
            {"stage": "+ 运行时", "size": "≈ 2 MB", "w": 70},
        ],
        "why": [
            "<strong>契约</strong>：require/ensure/invariant 把接口责任写成可执行断言。",
            "<strong>纯 OO</strong>：没有全局函数与静态方法，所有操作都属于某个对象。",
            "<strong>C 后端</strong>：先翻译成 C，复用系统工具链与平台 ABI。",
            "<strong>finalize</strong>：发布时关闭检查并冻结系统，减少运行时开销。",
        ],
    },
},

# ============================================================
"matlab": {
    "tagline": "把矩阵、绘图与工程仿真装进一个交互式工作台。",
    "intro": [
        "MATLAB 由 Cleve Moler 在 1980 年代初开发，最初是 LINPACK/EISPACK 的交互式前端，1984 年由 MathWorks 商业化。它的核心不是语法，而是矩阵：几乎所有值都是数组，运算默认向量化。",
        "MATLAB 的产物链不鼓励「编译成可执行文件」。`.m` 源码由解释器加载，JIT 在运行时优化热点；`pcode` 可以生成加密的 `.p` 文件；`mcc` 可以把函数打包成依赖 MATLAB Runtime 的独立程序。",
        "它的生态包括 Simulink、工具箱与 MEX（C/C++/Fortran 扩展）。这使 MATLAB 更像一个计算平台，而不是一门孤立的语言。",
    ],
    "lineage": {
        "from": ["LINPACK / EISPACK", "Fortran", "APL（数组思维）"],
        "to": ["Octave", "Julia（部分）", "NumPy（数组接口）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.m",
            "cmd": "$ cat hello.m",
            "code": r"""function hello
    disp('Hello, world')
end""",
            "format": [
                ("扩展名", ".m"),
                ("函数", "function … end"),
                ("数组", "默认 double 矩阵"),
                ("索引", "从 1 开始，列优先"),
            ],
            "note": "MATLAB 的函数名通常与文件名一致；`hello.m` 定义 `hello`，调用时按文件名查找。",
        },
        {
            "label": "解析",
            "file": "parse tree",
            "cmd": ">> tree = mtree('hello.m','-file')",
            "code": r"""; 解析树（结构示意）
FUNCTION
  name: hello
  body:
    EXPR
      CALL
        callee: disp
        args: STRING 'Hello, world'

; MATLAB 在加载时解析 .m
; JIT 在运行时把热点编译为机器码""",
            "format": [
                ("解析", "加载时构建语法树"),
                ("执行", "解释 + JIT"),
                ("类型", "动态，默认 double"),
                ("内存", "列优先，写时复制"),
            ],
            "note": "MATLAB 没有对用户暴露的稳定字节码格式。解析树与 JIT 编译结果都在内存里，不落盘。",
        },
        {
            "label": "p-code",
            "file": "hello.p",
            "cmd": "$ pcode hello.m",
            "code": r"""$ pcode hello.m
$ ls -l hello.p
-rw-r--r-- 1 user user 1.1K ... hello.p

$ file hello.p
hello.p: data
$ xxd -l 16 hello.p
00000000: 0001 0000 0000 0000 0000 0000 0000 0000  ................

; p-code 是加密/混淆后的可执行形式
; 头部结构未公开，字节为示例
; 仍需 MATLAB 环境运行""",
            "format": [
                ("命令", "pcode"),
                ("作用", "隐藏源码，不是独立程序"),
                ("格式", "私有二进制，未公开"),
                ("运行", "仍需 MATLAB"),
            ],
            "note": "p-code 的卖点是保护源码，不是可移植性。它绑定 MATLAB 版本，不能脱离 MATLAB 运行。",
        },
        {
            "label": "部署程序",
            "file": "hello.exe + hello.ctf",
            "cmd": "$ mcc -m hello.m",
            "code": r"""$ mcc -m hello.m
$ ls
hello.exe  hello.ctf  readme.txt

$ file hello.exe
hello.exe: PE32+ executable (console) x86-64

; hello.ctf = 加密的组件技术文件（AES）
; 目标机器需要安装 MATLAB Runtime (MCR)
; MCR 体积通常 1–3 GB""",
            "format": [
                ("工具", "MATLAB Compiler (mcc)"),
                ("产物", ".exe + .ctf + readme"),
                ("运行时", "MATLAB Runtime（MCR）"),
                ("依赖", "MCR 版本必须与编译时一致"),
            ],
            "note": "部署程序把 MATLAB 代码与工具箱打包进 .ctf，但数值计算、图形与 JIT 仍由 MCR 提供。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "MATLAB 命令行", "compiler": "解释器", "build": "—", "pkg": "工具箱", "debug": "dbstop / dbstep"},
        {"era": "1990s", "editor": "MATLAB 编辑器", "compiler": "解释器", "build": "—", "pkg": "Toolbox", "debug": "dbstop"},
        {"era": "2000s", "editor": "MATLAB IDE", "compiler": "JIT + mcc", "build": "mcc", "pkg": "Toolbox", "debug": "MATLAB 调试器"},
        {"era": "2020s", "editor": "MATLAB Online / VS Code", "compiler": "JIT + MATLAB Compiler", "build": "mcc / buildtool", "pkg": "Add-On Explorer", "debug": "MATLAB 调试器"},
    ],
    "hello": {
        "file": "hello.m",
        "code": r"""function hello
    disp('Hello, world')
end""",
        "footprint": [
            {"stage": "源码", "size": "≈ 60 B", "w": 4},
            {"stage": "解析树", "size": "≈ 200 B", "w": 8},
            {"stage": ".p", "size": "≈ 1.1 KB", "w": 14},
            {"stage": ".exe + .ctf", "size": "≈ 2 MB", "w": 45},
            {"stage": "+ MCR", "size": "≈ 2 GB", "w": 100},
        ],
        "why": [
            "<strong>数组优先</strong>：语言与运行时都为矩阵运算优化，循环通常不是首选。",
            "<strong>JIT</strong>：热点函数在运行时编译，源码不落盘为字节码。",
            "<strong>p-code</strong>：保护源码的加密形式，但仍依赖 MATLAB。",
            "<strong>MCR</strong>：部署程序把庞大运行时留给目标机器安装。",
        ],
    },
},

# ============================================================
"commonlisp": {
    "tagline": "1980 年代把各家长处合并成标准：CLOS、包、条件系统与宏。",
    "intro": [
        "Common Lisp 不是某个人设计的，而是 1980 年代初各家 Lisp 实现（Maclisp、Franz Lisp、Interlisp 等）的合并产物。1984 年的《Common Lisp the Language》定义了第一版标准，1994 年由 ANSI 正式标准化。",
        "它把 Lisp 的能力系统化了：包（package）管理名字，CLOS 提供泛型函数与多重方法，条件系统（condition system）把错误处理与恢复分开，宏在编译期改写代码。",
        "与早期的 LISP 相比，Common Lisp 的产物链更工程化：`compile-file` 生成实现相关的 FASL，ASDF 管理系统依赖，`save-lisp-and-die` 可以把运行时与程序一起保存成独立可执行文件。",
    ],
    "lineage": {
        "from": ["Maclisp", "Franz Lisp", "Interlisp", "Scheme（部分）"],
        "to": ["Clojure", "Emacs Lisp（部分）", "ACL2"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.lisp",
            "cmd": "$ cat hello.lisp",
            "code": r"""(defpackage :hello
  (:use :cl)
  (:export :main))

(in-package :hello)

(defclass greeter ()
  ((name :initarg :name :reader name)))

(defmethod greet ((g greeter))
  (format t "Hello, ~a!~%" (name g)))

(defun main ()
  (greet (make-instance 'greeter :name "world")))""",
            "format": [
                ("包", "defpackage 管理符号归属"),
                ("类", "defclass + 槽 + reader"),
                ("方法", "defmethod 按参数特化"),
                ("入口", "main 是自己约定的函数"),
            ],
            "note": "Common Lisp 没有标准的主函数。`main` 只是约定，真正启动要靠实现提供的保存/导出机制。",
        },
        {
            "label": "宏展开",
            "file": "expanded",
            "cmd": "CL-USER> (macroexpand-1 '(when (name g) (greet g)))",
            "code": r"""CL-USER> (macroexpand-1 '(when (name g) (greet g)))
(IF (NAME G)
    (PROGN (GREET G)))
T

; 宏在编译期运行，输出仍是 Lisp 代码
; 与函数不同，宏的返回值会被再次编译""",
            "format": [
                ("宏", "编译期代码变换"),
                ("展开", "macroexpand-1 / macroexpand"),
                ("卫生", "Common Lisp 宏不自动卫生"),
                ("能力", "可定义控制流、DSL、绑定形式"),
            ],
            "note": "Common Lisp 的宏不是文本替换：它接收已读取的表达式，返回新表达式，然后继续编译。",
        },
        {
            "label": "FASL",
            "file": "hello.fasl",
            "cmd": "$ sbcl --eval '(compile-file \"hello.lisp\")'",
            "code": r"""; compiling file "hello.lisp"
; wrote /home/user/.cache/common-lisp/.../hello.fasl

; FASL 结构（实现相关，示意）
;   header  : 魔数 / 版本 / 字长 / 特性
;   code    : 编译后的函数对象
;   data    : 字面量、符号、调试信息
;   linking : 加载时重定位

$ ls -lh hello.fasl
-rw-r--r-- 1 user user 6.2K ... hello.fasl""",
            "format": [
                ("FASL", "Fast Load，编译产物"),
                ("绑定", "与实现、版本、字长相关"),
                ("内容", "代码 + 字面量 + 符号 + 调试信息"),
                ("加载", "跳过读取与宏展开"),
            ],
            "note": "FASL 是「可加载的代码块」，不是可执行文件。它必须由同一实现的运行时加载。",
        },
        {
            "label": "独立可执行",
            "file": "hello",
            "cmd": "$ sbcl --load hello.lisp --eval '(sb-ext:save-lisp-and-die \"hello\" :executable t :toplevel (quote hello:main))'",
            "code": r"""$ ./hello
Hello, world!

$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ls -lh hello
-rwxr-xr-x 1 user user 42M ... hello

; 可执行文件 = Lisp 运行时 + 镜像
; 启动即恢复堆，不重新初始化""",
            "format": [
                ("机制", "保存镜像并加上可执行头"),
                ("体积", "通常 40–60 MB"),
                ("启动", "恢复堆，然后调用 toplevel"),
                ("平台", "与保存时的 OS/架构绑定"),
            ],
            "note": "Common Lisp 的独立程序本质上是一个带着 Lisp 世界的可执行镜像。启动快，但体积大、平台绑定强。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "Emacs / Zmacs", "compiler": "各家 CL 实现", "build": "defsystem", "pkg": "—", "debug": "实现调试器"},
        {"era": "1990s", "editor": "Emacs + ILISP", "compiler": "CMUCL / Allegro", "build": "ASDF", "pkg": "—", "debug": "SLDB"},
        {"era": "2000s", "editor": "Emacs + SLIME", "compiler": "SBCL / CCL", "build": "ASDF", "pkg": "Quicklisp", "debug": "SLDB"},
        {"era": "2020s", "editor": "Emacs + SLY / VS Code", "compiler": "SBCL / CCL", "build": "ASDF", "pkg": "Quicklisp / Ultralisp", "debug": "SLDB"},
    ],
    "hello": {
        "file": "hello.lisp",
        "code": r"""(format t "Hello, world~%")
(sb-ext:exit)""",
        "footprint": [
            {"stage": "源码", "size": "≈ 50 B", "w": 4},
            {"stage": "展开", "size": "≈ 80 B", "w": 5},
            {"stage": "FASL", "size": "≈ 6 KB", "w": 16},
            {"stage": "镜像", "size": "≈ 42 MB", "w": 80},
            {"stage": "可执行", "size": "≈ 42 MB", "w": 85},
        ],
        "why": [
            "<strong>包</strong>：解决大型程序中符号重名，是模块系统的 Lisp 版本。",
            "<strong>CLOS</strong>：泛型函数与多重方法，把 OO 从「类的成员」变成「方法的组合」。",
            "<strong>FASL</strong>：编译后的可加载代码，跳过读取与宏展开。",
            "<strong>镜像</strong>：把整个 Lisp 世界保存成文件，启动即恢复。",
        ],
    },
},

# ============================================================
"tcl": {
    "tagline": "一切皆字符串，一切皆命令；用最小的语法嵌进别的程序。",
    "intro": [
        "Tcl（Tool Command Language）由 John Ousterhout 在 1988 年于加州大学伯克利开发。它的语法只有一条规则：一条命令由若干「词」组成，第一个词是命令名，其余是参数。没有运算符优先级，没有语句关键字。",
        "这种极简语法让 Tcl 非常适合嵌入：C 程序注册几个命令，就能得到一个可脚本化的应用。EDA 工具、网络设备、测试框架长期大量使用 Tcl，正是因为这个原因。",
        "Tcl 8.0 之后加入了字节码编译：脚本在执行前被编译成内部字节码，但默认不落盘。需要分发时，人们用 starkit/starpack 把脚本与运行时打包成一个文件。",
    ],
    "lineage": {
        "from": ["shell 脚本", "Lisp（命令即数据）", "C 嵌入需求"],
        "to": ["Tk（GUI）", "Expect", "EDA 脚本生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.tcl",
            "cmd": "$ cat hello.tcl",
            "code": r"""proc hello {} {
    puts "Hello, world"
}

hello""",
            "format": [
                ("命令", "每行一条命令，空格分词"),
                ("引用", "{} 原样传递，"" 允许替换"),
                ("替换", "$变量 / [命令] 在求值前展开"),
                ("过程", "proc 定义命令"),
            ],
            "note": "Tcl 没有语句语法：`if`、`while`、`proc` 都是命令。大括号里的内容不会被替换，所以能安全地表示代码块。",
        },
        {
            "label": "解析",
            "file": "words",
            "cmd": "% set script {puts \"Hello, world\"}",
            "code": r"""% set script {puts "Hello, world"}
puts "Hello, world"

% llength $script
2

% lindex $script 0
puts

% lindex $script 1
Hello, world

; 一条命令 = 一个列表
; 第一个元素是命令名，其余是参数""",
            "format": [
                ("单位", "命令 = 词列表"),
                ("解析", "分号/换行分隔命令"),
                ("替换", "变量与命令替换"),
                ("求值", "先替换，再调用命令"),
            ],
            "note": "Tcl 的「语法树」非常浅：它几乎没有嵌套表达式，所有结构都由命令自己解释参数。",
        },
        {
            "label": "字节码",
            "file": "bytecode",
            "cmd": "% ::tcl::unsupported::disassemble proc hello",
            "code": r"""% ::tcl::unsupported::disassemble proc hello
ByteCode
  ...
  push1 "Hello, world"
  invokeStk1 2
  done

; Tcl 8 在执行前把脚本编译为字节码
; 字节码不落盘，只在内存中
; 不同 Tcl 版本的指令集不同""",
            "format": [
                ("编译", "脚本 → 内部字节码"),
                ("指令", "栈式，如 push1 / invokeStk1"),
                ("存储", "内存，不生成 .class 文件"),
                ("版本", "指令集随 Tcl 版本变化"),
            ],
            "note": "字节码是 Tcl 8 的性能基础，但它不是公开的可分发格式。换 Tcl 版本就可能失效。",
        },
        {
            "label": "starkit",
            "file": "hello.kit",
            "cmd": "$ sdx wrap hello.kit -runtime tclkit",
            "code": r"""$ sdx wrap hello.kit -runtime tclkit
$ file hello.kit
hello.kit: Zip archive data, at least v2.0

$ ls -lh hello.kit
-rwxr-xr-x 1 user user 3.1M ... hello.kit

$ ./hello.kit
Hello, world

; starkit = zip 文件 + Tcl 虚拟文件系统
; tclkit = 运行时（解释器 + Tk + 常用包）""",
            "format": [
                ("starkit", "zip 归档，内含 main.tcl 与库"),
                ("tclkit", "单文件运行时"),
                ("starpack", "运行时 + 脚本合成一个可执行"),
                ("挂载", "VFS 把 zip 当目录"),
            ],
            "note": "Tcl 的分发方式很符合它的哲学：不发明新格式，直接把 zip 当文件系统，把解释器当运行时。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "Emacs", "compiler": "tclsh", "build": "make", "pkg": "—", "debug": "puts 调试"},
        {"era": "1990s", "editor": "Emacs / Tk 工具", "compiler": "tclsh / wish", "build": "make", "pkg": "—", "debug": "tcl debug"},
        {"era": "2000s", "editor": "Komodo / Emacs", "compiler": "tclsh 8.5", "build": "Makefile", "pkg": "teacup", "debug": "tdbc / 调试器"},
        {"era": "2020s", "editor": "VS Code + Tcl", "compiler": "tclsh 8.6/9", "build": "make", "pkg": "teacup", "debug": "Tcl Dev Kit"},
    ],
    "hello": {
        "file": "hello.tcl",
        "code": r"""puts "Hello, world"
# 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 26 B", "w": 4},
            {"stage": "词列表", "size": "≈ 26 B", "w": 5},
            {"stage": "字节码", "size": "≈ 120 B", "w": 10},
            {"stage": "starkit", "size": "≈ 3.1 MB", "w": 70},
            {"stage": "+ tclkit", "size": "≈ 8 MB", "w": 100},
        ],
        "why": [
            "<strong>一切皆命令</strong>：if/while/proc 都是命令，语言可以被应用扩展。",
            "<strong>一切皆字符串</strong>：数据与代码之间没有硬边界，适合脚本与配置。",
            "<strong>字节码</strong>：8.0 后在内存中编译，提升循环性能。",
            "<strong>starkit</strong>：用 zip + VFS 打包，不发明新容器格式。",
        ],
    },
},

}
