# -*- coding: utf-8 -*-
"""第一批 · 1950s–1960s：10 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"fortran": {
    "tagline": "第一个真正被广泛使用的「高级」语言：让科学家用公式写程序，把卡片送进 IBM 704。",
    "intro": [
        "1953 年，John Backus 向 IBM 提交了一份备忘录，提议为 704 设计一种接近数学记号的编程语言。当时的主流判断是：自动生成的代码永远追不上人手写的汇编。1957 年交付的 FORTRAN 编译器用优化证明了这个判断是错的，也由此确立了此后半个世纪的一条分工——人写公式，机器负责寄存器分配。",
        "它的物理形态决定了语法：一行程序就是一张 80 列穿孔卡。第 1–5 列放标号，第 6 列非空表示续行，第 7–72 列才是语句，第 73–80 列留给序号。固定列不是风格选择，而是让读卡器不必理解语言也能切分记录。",
        "FORTRAN 的产物链随后分成两条传统：一条是 1950–60 年代的卡片作业（源卡组、控制卡、目标卡组），另一条是我们今天仍在用的 .f90 → 汇编 → ELF。这一页把两条链路放在一起看。",
    ],
    "lineage": {
        "from": ["汇编语言（IBM 704）", "数学公式记法"],
        "to": ["ALGOL 60", "BASIC", "Fortran 77 / 90 / 2018"],
    },
    "chain": [
        {
            "label": "源卡组",
            "file": "MAIN.f",
            "cmd": "$ cat MAIN.f   # 每行一张 80 列卡",
            "code": r"""C     HELLO WORLD — FORTRAN II
C     COL 1-5 LABEL / COL 6 CONTINUATION / COL 7-72 STATEMENT / 73-80 SEQ
      DIMENSION A(10)
      DO 10 I = 1, 10
   10 A(I) = I * 2
      WRITE (6, 20) A(3)
   20 FORMAT (1X, F8.2)
      STOP
      END""",
            "format": [
                ("载体", "80 列穿孔卡，每卡一行"),
                ("编码", "IBM 704 六位 BCD 字符集"),
                ("列规则", "1–5 标号 · 6 续行 · 7–72 语句 · 73–80 序号"),
                ("注释", "第 1 列写 C 或 *"),
                ("标识符", "FORTRAN 66 仅前 6 个字符有效"),
            ],
            "note": "读卡器不需要理解语法：列号就是记录边界。这套固定格式一直保留到 Fortran 90 的自由格式，今天 .f 与 .f90 的区别仍从这里开始。",
        },
        {
            "label": "作业控制卡组",
            "file": "JOB.DECK",
            "cmd": "1959 · IBM 7090 监控系统（FMS 风格）",
            "code": r"""$JOB     BACKUS   HELLO
$FORTRAN
C     SOURCE CARDS FOLLOW
      ...
$EXECUTE
$DATA
$END""",
            "format": [
                ("作用", "告诉监控系统依次编译、装入、运行"),
                ("控制卡", "以 $ 开头，独占一张卡"),
                ("源卡", "夹在 $FORTRAN 与 $EXECUTE 之间"),
                ("数据", "$DATA 之后的卡供程序读取"),
                ("变体", "具体控制卡随机器与监控系统而异"),
            ],
            "note": "在操作系统普及之前，「构建脚本」就是这一叠卡片。顺序错了，作业就失败；这张卡组是今天 Makefile 与 CI 配置的远祖。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "$ gfortran -O0 -S hello.f90",
            "code": r"""    .file   "hello.f90"
    .section    .rodata
.LC0:
    .string "Hello, world"
    .text
    .globl  MAIN__
    .type   MAIN__, @function
MAIN__:
    pushq   %rbp
    movq    %rsp, %rbp
    leaq    .LC0(%rip), %rdi
    call    _gfortran_st_write@PLT
    movl    $12, %esi
    call    _gfortran_transfer_character_write@PLT
    call    _gfortran_st_write_done@PLT
    movl    $0, %eax
    popq    %rbp
    ret""",
            "format": [
                ("语法", "GNU as（AT&T 语法）"),
                ("入口", "MAIN__，由 Fortran 运行时调用"),
                ("字符串", "放进 .rodata，只读"),
                ("I/O", "全部委托给 libgfortran 的运行时函数"),
            ],
            "note": "FORTRAN 的「高级」并不意味着它自己实现 I/O。WRITE 在汇编里变成三次运行时调用：开始记录、搬运字符、结束记录。",
        },
        {
            "label": "目标与可执行",
            "file": "hello.o → hello",
            "cmd": "$ xxd -l 16 hello.o; readelf -h hello",
            "code": r"""$ xxd -l 16 hello.o
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............

$ readelf -h hello.o | head -8
  Class:   ELF64
  Type:    REL (Relocatable file)
  Machine: Advanced Micro Devices X86-64

$ readelf -h hello | grep -E 'Type|Entry'
  Type:    DYN (Position-Independent Executable)
  Entry:   0x1050

$ ldd hello
  libgfortran.so.5 => /lib/x86_64-linux-gnu/libgfortran.so.5
  libc.so.6 => ...""",
            "format": [
                ("目标文件", "ELF64 · ET_REL · 含重定位与符号表"),
                ("可执行", "ELF64 · ET_DYN（PIE）"),
                ("链接", "ld 合并段、解析 libgfortran / libc 符号"),
                ("运行时", "真正的格式化与输出在共享库里"),
            ],
            "note": "今天一个 Fortran hello 的体积主要不是你的代码，而是动态链接所需的表与启动代码。把 -static 加上，libgfortran 会被整个塞进来，体积会跳到几 MB。",
        },
    ],
    "tools": [
        {"era": "1950s", "editor": "卡片穿孔机 IBM 026", "compiler": "FORTRAN 编译器（IBM 704）", "build": "FMS 作业控制卡", "pkg": "—", "debug": "存储转储"},
        {"era": "1960s", "editor": "电传打字机", "compiler": "FORTRAN IV", "build": "作业控制语言（JCL）", "pkg": "—", "debug": "核心转储"},
        {"era": "1980s", "editor": "vi / Emacs", "compiler": "f77 / gcc", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + fortls", "compiler": "gfortran / flang / ifx", "build": "CMake / fpm", "pkg": "fpm", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "HELLO.f90",
        "code": r"""program hello
  implicit none
  write (*, '(A)') 'Hello, world'
end program hello""",
        "footprint": [
            {"stage": "源卡", "size": "7 张卡 · 560 B", "w": 8},
            {"stage": "汇编", "size": "≈ 0.9 KB", "w": 16},
            {"stage": "目标 .o", "size": "≈ 3.2 KB", "w": 30},
            {"stage": "可执行", "size": "≈ 17 KB", "w": 48},
            {"stage": "+ libgfortran", "size": "≈ 3 MB", "w": 100},
        ],
        "why": [
            "<strong>固定列</strong>：让读卡器按物理列切分字段，编译器不必先做完整的词法分析。",
            "<strong>FORMAT 分离</strong>：把「数据长什么样」和「数据怎么算」分开，打印格式可以复用。",
            "<strong>运行时库</strong>：WRITE 的缓冲、格式化、设备处理都在 libgfortran 里，用户代码只负责传参。",
            "<strong>目标文件</strong>：让每个源文件可以独立编译，最后由链接器拼装。",
        ],
    },
},

# ============================================================
"lisp": {
    "tagline": "1958 年，McCarthy 把「程序」写成和「数据」一样的括号；从此语言可以处理语言自己。",
    "intro": [
        "LISP 诞生于对「符号计算」的需求：不是算数，而是操作公式、证明和句子。McCarthy 在 1958 年用 IBM 704 上的实现证明，只要有一种能表示列表的数据结构，加上 eval，就可以把程序本身当作数据来生成和求值。",
        "它的产物链与其他语言不同：源码是 S 表达式，读取器（reader）先把它变成 cons 单元构成的树；编译型实现再把这棵树编译成机器码或字节码，写进 FASL（fast-load）文件；很多实现还可以把整个堆保存成镜像（core image），下次直接恢复。",
        "这条链解释了 Lisp 的两个标志：宏在读取/编译期工作，所以「源码」不是最终语法；FASL 与镜像跳过读取器，所以加载快。",
    ],
    "lineage": {
        "from": ["λ 演算", "IPL（信息处理语言）"],
        "to": ["Scheme", "Common Lisp", "Clojure", "Emacs Lisp"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.lisp",
            "cmd": "$ cat hello.lisp",
            "code": r"""(defun hello (name)
  (format t "Hello, ~a!~%" name))

(hello "world")""",
            "format": [
                ("语法", "S 表达式，前缀记法"),
                ("结构", "列表即函数调用，第一个元素是操作符"),
                ("注释", "分号到行尾"),
                ("大小写", "读取器默认折叠为大写（Common Lisp）"),
            ],
            "note": "括号不是装饰，而是语法树本身。读取器把这段文本直接读成一棵可遍历的树，求值器或编译器随后消费这棵树。",
        },
        {
            "label": "读取器输出",
            "file": "cons 树",
            "cmd": "(read-from-string \"(hello \\\"world\\\")\")",
            "code": r"""(DEFUN HELLO (NAME)
  (FORMAT T "Hello, ~a!~%" NAME))

;; 内部不是文本，而是 cons 单元
;; 每个 cons = 两个机器字：car | cdr
;;
;; [ DEFUN | * ] --> [ HELLO | * ] --> [ (NAME) | * ] --> [ BODY | NIL ]
;;
;; 符号 HELLO 被 intern 到包中，所有出现共享同一个对象
;; 字符串是 simple-vector，不是 cons""",
            "format": [
                ("cons", "两个字段：car 与 cdr"),
                ("符号", "intern 后全局唯一，带包归属"),
                ("字符串", "向量，带长度与填充指针"),
                ("数字", "立即数或 boxed 对象，视实现而定"),
            ],
            "note": "源码文本在这一步已经消失。宏与编译器拿到的都是树；这也是为什么 Lisp 的宏能看见「代码的形状」。",
        },
        {
            "label": "编译与 FASL",
            "file": "hello.fasl",
            "cmd": "$ sbcl --eval '(compile-file \"hello.lisp\")'",
            "code": r"""; compiling file "hello.lisp"
; disassembly of HELLO (示意)
;   6A: MOV  RAX, [RDI+...]      ; name
;   71: MOV  RDI, #<FDEFN FORMAT>
;   80: CALL [RAX+...]
;   85: RET

;; FASL 结构（实现相关，示意）
;;   header : magic / word size / version / features
;;   blocks : code objects / literals / symbols / debug info
;;   loader : 重定位后直接 mmap 或复制进堆""",
            "format": [
                ("FASL", "Fast Load，编译器产物"),
                ("内容", "机器码 + 字面量 + 符号 + 调试信息"),
                ("绑定", "与实现版本、字长、特性集相关"),
                ("加载", "跳过读取器、宏展开与大部分编译"),
            ],
            "note": "FASL 不是可执行文件，而是「等待被装进某个 Lisp 镜像的代码块」。它通常不可跨实现移植。",
        },
        {
            "label": "镜像",
            "file": "sbcl.core",
            "cmd": "$ ls -lh sbcl.core && sbcl --core sbcl.core",
            "code": r"""$ ls -lh sbcl.core
-rw-r--r-- 1 user user 42M ... sbcl.core

$ sbcl --core sbcl.core --eval '(hello "world")'
Hello, world!

;; 镜像 = 整个堆的线性快照（示意）
;;   header        版本 / 字长 / 堆起始 / 动态空间
;;   read-only     code, literals, symbols, packages
;;   static        CLOS 类、方法表、全局变量
;;   dynamic       运行时分配的对象""",
            "format": [
                ("镜像", "整个 Lisp 堆的二进制快照"),
                ("包含", "代码、符号、包、CLOS、全局状态"),
                ("绑定", "OS、字长、实现版本"),
                ("可执行", "save-lisp-and-die 可生成 standalone binary"),
            ],
            "note": "镜像是 Lisp 与 Smalltalk 共有的思路：把「运行中的系统」本身当作产物保存。启动不再是初始化，而是恢复。",
        },
    ],
    "tools": [
        {"era": "1958", "editor": "卡片 / 电传打字机", "compiler": "LISP 1.5（IBM 7090）", "build": "—", "pkg": "—", "debug": "—"},
        {"era": "1970s", "editor": "Emacs（ELisp）", "compiler": "Maclisp / Franz Lisp", "build": "make", "pkg": "—", "debug": "trace / 断点"},
        {"era": "1980s", "editor": "Symbolics Genera", "compiler": "CL 编译器", "build": "defsystem", "pkg": "—", "debug": "Genera 调试器"},
        {"era": "2020s", "editor": "Emacs + SLIME", "compiler": "SBCL / CCL", "build": "ASDF", "pkg": "Quicklisp", "debug": "SLDB"},
    ],
    "hello": {
        "file": "hello.lisp",
        "code": r"""(defun hello ()
  (format t "Hello, world~%"))

(hello)""",
        "footprint": [
            {"stage": "源码", "size": "≈ 70 B", "w": 6},
            {"stage": "cons 树", "size": "≈ 1 KB", "w": 14},
            {"stage": "机器码", "size": "≈ 2 KB", "w": 20},
            {"stage": "FASL", "size": "≈ 4 KB", "w": 26},
            {"stage": "镜像", "size": "≈ 42 MB", "w": 100},
        ],
        "why": [
            "<strong>读取器与求值器分离</strong>：read 产生数据，eval 消费数据，语言因此可以操作自己。",
            "<strong>宏在编译期运行</strong>：它在树变成代码之前改写树，所以源码不是最终形态。",
            "<strong>FASL</strong>：跳过读取与宏展开，只做重定位，加载速度接近 mmap。",
            "<strong>镜像</strong>：把运行时状态整体冻结，启动时直接恢复，不必重新初始化世界。",
        ],
    },
},

# ============================================================
"algol60": {
    "tagline": "它没有赢得市场，却定义了此后所有语言怎么说「如果」「循环」和「块」。",
    "intro": [
        "1958 年，来自欧美的一批计算机科学家在苏黎世开会，目标是设计一种不绑定任何机器的通用算法语言。1960 年的报告给出了最终版本：块结构、递归、按名调用、自定义数组下界，以及一套用 BNF 写成的完整语法。",
        "ALGOL 60 最重要的产物可能不是某个可执行文件，而是那份语言报告本身。它第一次让语法成为可机械检查的对象，也让「语言规范」成为独立的工程文档。",
        "在实现层面，ALGOL 60 故意不管 I/O，也不规定内存布局。结果是每个实现都长得很不一样：Elliott 803、Ferranti Atlas、Burroughs B5000 各有自己的编译器和装入器。",
    ],
    "lineage": {
        "from": ["FORTRAN", "ALGOL 58", "λ 演算"],
        "to": ["Pascal", "C", "Simula", "Ada", "Modula-2"],
    },
    "chain": [
        {
            "label": "语言报告",
            "file": "ALGOL60-REPORT",
            "cmd": "1960 · Communications of the ACM",
            "code": r"""<program>      ::= <block> | <compound statement>
<block>        ::= begin <declaration list> ; <statement list> end
<statement>    ::= <unlabelled statement>
                 | <label> : <statement>
<if statement> ::= if <Boolean expression> then <statement>
                 | if <Boolean expression> then <statement>
                   else <statement>""",
            "format": [
                ("载体", "期刊论文 / 技术报告"),
                ("记法", "BNF（Backus–Naur Form）"),
                ("作用", "语法成为可机械检查的对象"),
                ("影响", "此后几乎所有语言规范"),
            ],
            "note": "Backus 在 1959 年提出 BNF，Naur 在 ALGOL 60 报告中采用并推广。语言报告本身就是这一页的「源文件」。",
        },
        {
            "label": "源码",
            "file": "hello.algol",
            "cmd": "$ cat hello.algol",
            "code": r"""begin
  integer i;
  real array a[1:10];
  procedure bump(x); real x;
  begin x := x + 1 end;
  for i := 1 step 1 until 10 do a[i] := i;
  bump(a[3]);
  outreal(1, a[3])
end""",
            "format": [
                ("块结构", "begin … end，声明在使用之前"),
                ("类型", "integer / real / Boolean"),
                ("数组", "下界由程序员指定，如 [1:10]"),
                ("参数", "按值或按名（call by name）"),
                ("I/O", "没有标准，随实现"),
            ],
            "note": "bump(a[3]) 是按名调用：每次在过程体里用到 x，都会重新求值 a[3]。这既强大又危险，后来几乎被所有语言放弃。",
        },
        {
            "label": "编译中间",
            "file": "thunk",
            "cmd": "（实现示意）",
            "code": r"""; bump(a[3]) 的按名调用：实参不是值，而是一段可重复求值的代码
THUNK_A3:
    LDA   I            ; 计算下标
    SUB   #1
    MUL   #4           ; real 的字节宽度
    ADD   A_BASE
    JMP   (RET)        ; 返回「地址」，不是值

BUMP:
    ; 每次引用 x：
    CALL  THUNK_A3
    ...                ; 间接取值 / 写回""",
            "format": [
                ("thunk", "把实参表达式包成无参过程"),
                ("求值", "每次引用参数时重新执行"),
                ("代价", "重复求值、别名、副作用"),
                ("替代", "后来的语言改用按值 / 按引用"),
            ],
            "note": "按名调用是 ALGOL 60 最著名的语义实验。它需要编译器生成 thunk，也让程序的求值顺序变得难以推理。",
        },
        {
            "label": "目标与装入",
            "file": "load map",
            "cmd": "（各实现不同）",
            "code": r"""$ load hello
  TEXT   0x0000–0x0A3F   2624 words
  DATA   0x0A40–0x0B1F    224 words
  ENTRY  MAIN

; Burroughs B5000 直接把块结构做进硬件：
;   显示寄存器（display）指向各层栈帧
;   数组越界由硬件检查""",
            "format": [
                ("编译器", "每个实现一套，无统一工具链"),
                ("目标", "机器字 / 汇编 / 装入模块"),
                ("链接", "早期多为一次性装入"),
                ("硬件", "B5000 用 display 支持块结构"),
            ],
            "note": "ALGOL 60 没有规定 ABI，也没有标准库。它的遗产主要在语法与语义，而不在可复用的产物格式。",
        },
    ],
    "tools": [
        {"era": "1960s", "editor": "纸带 / 卡片", "compiler": "Elliott 803 ALGOL", "build": "装入器", "pkg": "—", "debug": "转储"},
        {"era": "1960s", "editor": "电传打字机", "compiler": "Atlas ALGOL", "build": "作业控制", "pkg": "—", "debug": "—"},
        {"era": "1970s", "editor": "行编辑器", "compiler": "ALGOL 60 编译器", "build": "—", "pkg": "—", "debug": "—"},
        {"era": "2020s", "editor": "VS Code", "compiler": "GNU MARST", "build": "make", "pkg": "—", "debug": "gdb"},
    ],
    "hello": {
        "file": "hello.algol",
        "code": r"""begin
  outstring(1, 'Hello, world');
  outimage
end""",
        "footprint": [
            {"stage": "报告", "size": "≈ 30 页", "w": 20},
            {"stage": "源码", "size": "≈ 180 B", "w": 8},
            {"stage": "thunk/汇编", "size": "≈ 1.2 KB", "w": 18},
            {"stage": "目标", "size": "≈ 2 KB", "w": 26},
            {"stage": "可执行", "size": "≈ 8 KB", "w": 40},
        ],
        "why": [
            "<strong>BNF</strong>：把语法从自然语言描述变成可验证的形式规则。",
            "<strong>块结构</strong>：名字的作用域由 begin/end 决定，栈帧与显示寄存器由此而来。",
            "<strong>按名调用</strong>：用 thunk 把「表达式」延迟到使用时求值，代价是重复求值。",
            "<strong>无标准 I/O</strong>：语言只管算法，设备差异留给实现——这也是它难以移植的原因之一。",
        ],
    },
},

# ============================================================
"cobol": {
    "tagline": "为了让账本能被机器读，它把「数据长什么样」写进了语言；六十年后，银行仍在运行它。",
    "intro": [
        "1959 年，美国国防部召集计算机制造商与用户开会，目标是统一商业数据处理的语言。COBOL 不是由某位语言设计师独立完成的，而是委员会产物：它的每一部分都对应一类现实文档——文件、记录、字段、报表。",
        "COBOL 把数据描述提升到与过程同等的位置。DATA DIVISION 里的 PIC X(5)、PIC 9(7)V99 不是注释，而是内存布局与打印格式的共同契约。这也是它能在银行、保险、税务系统里活到今天的原因。",
        "它的源码是固定 80 列的卡片镜像；编译产物在大型机上是 load module，在 GnuCOBOL 上则先被翻译成 C。两条路径都保留着同一种「记录」思维。",
    ],
    "lineage": {
        "from": ["FLOW-MATIC", "COMTRAN", "商业报表格式"],
        "to": ["PL/I", "SQL 的数据定义", "现代报表 DSL"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.cob",
            "cmd": "$ cat -A hello.cob | head",
            "code": r"""       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-NAME PIC X(5) VALUE "WORLD".
       PROCEDURE DIVISION.
           DISPLAY "HELLO, " WS-NAME.
           STOP RUN.""",
            "format": [
                ("列规则", "1–6 序号 · 7 指示符 · 8–72 正文 · 73–80 标识"),
                ("指示符", "* 注释 · - 续行 · / 换页"),
                ("Area A", "第 8–11 列：部、段、层号 01"),
                ("Area B", "第 12–72 列：语句与子句"),
                ("固定格式", "默认 80 列，现代编译器可放宽"),
            ],
            "note": "源码的缩进不是美学：第 8 列与第 12 列是语法的一部分。层号 01 必须从 Area A 开始，DISPLAY 必须落在 Area B。",
        },
        {
            "label": "中间 C",
            "file": "hello.c",
            "cmd": "$ cobc -C hello.cob",
            "code": r"""/* Generated by GnuCOBOL (cobc -C) — 结构示意 */
#include "libcob.h"

static cob_field ws_name =
    { 5, (cob_u8_t *)"WORLD", NULL };

int main (int argc, char **argv)
{
    cob_init (argc, argv);
    cob_display (0, 1, (cob_u8_t *)"HELLO, ", 7);
    cob_display (0, 1, ws_name.data, ws_name.size);
    cob_stop_run (0);
    return 0;
}""",
            "format": [
                ("策略", "COBOL → C → 本机编译器"),
                ("运行时", "libcob 提供 DISPLAY、文件、排序等"),
                ("字段", "cob_field 描述长度、指针、属性"),
                ("编码", "GnuCOBOL 默认 ASCII，可切换 EBCDIC"),
            ],
            "note": "GnuCOBOL 不直接生成机器码，而是把 COBOL 翻译成 C。C 在这里既是中间表示，也是可移植层。",
        },
        {
            "label": "目标与可执行",
            "file": "hello.o → hello",
            "cmd": "$ cobc -x -o hello hello.cob && file hello",
            "code": r"""$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ readelf -d hello | grep NEEDED
 0x... NEEDED  libcob.so.4
 0x... NEEDED  libc.so.6""",
            "format": [
                ("目标", "ELF64 · ET_REL"),
                ("可执行", "ELF64 · ET_DYN（PIE）"),
                ("依赖", "libcob 运行时"),
                ("大型机", "z/OS 上产物是 load module（PDS 成员）"),
            ],
            "note": "在 z/OS 上，同样的源码由 JCL 编排编译与链接，产物不是 ELF，而是装入 PDS 的 load module。",
        },
        {
            "label": "大型机作业",
            "file": "HELLO.JCL",
            "cmd": "z/OS · JCL",
            "code": r"""//HELLO   JOB (ACCT),'HELLO',CLASS=A,MSGCLASS=X
//COB     EXEC PGM=IGYCRCTL
//SYSIN    DD *
       IDENTIFICATION DIVISION.
       ...
/*
//LKED    EXEC PGM=IEWL,
//             PARM='LIST,XREF'
//SYSLMOD  DD DSN=USER.LOAD(HELLO),DISP=SHR
//SYSLIN   DD DSN=&&OBJ,DISP=(OLD,DELETE)""",
            "format": [
                ("编译", "IGYCRCTL（Enterprise COBOL）"),
                ("链接", "IEWL（linkage editor）"),
                ("产物", "load module，存入 PDS"),
                ("数据", "EBCDIC · 记录式文件 · 定长/变长"),
            ],
            "note": "JCL 是大型机的「构建脚本」：它描述数据集的分配、程序的顺序、失败时做什么。和 1959 年的卡片作业一脉相承。",
        },
    ],
    "tools": [
        {"era": "1960s", "editor": "卡片穿孔机", "compiler": "COBOL-60 编译器", "build": "JCL", "pkg": "—", "debug": "核心转储"},
        {"era": "1980s", "editor": "ISPF 编辑面板", "compiler": "VS COBOL II", "build": "JCL", "pkg": "COPYBOOK 库", "debug": "XPEDITER"},
        {"era": "2000s", "editor": "ISPF / Eclipse", "compiler": "Enterprise COBOL", "build": "JCL / Ant", "pkg": "COPYBOOK / PDS", "debug": "Debug Tool"},
        {"era": "2020s", "editor": "VS Code + COBOL 扩展", "compiler": "GnuCOBOL / IBM Z Open", "build": "make / JCL", "pkg": "—", "debug": "gdb / Debug Tool"},
    ],
    "hello": {
        "file": "HELLO.cob",
        "code": r"""       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO.
       PROCEDURE DIVISION.
           DISPLAY "HELLO, WORLD".
           STOP RUN.""",
        "footprint": [
            {"stage": "源码", "size": "6 行 · 240 B", "w": 8},
            {"stage": "生成 C", "size": "≈ 1.1 KB", "w": 18},
            {"stage": "目标 .o", "size": "≈ 2.4 KB", "w": 28},
            {"stage": "可执行", "size": "≈ 16 KB", "w": 44},
            {"stage": "+ libcob", "size": "≈ 1.5 MB", "w": 90},
        ],
        "why": [
            "<strong>固定列</strong>：源文件首先是 80 列卡片，其次才是程序。",
            "<strong>DATA DIVISION</strong>：数据布局是语言的一部分，PIC 子句同时决定内存与打印。",
            "<strong>翻译成 C</strong>：GnuCOBOL 用 C 作为可移植中间层，运行时在 libcob。",
            "<strong>JCL</strong>：在大型机上，「怎么编译」由作业控制语言描述，而不是 Makefile。",
        ],
    },
},

# ============================================================
"basic": {
    "tagline": "1964 年它让大学生在分时终端上写程序；1970 年代它被塞进 8 位机，成为一代人的第一门语言。",
    "intro": [
        "BASIC 由 John Kemeny 与 Thomas Kurtz 在 Dartmouth 设计，1964 年跑在分时系统上。目标很明确：让非计算机专业的学生在一个会话里写完、运行、改错。行号、即时命令、简单的输入输出，都是为这个目标服务的。",
        "与很多人的印象相反，Dartmouth 的初版 BASIC 是编译执行的。真正把它变成「解释器 + 令牌化内存」的，是 1975 年之后的家用电脑：内存只有几 KB，源码必须压缩成一行行的 token 流。",
        "所以 BASIC 的产物链要分时代看：1964 年是编译，1970 年代是令牌化内存，今天 FreeBASIC 又能直接生成原生可执行文件。",
    ],
    "lineage": {
        "from": ["FORTRAN", "ALGOL 60", "分时系统"],
        "to": ["Visual Basic", "QuickBASIC", "FreeBASIC", "Small Basic"],
    },
    "chain": [
        {
            "label": "源码（1964）",
            "file": "HELLO.BAS",
            "cmd": "$ cat HELLO.BAS",
            "code": r"""10 PRINT "HELLO, WORLD"
20 FOR I = 1 TO 3
30 PRINT I
40 NEXT I
50 END""",
            "format": [
                ("行号", "每行必须编号，用于编辑与跳转"),
                ("语句", "PRINT / FOR / NEXT / END"),
                ("编辑", "按行号覆盖，LIST 列出，RUN 执行"),
                ("终端", "ASR-33 电传打字机，10 字符/秒"),
            ],
            "note": "行号是早期交互式编辑的核心：改一行就是「用同号覆盖」，删一行就是「输入空行」。这套交互后来被全屏编辑器取代，但行号留在了很多 BASIC 方言里。",
        },
        {
            "label": "令牌化内存（1970s）",
            "file": "内存映像",
            "cmd": "(Microsoft BASIC 结构示意)",
            "code": r"""; 8 位机 BASIC 的程序在内存中不是文本
0000: 00 00                 ; 程序结束标记
0002: 0A 00 1C 00           ; 行号 10，行体长度 0x1C
0006: 99                    ; token: PRINT
0007: 0E "HELLO, WORLD" 00  ; 字符串 + 结束
...
001E: 14 00 0A 00           ; 行号 20
0022: 81 ...                ; token: FOR
; LIST 时再把 token 还原成关键词""",
            "format": [
                ("行结构", "行号（2 B）+ 长度 + token 流 + 0x00"),
                ("token", "关键词压成 1 字节，如 PRINT=0x99"),
                ("字符串", "原样保存，以 0x00 结束"),
                ("兼容性", "token 编号随实现而变，源码不通用"),
            ],
            "note": "令牌化既省内存，也加快解释：解释器不必每次扫描关键字。代价是不同 BASIC 的 token 表互不兼容，程序很难迁移。",
        },
        {
            "label": "原生汇编（FreeBASIC）",
            "file": "hello.s",
            "cmd": "$ fbc -r hello.bas",
            "code": r"""    .section .text
main:
    leaq    .L_str(%rip), %rdi
    call    fb_PrintString
    xorl    %eax, %eax
    call    fb_End
    ret
.L_str:
    .asciz  "Hello, world"
    .text""",
            "format": [
                ("编译器", "FreeBASIC（自举，兼容 QuickBASIC）"),
                ("后端", "GNU as / binutils"),
                ("运行时", "fb 运行时库，提供 PRINT / 字符串"),
                ("输出", "COFF / ELF / PE，视目标平台"),
            ],
            "note": "现代 BASIC 方言又回到了编译路线，但保留了 BASIC 的语法与运行时习惯。",
        },
        {
            "label": "可执行（DOS / Windows）",
            "file": "HELLO.EXE",
            "cmd": "$ file HELLO.EXE && xxd -l 64 HELLO.EXE",
            "code": r"""$ file HELLO.EXE
HELLO.EXE: PE32+ executable (console) x86-64, for MS Windows

$ xxd -l 64 HELLO.EXE
00000000: 4d5a 9000 0300 0000 0400 0000 ffff 0000  MZ..............
00000010: b800 0000 0000 0000 4000 0000 0000 0000  ........@.......
00000020: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 8000 0000           ............""",
            "format": [
                ("MZ", "DOS 可执行头，前两个字节 4D 5A"),
                ("e_lfanew", "0x3C 处的 4 字节指向 PE 头"),
                ("PE", "COFF 头 + 可选头 + 节表"),
                ("DOS 时代", "Turbo BASIC / QuickBASIC 生成 .EXE"),
            ],
            "note": "MZ 头是 DOS 的遗产；即使程序早已是 64 位 PE，文件开头仍要放一个能打印「This program cannot be run in DOS mode」的残桩。",
        },
    ],
    "tools": [
        {"era": "1964", "editor": "ASR-33 电传打字机", "compiler": "Dartmouth BASIC 编译器", "build": "分时系统命令", "pkg": "—", "debug": "STOP / 打印变量"},
        {"era": "1970s", "editor": "行号编辑（内置）", "compiler": "解释器（Microsoft BASIC）", "build": "SAVE / LOAD（磁带）", "pkg": "—", "debug": "STOP / TRON"},
        {"era": "1980s", "editor": "GW-BASIC 全屏编辑", "compiler": "QuickBASIC 编译器", "build": "MAKE", "pkg": "—", "debug": "断点 / 单步"},
        {"era": "2020s", "editor": "VS Code", "compiler": "FreeBASIC / QB64", "build": "fbc / make", "pkg": "—", "debug": "gdb"},
    ],
    "hello": {
        "file": "HELLO.BAS",
        "code": r"""10 PRINT "Hello, world"
20 END""",
        "footprint": [
            {"stage": "源码", "size": "2 行 · 34 B", "w": 5},
            {"stage": "令牌", "size": "≈ 18 B", "w": 10},
            {"stage": "汇编", "size": "≈ 0.7 KB", "w": 16},
            {"stage": "目标", "size": "≈ 1.2 KB", "w": 22},
            {"stage": "可执行", "size": "≈ 24 KB", "w": 40},
        ],
        "why": [
            "<strong>行号</strong>：在没有全屏编辑器的年代，行号就是编辑器的索引。",
            "<strong>令牌化</strong>：把关键词压成字节，既省内存又加快解释。",
            "<strong>交互循环</strong>：READ–EVAL–PRINT 的雏形，改一行立即能跑。",
            "<strong>运行时</strong>：PRINT 的格式化与设备输出不在用户代码里。",
        ],
    },
},

# ============================================================
"simula": {
    "tagline": "1967 年，它在语言里放进了 class、对象和继承；Smalltalk、C++、Java 的族谱都从这里分叉。",
    "intro": [
        "Simula 由 Ole-Johan Dahl 与 Kristen Nygaard 在挪威计算中心设计，最初用于离散事件仿真。1967 年的 Simula 67 把仿真需要的东西——对象、类、继承、协同程序——做成了通用语言设施。",
        "class、对象、prefixing（继承）、virtual procedure、垃圾回收、协程，这些今天看起来理所当然的概念，第一次同时出现在一门语言里。C++ 的 class 与虚函数、Java 的对象模型，都能追溯到这份挪威的设计。",
        "Simula 的产物链也早早有了「外部类」：类可以单独编译，客户模块根据声明做类型检查——这就是后来的头文件、符号表与独立编译。",
    ],
    "lineage": {
        "from": ["ALGOL 60", "离散事件仿真"],
        "to": ["Smalltalk", "C++", "Java", "C#", "Eiffel"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "point.sim",
            "cmd": "$ cat point.sim",
            "code": r"""CLASS Point;
   REAL x, y;
   PROCEDURE Move(dx, dy); REAL dx, dy;
   BEGIN x := x + dx; y := y + dy END;
END Point;

BEGIN
   REF(Point) p;
   p :- NEW Point;
   p.Move(1, 2);
END""",
            "format": [
                ("类", "CLASS … END，字段与过程放在一起"),
                ("引用", "REF(Point)，赋值用 :-"),
                ("对象", "NEW 在堆上分配"),
                ("继承", "prefixing：CLASS Sub(Super)"),
            ],
            "note": "「对象」不是语法糖，而是运行时真实存在的堆对象；REF 是指向它的引用，:- 是引用赋值。",
        },
        {
            "label": "外部类声明",
            "file": "point.decl",
            "cmd": "（独立编译的声明文件）",
            "code": r"""EXTERNAL CLASS Point;
   PROCEDURE Move(dx, dy); REAL dx, dy;
END Point;

; 客户模块只看到这份声明：
;   - 字段布局由声明决定
;   - 过程签名用于类型检查
;   - 实现可以单独重新编译""",
            "format": [
                ("独立编译", "类可以单独编译"),
                ("声明", "客户模块依赖 EXTERNAL CLASS"),
                ("类型检查", "编译期核对过程签名"),
                ("对应物", "C 的头文件 / Modula-2 的 .def"),
            ],
            "note": "这是现代「接口与实现分离」的早期形态。Simula 的编译器会生成符号信息，供客户模块检查。",
        },
        {
            "label": "对象布局",
            "file": "point.obj",
            "cmd": "（实现示意）",
            "code": r"""; 对象布局（示意）
Point:
   +0   class descriptor
   +1   x
   +2   y

; 虚过程表
VMT_Point:
   Move -> Point.Move

; 前缀继承：子类字段接在父类之后
ColoredPoint:
   +0   class descriptor
   +1   x
   +2   y
   +3   color""",
            "format": [
                ("对象", "连续的字块，首字指向类描述符"),
                ("虚表", "每个类一张，支持动态绑定"),
                ("继承", "父类字段在前，子类字段在后"),
                ("回收", "运行时垃圾回收"),
            ],
            "note": "把类描述符放在对象首字，是此后几乎所有面向对象运行时的做法。",
        },
        {
            "label": "装入与运行",
            "file": "a.out",
            "cmd": "$ simula point.sim && ./a.out",
            "code": r"""$ simula point.sim
$ ./a.out
(程序运行，无输出)
$ size a.out
   text    data     bss     dec     hex
   6144    1024     512    7680    1e00""",
            "format": [
                ("编译器", "SIMULA 67 编译器（各机器一套）"),
                ("运行时", "堆、垃圾回收、协程调度"),
                ("链接", "与运行时库一起装入"),
                ("产物", "机器码可执行文件"),
            ],
            "note": "协程（coroutine）需要运行时维护多个栈；这也是 Simula 的运行时比同期语言更重的原因。",
        },
    ],
    "tools": [
        {"era": "1960s", "editor": "卡片 / 纸带", "compiler": "SIMULA 67（UNIVAC 1107）", "build": "装入器", "pkg": "外部类库", "debug": "转储"},
        {"era": "1970s", "editor": "行编辑器", "compiler": "DEC-10 Simula", "build": "make", "pkg": "类库", "debug": "—"},
        {"era": "1990s", "editor": "Emacs", "compiler": "GNU Cim", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code", "compiler": "GNU Cim", "build": "make", "pkg": "—", "debug": "gdb"},
    ],
    "hello": {
        "file": "hello.sim",
        "code": r"""BEGIN
   OutText("Hello, world");
   OutImage
END""",
        "footprint": [
            {"stage": "源码", "size": "≈ 70 B", "w": 6},
            {"stage": "声明/符号", "size": "≈ 300 B", "w": 12},
            {"stage": "对象布局", "size": "≈ 64 B/对象", "w": 18},
            {"stage": "目标", "size": "≈ 4 KB", "w": 30},
            {"stage": "可执行", "size": "≈ 18 KB", "w": 46},
        ],
        "why": [
            "<strong>类</strong>：把数据与操作绑定为一个可复制的模板。",
            "<strong>前缀继承</strong>：子类对象直接复用父类字段布局。",
            "<strong>外部类</strong>：声明与实现分离，支持独立编译。",
            "<strong>运行时</strong>：堆、垃圾回收、协程都需要运行时支持。",
        ],
    },
},

# ============================================================
"pli": {
    "tagline": "IBM 想把科学计算、商业数据处理和系统编程放进同一门语言；它做到了，也把编译器推到了极限。",
    "intro": [
        "PL/I 是 IBM 在 1964 年为 System/360 推出的语言。它的野心是把 FORTRAN 的数值计算、COBOL 的数据处理、ALGOL 的块结构，以及系统编程需要的指针与异常处理，全部收进一门语言。",
        "它有许多在当时很激进的设计：没有保留字（关键字由上下文决定）、编译期设施（%INCLUDE、%MACRO）、ON 条件处理、基于变量的指针、多任务。代价是语法与编译器都极其复杂。",
        "PL/I 的产物链保留了大型机的典型层次：源码先经过编译期设施展开，再由编译器生成目标模块（ESD/RLD/TXT 记录），最后由链接编辑器装入。",
    ],
    "lineage": {
        "from": ["FORTRAN", "COBOL", "ALGOL 60"],
        "to": ["Ada 的异常处理", "C 的预处理宏", "现代语言的多范式"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.pli",
            "cmd": "$ cat hello.pli",
            "code": r"""HELLO: PROCEDURE OPTIONS(MAIN);
   DCL NAME CHAR(8) INIT('WORLD');
   PUT SKIP LIST('HELLO, ' || NAME);
END HELLO;""",
            "format": [
                ("过程", "PROCEDURE OPTIONS(MAIN)"),
                ("声明", "DCL 定义类型、长度、初值"),
                ("字符串", "CHAR(n)，定长"),
                ("关键字", "无保留字，按上下文解析"),
            ],
            "note": "PL/I 没有保留字：IF、ELSE 也可以是变量名。这让语法更灵活，也让编译器必须做更多的上下文分析。",
        },
        {
            "label": "编译期展开",
            "file": "hello.i",
            "cmd": "%INCLUDE / %MACRO（编译期设施）",
            "code": r"""%INCLUDE DCLDEFS;
%DECLARE WHO CHAR;

%WHO = 'WORLD';

HELLO: PROCEDURE OPTIONS(MAIN);
   DCL NAME CHAR(8) INIT(&WHO);
   PUT SKIP LIST('HELLO, ' || NAME);
END HELLO;

/* 展开后：DCL NAME CHAR(8) INIT('WORLD'); */""",
            "format": [
                ("%INCLUDE", "把外部声明文本并入"),
                ("%MACRO", "定义编译期宏"),
                ("%变量", "在编译期求值，替换进源码"),
                ("阶段", "发生在语法分析之前"),
            ],
            "note": "这是 C 预处理器的同代人，但能力更强：编译期变量可以参与计算，宏可以生成声明。",
        },
        {
            "label": "目标模块",
            "file": "HELLO.OBJ",
            "cmd": "OS/360 · 目标卡组",
            "code": r"""// 目标模块记录（示意）
ESD   HELLO    SD   000000  000004
ESD   PUT      ER   ...
RLD   ...
TXT   000000  47F0  ...
TXT   ...
END   HELLO

; ESD = External Symbol Dictionary
; RLD = Relocation Dictionary
; TXT = 文本（机器码）""",
            "format": [
                ("ESD", "外部符号与段定义"),
                ("RLD", "重定位信息"),
                ("TXT", "机器码文本记录"),
                ("END", "模块结束与入口"),
            ],
            "note": "这些记录是链接编辑器的输入。今天的 ELF 用 .symtab 与 .rela.text 表达同一类信息。",
        },
        {
            "label": "装入模块",
            "file": "HELLO",
            "cmd": "//LKED EXEC PGM=IEWL",
            "code": r"""//LKED   EXEC PGM=IEWL,PARM='LIST,XREF'
//SYSLIN   DD DSN=&&OBJ,DISP=(OLD,DELETE)
//SYSLMOD  DD DSN=USER.LOAD(HELLO),DISP=SHR

; 产物：load module
; 已解析所有外部符号，可直接 EXEC""",
            "format": [
                ("链接器", "IEWL（Linkage Editor）"),
                ("产物", "load module，PDS 成员"),
                ("符号", "全部解析完毕，无动态链接"),
                ("运行", "JCL 的 EXEC PGM=HELLO"),
            ],
            "note": "大型机的装入模块是自包含的：没有 DLL、没有 PLT，所有依赖在链接时已经固定。",
        },
    ],
    "tools": [
        {"era": "1960s", "editor": "卡片穿孔机", "compiler": "PL/I (F) 编译器", "build": "JCL", "pkg": "—", "debug": "转储"},
        {"era": "1970s", "editor": "TSO / ISPF", "compiler": "PL/I Optimizing Compiler", "build": "JCL", "pkg": "—", "debug": "Debug Tool"},
        {"era": "1990s", "editor": "ISPF", "compiler": "IBM VisualAge PL/I", "build": "JCL", "pkg": "—", "debug": "Debug Tool"},
        {"era": "2020s", "editor": "VS Code + PL/I 扩展", "compiler": "IBM Enterprise PL/I", "build": "JCL", "pkg": "—", "debug": "Debug Tool"},
    ],
    "hello": {
        "file": "HELLO.pli",
        "code": r"""HELLO: PROCEDURE OPTIONS(MAIN);
   PUT SKIP LIST('Hello, world');
END HELLO;""",
        "footprint": [
            {"stage": "源码", "size": "≈ 90 B", "w": 6},
            {"stage": "预处理", "size": "≈ 90 B", "w": 8},
            {"stage": "目标模块", "size": "≈ 1.8 KB", "w": 22},
            {"stage": "load module", "size": "≈ 6 KB", "w": 36},
            {"stage": "分区数据集", "size": "固定块", "w": 50},
        ],
        "why": [
            "<strong>多范式</strong>：一套语法同时服务科学与商业，声明与语句都很重。",
            "<strong>编译期设施</strong>：宏与包含在语法分析前展开，能力超过 C 预处理器。",
            "<strong>目标模块</strong>：用 ESD/RLD/TXT 记录描述符号与重定位。",
            "<strong>自包含装入</strong>：大型机没有动态链接，链接时就把一切固定下来。",
        ],
    },
},

# ============================================================
"apl": {
    "tagline": "一行符号可以做完一屏 Fortran；它的产物不是文件，而是一个可以整体保存的工作区。",
    "intro": [
        "APL 来自 Kenneth Iverson 1962 年的《A Programming Language》一书。他想要一种能直接书写数组运算的记法：没有循环，没有下标管理，`+/V` 就是求和。1966 年的 APL\\360 把这套记法变成可交互的系统。",
        "APL 的产物形态很特殊：程序通常不存成 .c 那样的源文件，而是存在于工作区（workspace）里。函数、变量、系统设置一起被保存，下次整体恢复。工作区是二进制格式，跨实现往往不兼容。",
        "它还需要一套超出 ASCII 的字符集。IBM 2741 终端与 EBCDIC APL 代码页是它的物理接口；今天我们用 Unicode 的 APL 符号，但输入仍然依赖特殊键盘布局。",
    ],
    "lineage": {
        "from": ["数学记法", "数组理论"],
        "to": ["J", "K", "MATLAB（数组思维）", "NumPy（广播）"],
    },
    "chain": [
        {
            "label": "会话与函数",
            "file": "workspace",
            "cmd": "      ∇R←MEAN V",
            "code": r"""∇R←MEAN V
 R←(+/V)÷⍴V
∇

      MEAN 1 2 3 4
2.5

      ⍳5
1 2 3 4 5

      +/⍳100
5050""",
            "format": [
                ("函数", "∇ 开始/结束，结果赋值给 R"),
                ("数组", "默认操作整个数组，无显式循环"),
                ("符号", "← 赋值，⍴ 取形状，⍳ 生成序列"),
                ("会话", "交互式，表达式立即求值"),
            ],
            "note": "APL 的「源码」往往就是一段会话记录或函数定义，而不是一个独立文件。工作区才是持久的单位。",
        },
        {
            "label": "字符编码",
            "file": "APL2741",
            "cmd": "（EBCDIC APL 代码页，示意）",
            "code": r"""APL 字符     名称            终端键位
⍳            iota            ...
⌈            ceiling         ...
⌊            floor           ...
←            arrow           ...
⍴            rho             ...
×            times           ...

; IBM 2741 使用 Selectric 打字球
; APL 字符通过 EBCDIC 代码页映射
; 不同代码页的字节值不同""",
            "format": [
                ("字符集", "超出 ASCII 的 APL 符号"),
                ("终端", "IBM 2741 Selectric"),
                ("编码", "EBCDIC APL 代码页"),
                ("互操作", "工作区跨实现通常不兼容"),
            ],
            "note": "APL 的符号不是可选装饰：没有它们，语言的核心表达力就消失了。这也是它长期绑定特定终端的原因。",
        },
        {
            "label": "内部表示",
            "file": "tokenized function",
            "cmd": "（实现示意）",
            "code": r"""; 函数 MEAN 的内部表示（示意）
header:  name=MEAN  rank=1  locals=R,V
body:
    PUSH_V   V
    REDUCE   +          ; +/
    PUSH_V   V
    SHAPE               ; ⍴
    DIVIDE
    RETURN""",
            "format": [
                ("解析", "APL 表达式按右结合解析"),
                ("执行", "解释器逐项执行，或编译为字节码"),
                ("数组", "运行时对象带形状与类型"),
                ("优化", "现代实现会做数组融合"),
            ],
            "note": "APL 没有语句分隔符，表达式靠符号的右结合规则解析。`+/V` 是一个整体：归约操作符 + 作用在向量 V 上。",
        },
        {
            "label": "工作区文件",
            "file": "mean.ws",
            "cmd": "$ ls -l mean.ws && )LOAD mean",
            "code": r"""$ ls -l mean.ws
-rw-r--r-- 1 user user 2.1K ... mean.ws

      )LOAD mean
SAVED  2026-10-27 10:00:00

      )VARS
V  A  R

      )FNS
MEAN""",
            "format": [
                ("工作区", "函数 + 变量 + 系统设置的整体"),
                ("格式", "二进制，实现相关"),
                ("加载", ")LOAD 恢复全部状态"),
                ("移植", "不保证跨版本/平台兼容"),
            ],
            "note": "把整个工作区当作产物，意味着「保存程序」和「保存运行状态」是同一件事。这一点和 Smalltalk 的镜像是同一种思路。",
        },
    ],
    "tools": [
        {"era": "1966", "editor": "IBM 2741 终端", "compiler": "APL\\360 解释器", "build": ")SAVE 工作区", "pkg": "工作区库", "debug": ")TRACE"},
        {"era": "1980s", "editor": "APL 专用终端", "compiler": "IBM APL2", "build": ")SAVE", "pkg": "工作区", "debug": ")TRACE"},
        {"era": "2000s", "editor": "Dyalog IDE", "compiler": "Dyalog APL", "build": "⎕SAVE", "pkg": "命名空间", "debug": "追踪"},
        {"era": "2020s", "editor": "Dyalog / VS Code", "compiler": "Dyalog APL", "build": "⎕SAVE / 脚本", "pkg": "Tatin", "debug": "追踪"},
    ],
    "hello": {
        "file": "HELLO.apl",
        "code": r"""⎕←'Hello, world'""",
        "footprint": [
            {"stage": "会话", "size": "1 行 · 18 B", "w": 5},
            {"stage": "字符编码", "size": "1 字节/字符", "w": 8},
            {"stage": "内部表示", "size": "≈ 200 B", "w": 14},
            {"stage": "工作区", "size": "≈ 2 KB", "w": 28},
            {"stage": "运行时", "size": "≈ 20 MB", "w": 90},
        ],
        "why": [
            "<strong>数组优先</strong>：操作符默认作用于整个数组，循环被吸收进原语。",
            "<strong>右结合解析</strong>：没有优先级表，表达式从右往左归约。",
            "<strong>工作区</strong>：保存程序就是保存运行状态，函数与数据不分离。",
            "<strong>字符集</strong>：符号是语言的一部分，编码与终端因此成为产物链的一环。",
        ],
    },
},

# ============================================================
"snobol": {
    "tagline": "在正则表达式成为库函数之前，SNOBOL 已经让「模式」成为一等公民。",
    "intro": [
        "SNOBOL 由 David Farber、Ralph Griswold 与 Ivan Polonsky 在贝尔实验室设计，1962 年首次实现，1964 年的 SNOBOL3 开始流行。它的目标不是数值计算，而是字符串：解析、转换、匹配。",
        "SNOBOL 最重要的设计是「模式即数据」：模式可以拼接、赋值、作为参数传递、在运行时构造。匹配失败不是异常，而是一个可处理的信号。这直接影响了后来的 Icon 与正则表达式库。",
        "它的实现也很有代表性：SNOBOL4 用 SIL（SNOBOL Implementation Language）写成，编译器把源码降成 SIL，再交给汇编器。产物链因此多了一层「实现语言」。",
    ],
    "lineage": {
        "from": ["COMIT", "字符串处理需求"],
        "to": ["Icon", "Regex 库", "AWK 的模式-动作"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.sno",
            "cmd": "$ cat hello.sno",
            "code": r"""        &ANCHOR = 1
        TEXT = 'HELLO, WORLD'
        TEXT SPAN('A-Z') . WORD ',' ARB . REST
        OUTPUT = WORD
END""",
            "format": [
                ("语句", "模式匹配 + 赋值，靠成功/失败驱动"),
                ("模式", "SPAN / ARB / BREAK / LEN 等原语"),
                ("绑定", ". 变量 把匹配到的子串保存下来"),
                ("锚点", "&ANCHOR 控制是否从开头匹配"),
            ],
            "note": "这一行不是「查找子串」，而是「让 TEXT 去匹配一个模式」：先取连续大写字母存进 WORD，再匹配逗号，剩下的存进 REST。",
        },
        {
            "label": "模式编译",
            "file": "pattern automaton",
            "cmd": "（回溯程序，结构示意）",
            "code": r"""; SPAN('A-Z') . WORD ',' ARB . REST 编译为回溯程序
MATCH:
    SPAN    'A-Z'          ; 贪婪匹配连续大写
    ASSIGN  WORD
    LIT     ','
    ARB                    ; 任意长度，保存回溯点
    ASSIGN  REST
    SUCCEED
FAIL:
    RESTORE                ; 回到最近的回溯点
    ...""",
            "format": [
                ("编译", "模式被编译成匹配指令序列"),
                ("回溯", "失败时回到保存点，尝试更短/更长"),
                ("绑定", "ASSIGN 把子串写入变量"),
                ("运行时", "解释执行匹配指令"),
            ],
            "note": "SNOBOL 的模式不是正则的语法糖：它可以包含任意代码、可以递归、可以在运行时拼接。",
        },
        {
            "label": "SIL 与汇编",
            "file": "hello.sil",
            "cmd": "（SNOBOL Implementation Language）",
            "code": r"""; SIL 片段（结构示意）
        ...
        ; SNOBOL4 的编译器本身用 SIL 写成
        ; SIL 是一种类汇编的宏语言
        ; 先由 SIL 编译器生成汇编，再交给系统汇编器""",
            "format": [
                ("SIL", "SNOBOL Implementation Language"),
                ("层次", "SNOBOL → SIL → 汇编"),
                ("自举", "SNOBOL4 编译器用 SIL 实现"),
                ("移植", "换机器主要重写 SIL 后端"),
            ],
            "note": "用一门实现语言写编译器，是 1960 年代的常见做法。SIL 让 SNOBOL4 能在多种机器上落地。",
        },
        {
            "label": "目标与可执行",
            "file": "hello.o → hello",
            "cmd": "$ snobol4 hello.sno",
            "code": r"""$ snobol4 hello.sno
HELLO

$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

; 运行时包含：
;   模式匹配引擎
;   动态字符串
;   回溯栈""",
            "format": [
                ("目标", "ELF64 · ET_REL"),
                ("运行时", "模式引擎 + 动态字符串"),
                ("执行", "解释器或编译后程序"),
                ("输出", "OUTPUT 变量绑定到标准输出"),
            ],
            "note": "模式引擎是 SNOBOL 运行时最重的部分；用户程序只是向它提交模式与输入。",
        },
    ],
    "tools": [
        {"era": "1960s", "editor": "卡片 / 电传打字机", "compiler": "SNOBOL3 解释器", "build": "—", "pkg": "—", "debug": "TRACE"},
        {"era": "1970s", "editor": "行编辑器", "compiler": "SNOBOL4", "build": "make", "pkg": "—", "debug": "TRACE"},
        {"era": "1990s", "editor": "Emacs", "compiler": "SNOBOL4 (C 实现)", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code", "compiler": "SNOBOL4 / CSNOBOL4", "build": "make", "pkg": "—", "debug": "gdb"},
    ],
    "hello": {
        "file": "hello.sno",
        "code": r"""        OUTPUT = 'Hello, world'
END""",
        "footprint": [
            {"stage": "源码", "size": "≈ 40 B", "w": 5},
            {"stage": "模式程序", "size": "≈ 120 B", "w": 10},
            {"stage": "SIL/汇编", "size": "≈ 1.4 KB", "w": 20},
            {"stage": "目标", "size": "≈ 3 KB", "w": 30},
            {"stage": "可执行", "size": "≈ 22 KB", "w": 48},
        ],
        "why": [
            "<strong>模式即数据</strong>：模式可以拼接、赋值、传递，语言因此能描述「结构」而不只是「值」。",
            "<strong>成功/失败驱动</strong>：匹配失败不是异常，而是控制流的一部分。",
            "<strong>SIL</strong>：用实现语言写编译器，把前端与后端分开。",
            "<strong>回溯引擎</strong>：运行时保存匹配状态，失败时恢复。",
        ],
    },
},

# ============================================================
"b": {
    "tagline": "1969 年，Thompson 在 PDP-7 上写出的 B 是 C 的直接前身；它只有一种数据类型，却足够重写 UNIX。",
    "intro": [
        "B 由 Ken Thompson 在贝尔实验室设计，源自 BCPL，1969 年跑在 PDP-7 上。它只有一种数据类型——机器字；字符串是字数组，指针与整数不分。就是这门语言，让 Thompson 得以重写 UNIX。",
        "B 的编译器也是用 B 写的，这带来一个经典的自举问题：第一版编译器必须先由汇编或另一门语言生成。B 的语法直接孕育了 C：`auto`、`extrn`、`++`、`--`、`[]`、`->` 都能在 B 里找到前身。",
        "它的可执行格式是第一代 UNIX 的 a.out：一个极简的头部，后面紧跟正文与数据。理解 B 的产物链，就理解了 C 的 a.out 与今天 ELF 的祖先。",
    ],
    "lineage": {
        "from": ["BCPL", "PDP-7 汇编"],
        "to": ["C", "C++", "Go（语法亲缘）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.b",
            "cmd": "$ cat hello.b",
            "code": r"""main() {
    extrn putchar;
    auto i;
    i = 0;
    while (i < 13) {
        putchar("hello, world*n"[i]);
        i++;
    }
}""",
            "format": [
                ("类型", "只有 word，没有 char/int 区分"),
                ("字符串", "字数组，*n 表示换行"),
                ("声明", "auto 局部，extrn 外部"),
                ("语法", "C 的直接前身"),
            ],
            "note": "B 里没有类型系统：字符串、整数、指针都是字。`*n` 是转义，也是 B 与 C 在源码层面最明显的差别之一。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "（PDP-7，示意）",
            "code": r"""main:
    law     0           ; 取常数 0
    dac     i           ; i = 0
loop:
    lac     i
    tad     m12
    jms     putchar
    isz     i
    jmp     loop
    jmp     ...

i:  0
m12: -12""",
            "format": [
                ("机器", "PDP-7，18 位字"),
                ("语法", "PAL 汇编，符号地址"),
                ("调用", "JMS 跳转子程序"),
                ("数据", "字数组，无字节寻址"),
            ],
            "note": "PDP-7 没有字节寻址，字符串按字存放。这解释了 B 的字符串为什么是「字数组」而不是「字节数组」。",
        },
        {
            "label": "a.out",
            "file": "a.out",
            "cmd": "$ od -An -o -N 16 a.out",
            "code": r"""$ od -An -o -N 16 a.out
 000407 000020 000004 000000 000000 000000
 ; word 0  magic         (实现相关)
 ; word 1  text size
 ; word 2  data size
 ; word 3  bss size
 ; word 4  symbol size
 ; word 5  entry point
 ; word 6  unused
 ; word 7  unused""",
            "format": [
                ("格式", "PDP-7 a.out，8 字头"),
                ("魔数", "标识可执行格式，随版本变化"),
                ("段", "text / data / bss"),
                ("装入", "头部之后直接映射正文"),
            ],
            "note": "第一代 a.out 头部只有 8 个字。今天的 ELF 仍保留 e_type、e_entry、段表这类字段，只是表达得更通用。",
        },
        {
            "label": "自举",
            "file": "b compiler",
            "cmd": "（B 编译器用 B 写）",
            "code": r"""/* 自举链（示意）
 *   1. 用汇编写一个最小 B 编译器
 *   2. 用它编译 B 写成的完整编译器
 *   3. 用新编译器重新编译自己
 *   4. 从此只需要 B 编译器
 */""",
            "format": [
                ("自举", "编译器用自身语言实现"),
                ("种子", "第一版必须借助汇编/其他语言"),
                ("验证", "自编译结果与原编译器一致"),
                ("传承", "C 继承了这套自举传统"),
            ],
            "note": "「用 B 写 B 编译器」不是炫技：它让编译器可以跟着语言一起演化，也让移植只剩后端工作。",
        },
    ],
    "tools": [
        {"era": "1969", "editor": "PDP-7 电传打字机", "compiler": "B 编译器", "build": "汇编 + 装入", "pkg": "—", "debug": "核心转储"},
        {"era": "1970s", "editor": "ed", "compiler": "B 编译器", "build": "make（早期）", "pkg": "—", "debug": "adb"},
        {"era": "2020s", "editor": "—", "compiler": "无活跃实现", "build": "—", "pkg": "—", "debug": "—"},
    ],
    "hello": {
        "file": "hello.b",
        "code": r"""main() {
    extrn putchar;
    auto i;
    i = 0;
    while (i < 13) {
        putchar("hello, world*n"[i]);
        i++;
    }
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 110 B", "w": 7},
            {"stage": "汇编", "size": "≈ 0.6 KB", "w": 15},
            {"stage": "a.out", "size": "≈ 1.4 KB", "w": 25},
            {"stage": "内存映像", "size": "≈ 1.4 KB", "w": 25},
        ],
        "why": [
            "<strong>单一类型</strong>：所有值都是字，编译器不需要类型布局。",
            "<strong>自举</strong>：编译器用 B 写，语言可以自我演化。",
            "<strong>a.out</strong>：极简头部 + 连续段，装入器几乎只是 mmap。",
            "<strong>字寻址</strong>：字符串按字存放，直接影响了 C 的早期实现。",
        ],
    },
},

}
