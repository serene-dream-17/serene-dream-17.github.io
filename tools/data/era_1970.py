# -*- coding: utf-8 -*-
"""第一批 · 1970s：8 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"c": {
    "tagline": "为写 UNIX 而生的小语言，最后成了几乎所有操作系统的通用语。",
    "intro": [
        "1972 年，Dennis Ritchie 在贝尔实验室把 B 改造成 C：加入类型、结构体、字节寻址和可移植的编译模型。最初的理由很具体——B 只有一种字类型，无法在 PDP-11 上高效地按字节操作。",
        "C 的产物链是现代工具链的原型：预处理、编译、汇编、链接，每一步都有明确的输入输出。`.c → .i → .s → .o → ELF` 这条链不仅属于 C，也属于 C++、Rust、Go、Swift 等后来者。",
        "C 的另一个决定是「不规定运行时」。没有 GC、没有异常、没有标准输出函数——这些都在库或操作系统里。正因如此，C 能贴近硬件，也把大量责任交给了程序员。",
    ],
    "lineage": {
        "from": ["B", "BCPL", "ALGOL 60"],
        "to": ["C++", "Java", "C#", "Go", "Rust", "Objective-C"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.c",
            "cmd": "$ cat hello.c",
            "code": r"""#include <stdio.h>

int main(void) {
    printf("Hello, world\n");
    return 0;
}""",
            "format": [
                ("编码", "UTF-8 / ASCII，文本"),
                ("预处理", "以 # 开头的行交给 cpp"),
                ("翻译单元", "一个 .c + 它包含的头文件"),
                ("入口", "main，由 C 运行时调用"),
            ],
            "note": "C 的「源文件」并不是编译器真正看到的东西。编译器看到的是预处理之后的翻译单元。",
        },
        {
            "label": "预处理",
            "file": "hello.i",
            "cmd": "$ gcc -E hello.c -o hello.i",
            "code": r"""# 0 "hello.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "hello.c" 2
# 1 "/usr/include/stdio.h" 1 3 4
...
extern int printf (const char *__restrict __format, ...);
...
# 3 "hello.c" 2

int main(void) {
    printf("Hello, world\n");
    return 0;
}""",
            "format": [
                ("扩展名", ".i，纯 C 文本"),
                ("行标记", "# 行号 \"文件\" 标志，供调试定位"),
                ("宏", "全部展开，条件编译已决定"),
                ("头文件", "被原地并入，可能几万行"),
            ],
            "note": "一个 5 行的程序，预处理后可能有两万行，绝大多数来自 stdio.h。`# 1 \"hello.c\"` 这样的行标记让编译器在报错与调试时仍能指回原始文件。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "$ gcc -S -O0 hello.c -o hello.s",
            "code": r"""    .file   "hello.c"
    .text
    .section    .rodata
.LC0:
    .string "Hello, world"
    .text
    .globl  main
    .type   main, @function
main:
.LFB0:
    .cfi_startproc
    endbr64
    pushq   %rbp
    .cfi_def_cfa_offset 16
    .cfi_offset 6, -16
    movq    %rsp, %rbp
    .cfi_def_cfa_register 6
    leaq    .LC0(%rip), %rdi
    movl    $0, %eax
    call    printf@PLT
    movl    $0, %eax
    popq    %rbp
    .cfi_def_cfa 7, 8
    ret
    .cfi_endproc""",
            "format": [
                ("语法", "GNU as（AT&T：源在左，目标在右）"),
                ("段", ".text 代码 · .rodata 只读数据"),
                ("调用", "printf@PLT，经过程序链接表"),
                ("CFI", "调用帧信息，供调试与异常回溯"),
            ],
            "note": "同一个 hello.c，GCC 常把 printf 优化成 puts；这里保留 printf 是为了展示 PLT 调用。`-O2` 会移除栈帧，代码只剩几条指令。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ gcc -c hello.c && xxd -l 64 hello.o",
            "code": r"""$ xxd -l 64 hello.o
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
00000010: 0100 3e00 0100 0000 0000 0000 0000 0000  ..>.............
00000020: 0000 0000 0000 0000 0802 0000 0000 0000  ................
00000030: 0000 0000 4000 0000 0000 4000 0c00 0b00  ....@.....@.....

$ readelf -h hello.o | sed -n '1,12p'
  Class:   ELF64
  Type:    REL (Relocatable file)
  Machine: Advanced Micro Devices X86-64
  Entry:   0x0

$ readelf -S hello.o | grep -E '\.text|\.rodata|\.rela|\.symtab'
  [ 1] .text     PROGBITS  0000000000000000  00000040
  [ 4] .rela.text RELA     0000000000000000  000001a0
  [ 5] .rodata   PROGBITS  0000000000000000  0000005c
  [ 9] .symtab   SYMTAB    0000000000000000  00000128

$ nm hello.o
0000000000000000 T main
                 U printf""",
            "format": [
                ("魔数", "7f 45 4c 46 = \\x7fELF"),
                ("类型", "ET_REL（可重定位目标）"),
                ("机器", "EM_X86_64 = 0x3e"),
                ("段", ".text / .rodata / .rela.text / .symtab"),
                ("符号", "main 已定义，printf 未定义（U）"),
            ],
            "note": "目标文件里没有最终地址：.rela.text 记录了「这条 call 指令要去解析 printf」；链接器负责填上真正的地址。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ gcc -o hello hello.c && file hello",
            "code": r"""$ file hello
hello: ELF 64-bit LSB pie executable, x86-64, dynamically linked,
       interpreter /lib64/ld-linux-x86-64.so.2

$ readelf -h hello | grep -E 'Type|Entry'
  Type:    DYN (Position-Independent Executable)
  Entry:   0x1050

$ readelf -l hello | grep -A1 INTERP
  INTERP  0x...  [Requesting program interpreter:
                  /lib64/ld-linux-x86-64.so.2]

$ readelf -d hello | grep NEEDED
  NEEDED  libc.so.6

$ ./hello
Hello, world""",
            "format": [
                ("类型", "ET_DYN（PIE，位置无关可执行）"),
                ("解释器", "/lib64/ld-linux-x86-64.so.2"),
                ("依赖", "libc.so.6"),
                ("动态表", ".dynamic / .got.plt / .plt"),
                ("入口", "0x1050，先跑 _start 再调 main"),
            ],
            "note": "可执行文件并不直接调用 printf。它调用 PLT 桩，桩再通过 GOT 跳到 libc 里的真实地址；首次调用还会触发动态链接器解析符号。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "ed / vi", "compiler": "cc（PDP-11）", "build": "make（1976）", "pkg": "—", "debug": "adb"},
        {"era": "1980s", "editor": "vi / Emacs", "compiler": "cc / gcc（1987）", "build": "make", "pkg": "—", "debug": "gdb（1986）"},
        {"era": "1990s", "editor": "Emacs / vim", "compiler": "gcc", "build": "make / autoconf", "pkg": "—", "debug": "gdb"},
        {"era": "2000s", "editor": "Eclipse / vim", "compiler": "gcc / clang", "build": "make / CMake", "pkg": "pkg-config", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + clangd", "compiler": "clang / gcc", "build": "CMake / Meson", "pkg": "vcpkg / conan", "debug": "lldb / gdb"},
    ],
    "hello": {
        "file": "hello.c",
        "code": r"""#include <stdio.h>

int main(void) {
    printf("Hello, world\n");
    return 0;
}""",
        "footprint": [
            {"stage": "hello.c", "size": "78 B", "w": 5},
            {"stage": "hello.i", "size": "≈ 18 KB", "w": 24},
            {"stage": "hello.s", "size": "≈ 1.3 KB", "w": 12},
            {"stage": "hello.o", "size": "≈ 1.5 KB", "w": 13},
            {"stage": "hello", "size": "≈ 16 KB", "w": 46},
            {"stage": "+ libc", "size": "≈ 2 MB", "w": 100},
        ],
        "why": [
            "<strong>预处理</strong>：把宏、条件编译、头文件展开成编译器能直接处理的一个翻译单元。",
            "<strong>汇编</strong>：把与机器无关的 C 降到具体指令集，保留符号与段信息。",
            "<strong>目标文件</strong>：允许分别编译；未解析的符号留给链接器。",
            "<strong>链接</strong>：把多个 .o 与库合并，解析 printf，生成可加载的段表。",
            "<strong>动态链接</strong>：printf 的代码不在 hello 里，而在 libc.so；运行时由 ld.so 绑定。",
        ],
    },
},

# ============================================================
"pascal": {
    "tagline": "Wirth 为教学设计的语言，先用 P-code 证明了可移植，再靠 Turbo Pascal 统治了 DOS 桌面。",
    "intro": [
        "Pascal 由 Niklaus Wirth 在 1970 年发布，目标是教「结构化程序设计」：强类型、嵌套过程、清晰的 begin/end、没有 goto 的诱惑。它很快成为大学课程的标准语言。",
        "Pascal 的可移植性来自一个聪明的中间产物：P-code。Pascal-P 编译器不直接生成机器码，而是生成一台虚拟栈机的指令；换平台只需要实现 P 解释器。Java 的字节码与 .NET 的 IL 都走着同一条路。",
        "1983 年，Borland 的 Turbo Pascal 把编译器、编辑器、调试器塞进一个几十 KB 的程序，直接生成 DOS 可执行文件。它让 Pascal 从课堂走进了商业桌面。",
    ],
    "lineage": {
        "from": ["ALGOL 60", "ALGOL W"],
        "to": ["Modula-2", "Oberon", "Delphi", "Ada（部分）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.pas",
            "cmd": "$ cat hello.pas",
            "code": r"""program Hello;
begin
  writeln('Hello, world')
end.""",
            "format": [
                ("结构", "program … begin … end."),
                ("语句", "分号分隔，最后一句可省略"),
                ("类型", "强类型，需显式声明"),
                ("大小写", "不敏感"),
            ],
            "note": "Wirth 的设计原则是「少而够用」：没有宏、没有运算符重载、没有异常。语法几乎可以直接映射到一棵简单的语法树。",
        },
        {
            "label": "P-code",
            "file": "hello.pcode",
            "cmd": "Pascal-P 编译器输出（示意）",
            "code": r"""; P-code（栈式字节码）
0:  ENT   1          ; 建立栈帧
1:  LDC   1          ; 字符串字面量地址
2:  LDC   "Hello, world"
3:  SYS   12         ; 写字符串
4:  SYS   13         ; 换行
5:  RET
6:  STP""",
            "format": [
                ("形态", "栈式虚拟机的指令序列"),
                ("可移植", "换机器只需实现 P 解释器"),
                ("栈", "操作数栈 + 活动记录栈"),
                ("影响", "JVM 字节码 / .NET IL 的先声"),
            ],
            "note": "P-code 的指令很小，生成简单，解释器也容易写。代价是性能：每条指令都要经过一次分发。",
        },
        {
            "label": "DOS 可执行",
            "file": "HELLO.EXE",
            "cmd": "Turbo Pascal 3.0 · DOS",
            "code": r"""$ xxd -l 32 HELLO.EXE
00000000: 4d5a 5001 0a00 0000 2000 ffff 0000 0000  MZP..... .......
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................

; MZ 头：
;   4D 5A        "MZ"
;   01 50        最后一页字节数
;   00 0A        页数
;   00 00        重定位项数
;   00 20        头部长度（32 段）""",
            "format": [
                ("格式", "DOS MZ 可执行（.EXE）"),
                ("代码", "直接生成 8086 机器码"),
                ("运行时", "静态链接，无需外部 DLL"),
                ("体积", "最小程序约 2–4 KB"),
            ],
            "note": "Turbo Pascal 不生成 P-code：它直接编译到 8086，把运行时静态链接进去。整个 IDE 常驻内存，编译速度以秒计。",
        },
        {
            "label": "现代原生",
            "file": "hello",
            "cmd": "$ fpc hello.pas",
            "code": r"""$ fpc hello.pas
Free Pascal Compiler version ...
$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ ./hello
Hello, world""",
            "format": [
                ("编译器", "Free Pascal / Delphi"),
                ("后端", "原生代码，可选 LLVM"),
                ("运行时", "静态或动态链接"),
                ("平台", "Windows / Linux / macOS / 嵌入式"),
            ],
            "note": "Free Pascal 保留了 Object Pascal 语法，同时支持多平台与原生代码。Delphi 则把这条路带进了 Windows 商业开发。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "行编辑器", "compiler": "Pascal-P（P-code）", "build": "P 解释器", "pkg": "—", "debug": "—"},
        {"era": "1980s", "editor": "Turbo Pascal IDE", "compiler": "Turbo Pascal", "build": "内置 MAKE", "pkg": "单元（unit）", "debug": "内置调试器"},
        {"era": "1990s", "editor": "Delphi IDE", "compiler": "Delphi", "build": "内置", "pkg": "VCL / 组件", "debug": "集成调试器"},
        {"era": "2020s", "editor": "VS Code + Pascal 扩展", "compiler": "Free Pascal / Delphi", "build": "fpc / MSBuild", "pkg": "fpm / GetIt", "debug": "gdb / IDE"},
    ],
    "hello": {
        "file": "hello.pas",
        "code": r"""program Hello;
begin
  writeln('Hello, world')
end.""",
        "footprint": [
            {"stage": "源码", "size": "≈ 60 B", "w": 5},
            {"stage": "P-code", "size": "≈ 28 B", "w": 8},
            {"stage": "DOS .EXE", "size": "≈ 3 KB", "w": 20},
            {"stage": "P 解释器", "size": "≈ 30 KB", "w": 42},
            {"stage": "原生 ELF", "size": "≈ 40 KB", "w": 48},
        ],
        "why": [
            "<strong>P-code</strong>：用虚拟指令换取可移植性，换平台只重写解释器。",
            "<strong>强类型</strong>：编译期检查数组边界与参数类型，运行时更轻。",
            "<strong>Turbo 的静态链接</strong>：把运行时塞进 EXE，换来「拷贝即运行」。",
            "<strong>现代后端</strong>：Free Pascal 直接生成原生代码，P-code 成为历史层。",
        ],
    },
},

# ============================================================
"smalltalk": {
    "tagline": "在 Smalltalk 里，源码、编译结果和运行环境住在同一个镜像里；保存镜像就是保存一切。",
    "intro": [
        "Smalltalk 诞生于 Xerox PARC，Alan Kay、Dan Ingalls、Adele Goldberg 等人把它做成了一个「活的」编程环境：类、方法、窗口、调试器都在同一个镜像里，修改立即生效。",
        "它的产物链没有传统意义上的「可执行文件」。方法被编译成字节码，装进方法字典；类和全局变量都在对象内存里；保存镜像（snapshot）就是把整个对象内存写成磁盘文件。",
        "`.st` 的 file-out 是另一条路：把类与方法写成文本 chunk，用于版本管理、交换代码或在另一台机器上 file-in。`!` 是 chunk 分隔符，不是注释。",
    ],
    "lineage": {
        "from": ["Simula 67", "Lisp", "Sketchpad"],
        "to": ["Objective-C（消息）", "Ruby（一切皆对象）", "Self", "Pharo"],
    },
    "chain": [
        {
            "label": "源码（file-out）",
            "file": "Hello.st",
            "cmd": "$ cat Hello.st",
            "code": r"""Object subclass: #Hello
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'!

!Hello class methodsFor: 'examples'!
world
    ^ 'Hello, world'!
! !""",
            "format": [
                ("格式", "chunk 格式，! 分隔"),
                ("内容", "类定义 / 方法分类 / 方法体"),
                ("file-out", "把镜像中的代码写成文本"),
                ("file-in", "把文本读回镜像"),
            ],
            "note": "`!` 不是注释，而是 chunk 的边界。file-out 的文本可以被版本控制系统管理，但镜像里的活对象才是真正的程序。",
        },
        {
            "label": "编译方法",
            "file": "CompiledMethod",
            "cmd": "Hello class >> #world  （示意）",
            "code": r"""; CompiledMethod: Hello class >> #world
header:    numLiterals=2  numTemps=0  numArgs=0
literals:  #world   'Hello, world'

bytecode:
  0: push self
  1: push literal 'Hello, world'
  2: return top

; 字节码编号依 Smalltalk-80 规范；
; 不同实现（Pharo / Squeak）有扩展""",
            "format": [
                ("产物", "CompiledMethod 对象"),
                ("字节码", "栈式指令，1 字节为主"),
                ("字面量", "方法持有的常量表"),
                ("安装", "放入方法字典，立即生效"),
            ],
            "note": "方法不是存成 .class 文件，而是内存里的对象。保存镜像时，字节码与字面量一起被写进对象内存。",
        },
        {
            "label": "镜像",
            "file": "Pharo.image",
            "cmd": "$ ls -lh Pharo.image Pharo.changes",
            "code": r"""$ ls -lh Pharo.image Pharo.changes
-rw-r--r-- 1 user user 78M ... Pharo.image
-rw-r--r-- 1 user user 2.1M ... Pharo.changes

; 镜像结构（示意）
;   header       magic / version / endianness / word size
;   object table 所有对象的地址表
;   class table  类与方法字典
;   heap         代码、字符串、集合、窗口状态""",
            "format": [
                ("镜像", "整个对象内存的二进制快照"),
                ("包含", "代码、类、实例、窗口、进程"),
                ("绑定", "字长、字节序、实现版本"),
                ("启动", "恢复镜像，而不是重新初始化"),
            ],
            "note": "镜像让「保存程序」和「保存运行状态」变成同一件事。代价是它与实现、平台深度绑定。",
        },
        {
            "label": "变更日志",
            "file": "Pharo.changes",
            "cmd": "（changes file）",
            "code": r"""!Hello class methodsFor: 'examples' stamp: 'me 10/27/2026 10:00'!
world
    ^ 'Hello, world'!
! !

; changes 文件追加记录每次编辑
; 可用于恢复、重放、审计
; 镜像 + changes = 当前系统 + 历史""",
            "format": [
                ("作用", "记录所有源码编辑"),
                ("格式", "chunk 文本，追加写入"),
                ("恢复", "可从 changes 重建部分代码"),
                ("关系", "镜像是状态，changes 是历史"),
            ],
            "note": "Smalltalk 的做法接近「数据库 + 日志」：镜像是快照，changes 是预写日志。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "Smalltalk-76 环境", "compiler": "Smalltalk 编译器", "build": "镜像快照", "pkg": "类别（category）", "debug": "集成调试器"},
        {"era": "1980s", "editor": "Smalltalk-80", "compiler": "字节码编译器", "build": "snapshot", "pkg": "changes / file-out", "debug": "walkback"},
        {"era": "2000s", "editor": "Squeak", "compiler": "字节码编译器", "build": "image", "pkg": "Monticello", "debug": "调试器"},
        {"era": "2020s", "editor": "Pharo / Glamorous", "compiler": "字节码 + JIT", "build": "Image / Metacello", "pkg": "Metacello", "debug": "调试器"},
    ],
    "hello": {
        "file": "Hello.st",
        "code": r"""!Hello class methodsFor: 'examples'!
world
    ^ 'Hello, world'!
! !

Transcript show: Hello world; cr.""",
        "footprint": [
            {"stage": "file-out", "size": "≈ 130 B", "w": 5},
            {"stage": "字节码", "size": "≈ 24 B", "w": 8},
            {"stage": "方法对象", "size": "≈ 80 B", "w": 12},
            {"stage": "镜像", "size": "≈ 78 MB", "w": 100},
            {"stage": "changes", "size": "≈ 2 MB", "w": 55},
        ],
        "why": [
            "<strong>消息发送</strong>：调用是「给对象发消息」，方法查找在运行时完成。",
            "<strong>字节码</strong>：源码先编译成栈式字节码，再装进方法字典。",
            "<strong>镜像</strong>：对象内存整体保存，启动即恢复，没有单独的「初始化」阶段。",
            "<strong>changes</strong>：所有编辑追加记录，镜像是快照，日志是历史。",
        ],
    },
},

# ============================================================
"prolog": {
    "tagline": "程序不是步骤，而是一组事实与规则；运行就是让机器去寻找一个证明。",
    "intro": [
        "Prolog 由 Alain Colmerauer 与 Philippe Roussel 在马赛于 1972 年实现，Robert Kowalski 在爱丁堡给出了逻辑基础。它的程序由事实（fact）与规则（rule）组成，执行就是提问（query）并让系统做归结与回溯。",
        "Prolog 的「产物」有两层：源码里的子句，和运行时数据库里的子句。consult 把子句装进数据库，解释器直接在上面推理；编译器则把子句编译成 WAM（Warren Abstract Machine）指令，再交给 WAM 模拟器或原生后端。",
        "WAM 是逻辑编程的「字节码」：get_structure、unify_variable、call、proceed 这些指令描述了合一与回溯。它让 Prolog 的性能从「直接解释子句」提升到可用。",
    ],
    "lineage": {
        "from": ["一阶逻辑", "归结原理", "ALGOL（语法）"],
        "to": ["Erlang（语法）", "Datalog", "约束逻辑编程"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "greet.pl",
            "cmd": "$ cat greet.pl",
            "code": r"""greet(Name) :-
    write('Hello, '),
    write(Name),
    nl.

?- greet('world').

% 逗号 = 合取；句号结束子句
% 大写开头 = 变量；小写/引号 = 原子""",
            "format": [
                ("事实", "parent(tom, bob)."),
                ("规则", "Head :- Body."),
                ("变量", "大写或 _ 开头"),
                ("查询", "?- Goal."),
            ],
            "note": "Prolog 的程序没有「主函数」。你给它一个目标，它尝试让目标成立；打印只是副作用。",
        },
        {
            "label": "WAM 指令",
            "file": "greet.wam",
            "cmd": "$ swipl -O -c greet.pl（示意）",
            "code": r"""; greet/1 编译为 WAM
clause greet/1:
    allocate 2
    get_variable Y1, A1
    put_atom 'Hello, ', A1
    call write/1, 1
    put_value Y1, A1
    call write/1, 1
    call nl/0, 0
    deallocate
    proceed""",
            "format": [
                ("中间码", "WAM 指令序列"),
                ("合一", "get_* / unify_* 匹配参数"),
                ("调用", "call 谓词/元数"),
                ("回溯", "choice point + trail"),
            ],
            "note": "WAM 把「匹配参数」「建立选择点」「回溯」变成显式指令。它是 Prolog 性能的关键，也影响了后来的 Erlang 与 Datalog 实现。",
        },
        {
            "label": "运行时数据库",
            "file": "clause database",
            "cmd": "?- listing(greet/1).",
            "code": r"""?- listing(greet/1).
greet(A) :-
    write('Hello, '),
    write(A),
    nl.

?- assertz(fact(hello)).
true.

?- fact(X).
X = hello.

; consult 时子句进入数据库
; assert / retract 可在运行时修改""",
            "format": [
                ("数据库", "子句的有序集合"),
                ("consult", "把文件中的子句装入"),
                ("assert/retract", "运行时增删子句"),
                ("索引", "首参数索引加速匹配"),
            ],
            "note": "Prolog 的「程序」可以在运行时改变：断言的子句参与后续查询。这让它更像数据库而不是传统程序。",
        },
        {
            "label": "可执行",
            "file": "greet",
            "cmd": "$ swipl -O --toplevel=halt -o greet greet.pl",
            "code": r"""$ swipl -O --toplevel=halt -o greet greet.pl
$ ./greet
Hello, world

$ file greet
greet: ELF 64-bit LSB pie executable, x86-64 ...

; 也可用 SICStus / GNU Prolog 编译
; 或保持解释执行：swipl greet.pl""",
            "format": [
                ("编译", "子句 → WAM → 原生/字节码"),
                ("打包", "把运行时与数据库嵌入可执行"),
                ("解释", "不编译也可直接 consult"),
                ("产物", "可执行文件或数据库状态"),
            ],
            "note": "Prolog 不强制编译。很多系统直接 consult 源码，把子句装进数据库——这本身就是一种「加载」。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "行编辑器", "compiler": "Marseille Prolog", "build": "consult", "pkg": "—", "debug": "trace"},
        {"era": "1980s", "editor": "Emacs", "compiler": "Edinburgh Prolog", "build": "consult", "pkg": "库文件", "debug": "trace / spy"},
        {"era": "2000s", "editor": "Emacs / SWI 编辑器", "compiler": "SWI-Prolog", "build": "qsave_program", "pkg": "pack", "debug": "trace / debug"},
        {"era": "2020s", "editor": "VS Code + Prolog 扩展", "compiler": "SWI / SICStus / GNU", "build": "qsave_program", "pkg": "pack", "debug": "trace / debugger"},
    ],
    "hello": {
        "file": "hello.pl",
        "code": r"""hello :-
    write('Hello, world'),
    nl.

?- hello.""",
        "footprint": [
            {"stage": "源码", "size": "≈ 60 B", "w": 5},
            {"stage": "WAM", "size": "≈ 120 B", "w": 10},
            {"stage": "数据库", "size": "≈ 200 B", "w": 14},
            {"stage": "可执行", "size": "≈ 12 MB", "w": 90},
        ],
        "why": [
            "<strong>合一</strong>：参数匹配不是赋值，而是寻找变量绑定。",
            "<strong>回溯</strong>：失败时回到最近的选择点，尝试其他子句。",
            "<strong>WAM</strong>：把合一与回溯编译成显式指令，提升性能。",
            "<strong>数据库</strong>：子句可以在运行时增删，程序状态与代码合一。",
        ],
    },
},

# ============================================================
"ml": {
    "tagline": "1973 年，Milner 在 LCF 里需要一种能安全操作证明的语言；类型推断和模块系统从这里进入主流。",
    "intro": [
        "ML 最初是 Edinburgh LCF 的元语言（Meta Language）：用来写证明策略，必须安全、可组合、能在编译期抓住错误。1973 年的第一版由 Robin Milner 与同事完成。",
        "它带来了 Hindley–Milner 类型推断：你不写类型，编译器也能推出最一般的类型；一旦推出，就严格检查。异常、代数数据类型、模式匹配、模块（后来在 SML 中）都从这里进入主流。",
        "ML 的产物链体现了「先证明、再生成」：源码先被 elaboration 成带显式类型的 Core，再做闭包转换/ CPS，最后交给后端生成机器码或堆镜像。",
    ],
    "lineage": {
        "from": ["LCF", "λ 演算", "ALGOL 60"],
        "to": ["Standard ML", "OCaml", "Haskell", "F#", "Rust（类型系统影响）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.sml",
            "cmd": "$ cat hello.sml",
            "code": r"""fun greet name = "Hello, " ^ name

val _ = print (greet "world" ^ "\n")

(* 类型由编译器推断：
   greet : string -> string
*)""",
            "format": [
                ("函数", "fun 定义，模式匹配参数"),
                ("类型", "推断，不必显式标注"),
                ("字符串", "^ 拼接"),
                ("注释", "(* … *)"),
            ],
            "note": "源码里没有类型标注，但编译器在内部为每个表达式求出类型。类型错误在编译期就会被拒绝。",
        },
        {
            "label": "Core（带类型）",
            "file": "core.ml",
            "cmd": "（elaboration 输出，示意）",
            "code": r"""val greet : string -> string =
  fn (name : string) => "Hello, " ^ name

val it : unit =
  print (greet "world" ^ "\n")

(* 语法糖已去掉：
   - 柯里化/元组已显式
   - 类型标注已插入
   - 模式匹配已降为 case
*)""",
            "format": [
                ("Core", "去糖后的核心语言"),
                ("类型", "每个绑定都有显式类型"),
                ("模式", "降为 case / 投影"),
                ("作用", "后续优化的稳定输入"),
            ],
            "note": "Core 是 ML 编译器的中间表示。类型推断的结果就在这里固化，后续阶段不再猜类型。",
        },
        {
            "label": "闭包转换",
            "file": "closure",
            "cmd": "（示意）",
            "code": r"""; 闭包转换
greet = closure {
    code: fn(name) => concat("Hello, ", name),
    env:  {}
}

; 自由变量被放进环境
; 之后可做 CPS / 去函数化 / 直接生成代码""",
            "format": [
                ("闭包", "代码指针 + 环境"),
                ("自由变量", "显式放入环境"),
                ("后续", "CPS / 去函数化 / 寄存器分配"),
                ("保证", "类型安全在转换中保持"),
            ],
            "note": "闭包转换把「函数」变成运行时可表示的对象；从这一步开始，语言逐渐接近机器。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ mlton hello.sml && ./hello",
            "code": r"""$ mlton hello.sml
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; MLton：全程序优化 + 原生代码
; SML/NJ：heap image + 运行时""",
            "format": [
                ("MLton", "全程序编译，生成原生 ELF"),
                ("SML/NJ", "heap image + runtime"),
                ("链接", "静态链接运行时"),
                ("产物", "可执行文件或堆镜像"),
            ],
            "note": "ML 的实现分成两大路线：MLton 做全程序优化，SML/NJ 保存 heap image。前者像 C，后者像 Lisp。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "电传打字机 / Emacs", "compiler": "Edinburgh LCF ML", "build": "make", "pkg": "—", "debug": "—"},
        {"era": "1980s", "editor": "Emacs", "compiler": "SML/NJ", "build": "CM", "pkg": "—", "debug": "—"},
        {"era": "2000s", "editor": "Emacs", "compiler": "MLton / SML/NJ", "build": "make / CM", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + SML 扩展", "compiler": "MLton / MLKit", "build": "make / CM", "pkg": "smlpkg", "debug": "gdb"},
    ],
    "hello": {
        "file": "hello.sml",
        "code": r"""val _ = print "Hello, world\n"
(* 输出：Hello, world *)""",
        "footprint": [
            {"stage": "源码", "size": "≈ 30 B", "w": 4},
            {"stage": "Core", "size": "≈ 90 B", "w": 8},
            {"stage": "闭包/IR", "size": "≈ 400 B", "w": 14},
            {"stage": "目标", "size": "≈ 8 KB", "w": 28},
            {"stage": "可执行", "size": "≈ 120 KB", "w": 56},
        ],
        "why": [
            "<strong>类型推断</strong>：不写类型也能得到最一般类型，编译期严格检查。",
            "<strong>Core</strong>：去糖 + 显式类型，成为后续优化的稳定中间表示。",
            "<strong>闭包转换</strong>：把函数变成代码指针 + 环境，接近机器表示。",
            "<strong>全程序优化</strong>：MLton 能看到整个程序，做跨模块内联与去函数化。",
        ],
    },
},

# ============================================================
"scheme": {
    "tagline": "1975 年，Sussman 与 Steele 用最小的规则做出了一个支持尾调用与续延的 Lisp 方言。",
    "intro": [
        "Scheme 诞生于 MIT，Guy Steele 与 Gerald Sussman 在 1975 年把它做成一门极简的 Lisp：只有 lambda、if、quote 等少数特殊形式，其余都能用它们定义。词法作用域、尾调用、一等续延是它的标志。",
        "Scheme 的宏系统 syntax-rules 是「卫生宏」：展开时不会意外捕获用户变量。宏在编译期运行，输出是核心表达式；这一步让源码与最终代码之间出现了明显的中间层。",
        "它的编译器传统（Rabbit、Chez、CHICKEN、Racket）常把程序转成 CPS 或 ANF，再做闭包转换与代码生成。续延因此不是库技巧，而是编译策略的一部分。",
    ],
    "lineage": {
        "from": ["Lisp 1.5", "λ 演算", "Actors 模型"],
        "to": ["Racket", "Clojure（部分）", "JavaScript（尾调用提案）", "SICP 教学"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.scm",
            "cmd": "$ cat hello.scm",
            "code": r"""(define (hello name)
  (display "Hello, ")
  (display name)
  (newline))

(hello "world")""",
            "format": [
                ("定义", "define 绑定变量/函数"),
                ("调用", "(f arg …) 前缀记法"),
                ("作用域", "词法作用域"),
                ("尾调用", "尾位置的调用不增长栈"),
            ],
            "note": "Scheme 的语法只有括号与少数特殊形式。`define`、`let`、`cond` 都可以用 lambda 展开。",
        },
        {
            "label": "宏展开",
            "file": "expanded.scm",
            "cmd": "（syntax-rules，示意）",
            "code": r"""(define-syntax swap!
  (syntax-rules ()
    ((_ a b)
     (let ((tmp a))
       (set! a b)
       (set! b tmp)))))

(swap! x y)
;; 展开为：
(let ((tmp x))
  (set! x y)
  (set! y tmp))

;; tmp 是卫生的：不会捕获用户的 tmp""",
            "format": [
                ("宏", "syntax-rules，模式 → 模板"),
                ("卫生", "引入的绑定自动重命名"),
                ("阶段", "编译期展开"),
                ("输出", "核心表达式"),
            ],
            "note": "卫生宏的关键不是「展开」，而是「不捕获」：模板里的 tmp 与用户写的 tmp 是两个不同的变量。",
        },
        {
            "label": "CPS 核心",
            "file": "cps.scm",
            "cmd": "（Rabbit 风格，示意）",
            "code": r""";; 直接风格
(display "Hello, ")

;; CPS 变换
(lambda (k)
  (display "Hello, "
           (lambda (ignored)
             (display "world"
                      (lambda (ignored)
                        (newline
                          (lambda (ignored)
                            (k 'done))))))))

;; 每个调用都带一个续延 k
;; 尾调用 = 直接调用 k，不返回""",
            "format": [
                ("CPS", "Continuation Passing Style"),
                ("续延", "显式的一等函数"),
                ("尾调用", "直接跳转，不压栈"),
                ("用途", "编译器中间表示 / 实现 call/cc"),
            ],
            "note": "CPS 让控制流显式化：函数不再「返回」，而是把结果交给续延。尾调用优化在 CPS 里是自然结果。",
        },
        {
            "label": "编译产物",
            "file": "hello.o / hello",
            "cmd": "$ csc -o hello hello.scm && ./hello",
            "code": r"""$ csc -o hello hello.scm
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; CHICKEN：Scheme → C → 原生
; Chez：原生代码 + 运行时
; Racket：字节码 / 原生""",
            "format": [
                ("CHICKEN", "编译到 C，再交给 C 编译器"),
                ("Chez", "原生代码，极快"),
                ("Racket", "字节码或 Chez 后端"),
                ("续延", "运行时支持，可能复制栈"),
            ],
            "note": "Scheme 的实现差异很大，但共享同一条逻辑链：宏展开 → 核心 → CPS/ANF → 闭包转换 → 代码生成。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "Emacs", "compiler": "Scheme 解释器（MIT）", "build": "—", "pkg": "—", "debug": "—"},
        {"era": "1980s", "editor": "Emacs", "compiler": "Chez Scheme", "build": "make", "pkg": "—", "debug": "调试器"},
        {"era": "2000s", "editor": "DrRacket", "compiler": "Racket / CHICKEN", "build": "raco", "pkg": "raco pkg", "debug": "DrRacket 调试"},
        {"era": "2020s", "editor": "VS Code + Racket 扩展", "compiler": "Chez / Racket / CHICKEN", "build": "raco / make", "pkg": "raco pkg", "debug": "调试器"},
    ],
    "hello": {
        "file": "hello.scm",
        "code": r"""(display "Hello, world")
(newline)""",
        "footprint": [
            {"stage": "源码", "size": "≈ 40 B", "w": 5},
            {"stage": "展开", "size": "≈ 40 B", "w": 6},
            {"stage": "CPS", "size": "≈ 180 B", "w": 12},
            {"stage": "C / 目标", "size": "≈ 2 KB", "w": 20},
            {"stage": "可执行", "size": "≈ 30 KB", "w": 40},
            {"stage": "+ 运行时", "size": "≈ 1 MB", "w": 85},
        ],
        "why": [
            "<strong>极简核心</strong>：特殊形式很少，其余用 lambda 定义，语义容易形式化。",
            "<strong>卫生宏</strong>：在编译期改写语法，且不捕获用户变量。",
            "<strong>CPS</strong>：把控制流变成显式的续延，尾调用与 call/cc 自然实现。",
            "<strong>闭包转换</strong>：把词法作用域变成运行时的环境对象。",
        ],
    },
},

# ============================================================
"forth": {
    "tagline": "Forth 没有语法，只有词；程序是词典，产物是一段可以直接执行的线程码。",
    "intro": [
        "Forth 由 Chuck Moore 在 1970 年前后设计。它没有语句、没有语法树，只有一个后进先出的数据栈，以及一本不断增长的词典。你定义「词」，词调用词，最终整个程序就是词典的一部分。",
        "传统 Forth 的源码不以文件为单位，而以 1024 字节的 block 为单位：16 行 × 64 列。编辑器按网格工作，磁盘按块读写。这种形态来自 1970 年代的机器与存储限制，也塑造了 Forth 的极简美学。",
        "Forth 的产物是线程码（threaded code）：每个词编译成一段地址序列，由内解释器（inner interpreter）逐个取词执行。保存词典与启动代码，就得到一个 turnkey 程序。",
    ],
    "lineage": {
        "from": ["汇编", "栈式计算器", "Chuck Moore 的极简主义"],
        "to": ["Open Firmware", "嵌入式控制", "PostScript（栈式语言）"],
    },
    "chain": [
        {
            "label": "block 源文件",
            "file": "hello.fth",
            "cmd": "（1024 字节 / block）",
            "code": r"""\ block 0 of hello.fth — 16 lines × 64 chars
: HELLO  ." Hello, world" CR ;
HELLO














; 其余行以空格填充到 64 列""",
            "format": [
                ("单位", "1024 字节 block"),
                ("布局", "16 行 × 64 字符"),
                ("编辑", "按块读写，无换行概念"),
                ("注释", "\\ 到行尾 / ( … )"),
            ],
            "note": "block 是 Forth 的「文件系统」：没有目录树，只有编号的 1 KB 块。源码、数据、文档可以放在同一块里。",
        },
        {
            "label": "词典",
            "file": "dictionary",
            "cmd": "WORDS",
            "code": r"""; 词典条目（示意）
name:   "HELLO"        ; 计数 + 字符
link:   → previous     ; 链表
flags:  ...
code:   DOCOL          ; 冒号定义
body:   LIT str TYPE CR EXIT

; 每个词是一个可执行的地址
; 词典从低地址向高地址增长""",
            "format": [
                ("词典", "词名 + 链接 + 代码字段 + 体"),
                ("代码字段", "DOCOL / 原生代码 / 变量"),
                ("查找", "从最新词沿 link 回溯"),
                ("增长", "编译一个词就追加一条"),
            ],
            "note": "Forth 没有独立的符号表：词典就是符号表，也是运行时结构。`WORDS` 遍历它并打印名字。",
        },
        {
            "label": "线程码",
            "file": "threaded code",
            "cmd": "（内解释器）",
            "code": r"""; 间接线程码
HELLO:
    DOCOL
    LIT    str_addr
    COUNT  TYPE
    CR
    EXIT

; inner interpreter:
;   IP → 取词地址 → 跳代码字段 → 执行
;   下一条地址紧跟在后面
; DOCOL / LIT / EXIT 依实现而定""",
            "format": [
                ("形态", "地址序列 + 内解释器"),
                ("IP", "指令指针遍历线程"),
                ("DOCOL", "开始执行冒号定义"),
                ("变体", "间接 / 直接 / 子程序线程"),
            ],
            "note": "线程码让 Forth 程序非常紧凑：一个词通常只占几个地址。代价是每条指令都要经过内解释器分发。",
        },
        {
            "label": "镜像",
            "file": "hello.com",
            "cmd": "$ ls -l hello.com && ./hello.com",
            "code": r"""$ ls -l hello.com
-rw-r--r-- 1 user user 4.2K ... hello.com

$ ./hello.com
Hello, world

; 镜像 = 词典 + 启动代码 + 运行时
; 嵌入式：直接烧进 ROM
; turnkey：开机即运行""",
            "format": [
                ("镜像", "词典 + 启动词的二进制"),
                ("turnkey", "保存后开机直接执行"),
                ("嵌入式", "烧录 ROM / Flash"),
                ("体积", "通常几 KB"),
            ],
            "note": "Forth 的镜像不是「链接产物」，而是「当前词典的冻结」。这和 Lisp 镜像的思路相似，只是对象换成词。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "block 编辑器", "compiler": "Forth 内编译", "build": "SAVE-SYSTEM", "pkg": "词典", "debug": "跟踪 / 单步"},
        {"era": "1980s", "editor": "block 编辑器", "compiler": "F-PC / urForth", "build": "turnkey", "pkg": "词典", "debug": "调试词"},
        {"era": "2000s", "editor": "Emacs", "compiler": "gforth", "build": "make", "pkg": "require", "debug": "gforth 调试"},
        {"era": "2020s", "editor": "VS Code", "compiler": "gforth / SwiftForth", "build": "make", "pkg": "包词", "debug": "见调试器"},
    ],
    "hello": {
        "file": "hello.fth",
        "code": r""": HELLO  ." Hello, world" CR ;
HELLO""",
        "footprint": [
            {"stage": "block", "size": "1 KB（整块）", "w": 10},
            {"stage": "词典条目", "size": "≈ 40 B", "w": 8},
            {"stage": "线程码", "size": "≈ 20 B", "w": 6},
            {"stage": "镜像", "size": "≈ 4 KB", "w": 22},
            {"stage": "运行时", "size": "≈ 8 KB", "w": 32},
        ],
        "why": [
            "<strong>栈</strong>：参数与返回值都在数据栈上，调用约定极简。",
            "<strong>词典</strong>：符号表与运行时结构合一，编译与执行没有明显边界。",
            "<strong>线程码</strong>：程序是地址序列，内解释器逐条分发。",
            "<strong>镜像</strong>：保存词典即保存程序，适合 ROM 与嵌入式。",
        ],
    },
},

# ============================================================
"modula2": {
    "tagline": "Wirth 把「模块」做成语言的一等公民：定义模块说接口，实现模块藏细节。",
    "intro": [
        "Modula-2 由 Niklaus Wirth 在 1978 年发布，是 Pascal 的继任者。它保留强类型与结构化控制，同时加入两个关键设施：模块（module）与并发（coroutine/进程）。",
        "模块被分成定义模块（.def）与实现模块（.mod）：前者只写接口，后者写实现。客户模块编译时只依赖 .def 与编译器生成的符号文件（.sym），实现可以独立替换。",
        "这套设计与今天的「头文件 + 目标文件 + 包」并没有本质区别，但它是第一次把模块边界写进语言本身。Ada、Oberon、Go 的包模型都能看到它的影子。",
    ],
    "lineage": {
        "from": ["Pascal", "Modula"],
        "to": ["Oberon", "Ada（包）", "Go（包）", "Rust（模块）"],
    },
    "chain": [
        {
            "label": "定义模块",
            "file": "Hello.def",
            "cmd": "$ cat Hello.def",
            "code": r"""DEFINITION MODULE Hello;

PROCEDURE Greet*;

END Hello.""",
            "format": [
                ("扩展名", ".def"),
                ("内容", "只写接口，不写实现"),
                ("导出", "名字后的 * 表示对外可见"),
                ("客户", "只依赖这份声明"),
            ],
            "note": "定义模块是客户与实现之间的契约。它不含任何可执行代码，编译后主要产生符号信息。",
        },
        {
            "label": "实现模块",
            "file": "Hello.mod",
            "cmd": "$ cat Hello.mod",
            "code": r"""IMPLEMENTATION MODULE Hello;

FROM InOut IMPORT WriteString, WriteLn;

PROCEDURE Greet;
BEGIN
  WriteString("Hello, world");
  WriteLn
END Greet;

END Hello.""",
            "format": [
                ("扩展名", ".mod"),
                ("内容", "实现 + 私有声明"),
                ("IMPORT", "显式导入依赖"),
                ("一致性", "必须与 .def 的签名匹配"),
            ],
            "note": "实现模块可以持有私有过程与变量；客户看不到它们，也无法依赖它们。",
        },
        {
            "label": "符号与目标",
            "file": "Hello.sym / Hello.obj",
            "cmd": "$ ls -l Hello.sym Hello.obj",
            "code": r"""$ ls -l Hello.sym Hello.obj
-rw-r--r-- 1 user user  1.2K ... Hello.sym
-rw-r--r-- 1 user user  3.4K ... Hello.obj

$ file Hello.obj
Hello.obj: Intel 80386 COFF object file

; .sym 记录导出符号与类型签名
; 客户模块编译时读取它做检查
; 实现改动但接口不变 → 客户不必重编译""",
            "format": [
                ("符号文件", ".sym，编译器私有格式"),
                ("目标", ".obj / .o，平台格式"),
                ("检查", "客户模块对照 .sym 检查签名"),
                ("重编译", "接口不变则无需重编客户"),
            ],
            "note": "符号文件是 Modula-2 独立编译的核心：它比 C 的头文件携带更多类型信息，也比 C 更严格。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ gm2 -o hello Hello.mod && ./hello",
            "code": r"""$ gm2 -o hello Hello.mod
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; 链接：Hello.obj + 运行时 + 系统库""",
            "format": [
                ("编译器", "GNU Modula-2（gm2）"),
                ("链接", "与运行时、系统库合并"),
                ("产物", "原生可执行文件"),
                ("平台", "Linux / Windows / 嵌入式"),
            ],
            "note": "Wirth 后来在 Oberon 里进一步简化了模块系统；Modula-2 的 .def/.mod 分裂仍是最清晰的接口分离教学样本之一。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "Lilith 工作站", "compiler": "Modula-2 编译器", "build": "make", "pkg": "模块库", "debug": "Lilith 调试器"},
        {"era": "1980s", "editor": "Lilith / Logitech", "compiler": "Modula-2 编译器", "build": "make", "pkg": "模块库", "debug": "调试器"},
        {"era": "2000s", "editor": "Emacs", "compiler": "gm2", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code", "compiler": "gm2", "build": "make", "pkg": "—", "debug": "gdb"},
    ],
    "hello": {
        "file": "Hello.mod",
        "code": r"""MODULE Hello;
FROM InOut IMPORT WriteString, WriteLn;
BEGIN
  WriteString("Hello, world");
  WriteLn
END Hello.""",
        "footprint": [
            {"stage": "定义模块", "size": "≈ 60 B", "w": 5},
            {"stage": "实现模块", "size": "≈ 150 B", "w": 8},
            {"stage": "符号文件", "size": "≈ 1.2 KB", "w": 16},
            {"stage": "目标", "size": "≈ 3.4 KB", "w": 28},
            {"stage": "可执行", "size": "≈ 20 KB", "w": 46},
        ],
        "why": [
            "<strong>定义/实现分离</strong>：接口是契约，实现可以替换。",
            "<strong>符号文件</strong>：携带类型签名，支持严格的独立编译。",
            "<strong>显式 IMPORT</strong>：依赖写在模块头部，不需要预处理器。",
            "<strong>强类型</strong>：数组边界、子界、枚举都在编译期检查。",
        ],
    },
},

}
