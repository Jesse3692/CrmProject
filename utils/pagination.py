#!/usr/bin/python3
# coding: utf-8
# @File: pagination.py
# @Author:lcfzh
# @Time: 2019年03月14日 01:45
# 说明:

class Pagination:
    def __init__(self, page_num, all_count, per_num=10, max_show=11):
        # 总页数
        self.page_count, more = divmod(all_count, per_num)
        if more:
            self.page_count += 1
            
        # 从网页获取的页码（加判断）
        try:
            # 如果没有页数值传过来
            self.page_num = int(page_num)
            if self.page_num <= 0:
                self.page_num = 1
            elif self.page_num >= self.page_count:
                self.page_num = self.page_count
        except ValueError as e:
            self.page_num = 1
        print(">>>", self.page_num)
        
        # 每页显示的数量
        self.per_num = 10
    
        # 总数据量
        all_count = all_count
        
        # 最大显示页数（显示多少个分页按钮）
        self.max_show = 11
        self.half_show = max_show // 2
        
    @property
    def page_html(self):
        #          对页码显示的逻辑判断
        if self.page_count < self.max_show:  # 总页码数 < 最大显示页码数
            page_start = 1  # 起始页数
            page_end = self.page_count  # 结束页数
        else:  # 总页码数 > 最大显示页码数    -- 一般情况下
            if self.page_num <= self.half_show:  # 请求的页码小于中间值时（左边极值）
                page_start = 1
                page_end = self.max_show
            elif self.page_num + self.half_show >= self.page_count:  # 请求的页码加上中间值大于总页数时 （右边极值）
                page_start = self.page_count - self.max_show + 1
                page_end = self.page_count
            else:
                page_start = self.page_num - self.half_show
                page_end = self.page_num + self.half_show
        
        # 在后端直接处理前端的HTML代码，然后发送过去
    
        # 添加上一页
        page_list = []
        if self.page_num == 1:  # 如果是第一页则上一页没法使用
            page_list.append('<li class="disabled"><a>上一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">上一页</a></li>'.format(self.page_num - 1, ))
    
        # 添加分页按钮
        for i in range(page_start, page_end + 1):
            if i == self.page_num:  # 当前标签高亮
                page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
    
        # 添加下一页按钮
        if self.page_num == self.page_count:  # 如果是最后一页则下一页没法使用
            page_list.append('<li class="disabled"><a>下一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">下一页</a></li>'.format(self.page_num + 1, ))
    
        # 对列表中的标签拼接成字符串
        return ''.join(page_list)
    
    @property
    def start(self):
        """
        切片的起始值
        :return:
        """
        return (self.page_num - 1)*self.per_num
    
    @property
    def end(self):
        """
        切片的结束值
        :return:
        """
        return self.page_num*self.per_num