####使用 `tornado` 和 `highcharts` 简单实现 web 查看**

####启动 web 服务
	$ python webapp.py

####推荐使用 Chrome 浏览器
	http://your-host:8000

####按天查看
	# 查看 2015-01-17 至 2015-01-18 的数据
	http://your-host:8000?gt=2015-01-17&lt=2015-01-18

	# 查看 2015-01-17 之后的数据
	http://your-host:8000?gt=2015-01-17
