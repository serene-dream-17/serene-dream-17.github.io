# -*- coding: utf-8 -*-
"""框架卡补充信息：学习曲线 / 生态成熟度 / 许可证。"""

META = {
    ("c", "GTK"): {"learn": "中", "eco": "成熟", "license": "LGPL"},
    ("c", "SDL2"): {"learn": "低", "eco": "成熟", "license": "zlib"},
    ("c", "FreeRTOS"): {"learn": "中", "eco": "成熟", "license": "MIT"},

    ("cpp", "Qt"): {"learn": "中", "eco": "成熟", "license": "LGPL / 商业"},
    ("cpp", "Unreal Engine"): {"learn": "高", "eco": "成熟", "license": "商业"},
    ("cpp", "Boost"): {"learn": "中", "eco": "成熟", "license": "Boost"},
    ("cpp", "POCO"): {"learn": "低", "eco": "成熟", "license": "Boost"},

    ("rust", "Axum"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("rust", "Actix Web"): {"learn": "中", "eco": "成熟", "license": "MIT / Apache-2.0"},
    ("rust", "Tauri"): {"learn": "中", "eco": "成长", "license": "MIT / Apache-2.0"},
    ("rust", "Bevy"): {"learn": "中", "eco": "早期", "license": "MIT / Apache-2.0"},

    ("go", "Gin"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("go", "Echo"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("go", "gRPC-Go"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("go", "controller-runtime"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},

    ("java", "Spring Boot"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("java", "Quarkus"): {"learn": "中", "eco": "成长", "license": "Apache-2.0"},
    ("java", "Jakarta EE"): {"learn": "高", "eco": "成熟", "license": "EPL / 各实现"},
    ("java", "Android SDK"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},

    ("kotlin", "Jetpack Compose"): {"learn": "中", "eco": "成长", "license": "Apache-2.0"},
    ("kotlin", "Ktor"): {"learn": "低", "eco": "成长", "license": "Apache-2.0"},
    ("kotlin", "Spring Boot"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},

    ("scala", "Akka"): {"learn": "高", "eco": "成熟", "license": "BUSL / 商业"},
    ("scala", "Play"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("scala", "Apache Spark"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},

    ("csharp", "ASP.NET Core"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("csharp", "Unity"): {"learn": "中", "eco": "成熟", "license": "商业"},
    ("csharp", "WPF"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("csharp", "Blazor"): {"learn": "中", "eco": "成长", "license": "MIT"},

    ("fsharp", "Giraffe"): {"learn": "中", "eco": "成长", "license": "Apache-2.0"},
    ("fsharp", "Saturn"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("fsharp", "Bolero"): {"learn": "中", "eco": "早期", "license": "Apache-2.0"},

    ("clojure", "Ring + Compojure"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("clojure", "Re-frame"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("clojure", "Datomic"): {"learn": "高", "eco": "成熟", "license": "商业"},

    ("javascript", "React"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("javascript", "Vue"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("javascript", "Express"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("javascript", "Next.js"): {"learn": "中", "eco": "成熟", "license": "MIT"},

    ("typescript", "Angular"): {"learn": "高", "eco": "成熟", "license": "MIT"},
    ("typescript", "NestJS"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("typescript", "Next.js"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("typescript", "tRPC"): {"learn": "中", "eco": "成长", "license": "MIT"},

    ("python", "Django"): {"learn": "中", "eco": "成熟", "license": "BSD"},
    ("python", "FastAPI"): {"learn": "低", "eco": "成长", "license": "MIT"},
    ("python", "Flask"): {"learn": "低", "eco": "成熟", "license": "BSD"},
    ("python", "PyTorch"): {"learn": "中", "eco": "成熟", "license": "BSD"},

    ("php", "Laravel"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("php", "Symfony"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("php", "WordPress"): {"learn": "低", "eco": "成熟", "license": "GPL"},

    ("ruby", "Rails"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("ruby", "Sinatra"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("ruby", "Hanami"): {"learn": "中", "eco": "成长", "license": "MIT"},

    ("perl", "Mojolicious"): {"learn": "中", "eco": "成熟", "license": "Artistic-2.0"},
    ("perl", "Catalyst"): {"learn": "中", "eco": "成熟", "license": "Perl_5"},
    ("perl", "Dancer"): {"learn": "低", "eco": "成熟", "license": "Perl_5"},

    ("elixir", "Phoenix"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("elixir", "LiveView"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("elixir", "Ecto"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},

    ("erlang", "OTP"): {"learn": "高", "eco": "成熟", "license": "Apache-2.0"},
    ("erlang", "Cowboy"): {"learn": "中", "eco": "成熟", "license": "ISC"},

    ("swift", "SwiftUI"): {"learn": "中", "eco": "成熟", "license": "Apple SDK"},
    ("swift", "UIKit"): {"learn": "中", "eco": "成熟", "license": "Apple SDK"},
    ("swift", "Vapor"): {"learn": "中", "eco": "成长", "license": "MIT"},

    ("dart", "Flutter"): {"learn": "中", "eco": "成熟", "license": "BSD"},
    ("dart", "shelf"): {"learn": "低", "eco": "成长", "license": "BSD"},

    ("objectivec", "Cocoa / Cocoa Touch"): {"learn": "中", "eco": "成熟", "license": "Apple SDK"},
    ("objectivec", "AFNetworking"): {"learn": "低", "eco": "维护", "license": "MIT"},

    ("vb", "WinForms"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("vb", "WPF（VB.NET）"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("vb", "VBA"): {"learn": "低", "eco": "成熟", "license": "商业"},

    ("delphi", "VCL"): {"learn": "中", "eco": "成熟", "license": "商业"},
    ("delphi", "FireMonkey"): {"learn": "中", "eco": "成熟", "license": "商业"},
    ("delphi", "Lazarus LCL"): {"learn": "中", "eco": "成熟", "license": "LGPL"},

    ("r", "Shiny"): {"learn": "低", "eco": "成熟", "license": "GPL / 商业"},
    ("r", "tidyverse"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("r", "RMarkdown"): {"learn": "低", "eco": "成熟", "license": "GPL"},

    ("matlab", "Simulink"): {"learn": "高", "eco": "成熟", "license": "商业"},
    ("matlab", "App Designer"): {"learn": "中", "eco": "成熟", "license": "商业"},
    ("matlab", "MATLAB Compiler"): {"learn": "中", "eco": "成熟", "license": "商业"},

    ("julia", "Genie"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("julia", "Flux"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("julia", "DifferentialEquations.jl"): {"learn": "中", "eco": "成熟", "license": "MIT"},

    ("sql", "dbt"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("sql", "Prisma"): {"learn": "低", "eco": "成长", "license": "Apache-2.0"},
    ("sql", "SQLAlchemy"): {"learn": "中", "eco": "成熟", "license": "MIT"},

    ("lua", "LÖVE"): {"learn": "低", "eco": "成熟", "license": "zlib"},
    ("lua", "OpenResty"): {"learn": "中", "eco": "成熟", "license": "BSD"},
    ("lua", "Roblox"): {"learn": "低", "eco": "成熟", "license": "商业"},

    ("solidity", "OpenZeppelin"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("solidity", "Hardhat"): {"learn": "中", "eco": "成熟", "license": "MIT"},
    ("solidity", "Foundry"): {"learn": "中", "eco": "成长", "license": "MIT / Apache-2.0"},

    ("shell", "bats"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("shell", "Ansible"): {"learn": "中", "eco": "成熟", "license": "GPL / 商业"},

    ("html", "Bootstrap"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("html", "Tailwind CSS"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("html", "Web Components"): {"learn": "中", "eco": "标准", "license": "W3C"},

    ("css", "Tailwind CSS"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("css", "Bootstrap"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("css", "Bulma"): {"learn": "低", "eco": "成熟", "license": "MIT"},

    ("markdown", "CommonMark"): {"learn": "低", "eco": "标准", "license": "BSD"},
    ("markdown", "MDX"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("markdown", "Pandoc"): {"learn": "中", "eco": "成熟", "license": "GPL"},

    ("svg", "D3"): {"learn": "中", "eco": "成熟", "license": "ISC"},
    ("svg", "Snap.svg"): {"learn": "低", "eco": "维护", "license": "Apache-2.0"},
    ("svg", "SVGO"): {"learn": "低", "eco": "成熟", "license": "MIT"},

    ("xml", "XSLT / XPath"): {"learn": "中", "eco": "标准", "license": "W3C"},
    ("xml", "XSD"): {"learn": "中", "eco": "标准", "license": "W3C"},
    ("xml", "DOM / SAX"): {"learn": "中", "eco": "标准", "license": "W3C"},

    ("sass", "Dart Sass"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("sass", "PostCSS"): {"learn": "低", "eco": "成熟", "license": "MIT"},
    ("sass", "Compass"): {"learn": "中", "eco": "停止维护", "license": "MIT"},

    ("less", "Less.js"): {"learn": "低", "eco": "维护", "license": "Apache-2.0"},
    ("less", "PostCSS"): {"learn": "低", "eco": "成熟", "license": "MIT"},

    ("yaml", "Kubernetes"): {"learn": "高", "eco": "成熟", "license": "Apache-2.0"},
    ("yaml", "GitHub Actions"): {"learn": "中", "eco": "成熟", "license": "商业"},
    ("yaml", "Docker Compose"): {"learn": "低", "eco": "成熟", "license": "Apache-2.0"},

    ("fortran", "LAPACK / BLAS"): {"learn": "中", "eco": "成熟", "license": "BSD"},
    ("fortran", "MPI"): {"learn": "中", "eco": "成熟", "license": "各实现"},
    ("fortran", "NetCDF"): {"learn": "低", "eco": "成熟", "license": "BSD"},

    ("cobol", "CICS"): {"learn": "高", "eco": "成熟", "license": "商业"},
    ("cobol", "IMS"): {"learn": "高", "eco": "成熟", "license": "商业"},
    ("cobol", "GnuCOBOL"): {"learn": "中", "eco": "成长", "license": "GPL"},
    ("groovy", "Grails"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("groovy", "Spock"): {"learn": "低", "eco": "成熟", "license": "Apache-2.0"},
    ("groovy", "Gradle"): {"learn": "中", "eco": "成熟", "license": "Apache-2.0"},
    ("d", "vibe.d"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("d", "DUB"): {"learn": "低", "eco": "成长", "license": "MIT"},
    ("nim", "Jester"): {"learn": "低", "eco": "成长", "license": "MIT"},
    ("nim", "Karax"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("nim", "Nimble"): {"learn": "低", "eco": "成长", "license": "BSD"},
    ("crystal", "Lucky"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("crystal", "Kemal"): {"learn": "低", "eco": "成长", "license": "MIT"},
    ("haskell", "Yesod"): {"learn": "高", "eco": "成熟", "license": "MIT"},
    ("haskell", "Servant"): {"learn": "高", "eco": "成长", "license": "BSD-3-Clause"},
    ("haskell", "Scotty"): {"learn": "低", "eco": "成熟", "license": "BSD-3-Clause"},
    ("ocaml", "Dream"): {"learn": "中", "eco": "成长", "license": "MIT"},
    ("ocaml", "MirageOS"): {"learn": "高", "eco": "成长", "license": "ISC"},
    ("commonlisp", "Hunchentoot"): {"learn": "中", "eco": "成熟", "license": "BSD"},
    ("commonlisp", "Caveman2"): {"learn": "中", "eco": "成长", "license": "LLGPL"},
    ("smalltalk", "Seaside"): {"learn": "高", "eco": "成熟", "license": "MIT"},
    ("smalltalk", "Glamorous Toolkit"): {"learn": "中", "eco": "成长", "license": "MIT"},
}
