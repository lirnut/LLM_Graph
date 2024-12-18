# LLM提示词创造性生图

## 环境配置
* python >= 3.12
* 环境变量中配置`OPENAI_API_KEY`与`OPENAI_BASE_URL`
```bash
pip install -r requirements.txt
```

## json文件
```
[    
    {
        "PromptMind":"如果在绘制室内建筑，可以这么思考，先思考灯光是什么色调的，再思考墙壁是什么颜色的，····",
        "PromptTemplate":{
            "input_variables":["灯光颜色", "墙壁颜色", "···"],
            "template":"灯光是{灯光颜色}，墙壁的是{墙壁颜色}，···"
        },
        "Example":[
            ["昏暗","惨白","..."],
            ["橘黄","木板做的","..."],
            ...
        ]
    },
    ......
]
```

## 运行任务
任务运行
```bash
python Prompt.py --...(参数可选)
```
参数帮助
```bash
python Prompt.py --help
```