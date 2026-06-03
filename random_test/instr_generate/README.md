随机测试脚本使用说明
 
```
使用方法

python3 main.py 'instr' 'number'
 
把"instr"换成需要测试的指令，目前支持的指令见后文
还可以使用以下特殊字符
"random1"：随机测试slot1的全部指令
"random2"：随机测试slot2的全部指令
"random3"：随机测试slot3的全部指令
"random"：随机测试全部指令,并且进行指令字打包
  
"number"：测试次数，代表进行多少次测试，
          但是很多指令需要有依赖，所以不代表生成的指令数

生成的汇编在./generate文件夹底下，命名为'instr'.s(取决于测试输入的instr名字)
```
 
```

MOV指令
"movigh": 
"movigl": 
"moviglz":
"moviglx":
"movg2c": 
"movg2g": 
"movc2g": 
```

```

LOAD指令
"load8": 
"load16":
"load32":
"loadu8":
"loadu16":
"loadu32":
 
"loado16":
"loado32":

"loadi8":
"loadi16":
"loadi32":

"loadui8":
"loadui16":
"loadui32":
```

```
STORE指令
"store8":
"store16":
"store32":

"storeu8":
"storeu16":
"storeu32":

"storeo16":
"storeo32":

"storei8":
"storei16":
"storei32":

"storeui8":
"storeui16":
"storeui32":
 ```
