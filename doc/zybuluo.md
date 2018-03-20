# 设置初始文本

```javascript
com.zybuluo.mdeditor.unifiedEditor.setValue("# aa")
```

# 获取markdown格式文本

```javascript
com.zybuluo.mdeditor.unifiedEditor.getValue("# aa")
```

# 获取转换后的文本

```javascript
$("#wmd-preview").html()
```

# 获取目录
```javascript
$("toc-list").html()
```

# 模拟提交

```javascript
markdown=com.zybuluo.mdeditor.unifiedEditor.getValue("# aa")
content=$("#wmd-preview").html()
nav=$("#toc-list").html()
$.post('/blog/edit',{'name':"test",markdown: markdown, content: content,nav:nav})

```

# 模拟读取
