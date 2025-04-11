一种灵活的数据文本格式：

```
# --kevin_notation--
格式说明，可选。如果有，则模式会自动调用对应格式的读取函数进行解读
# --metadata--
# sep
,
# comment_flag
//
# title
this is the title
# column_name// 不指定描述信息时，默认使用全局的 
epoch,loss,model_name
# column_type (sep=" ")
int float str
# column_num// 不指定时，根据 column_name 和 column_type 的数量进行推断
3
# --contents--
0,2.31,m0.pkt
1,2.22,m1.pkt
// 使用`//` 表示注释
...
```

注意在 # comment_flag 之前，不能使用注释
