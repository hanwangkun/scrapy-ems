# -*- coding: utf-8 -*-
import scrapy;
import ems.items;

class EmsdotSpider(scrapy.Spider):
    name = 'emsdot'
    allowed_domains = ['www.psbc.com']
    province_url = 'http://www.psbc.com/cms/WdjgQuery.do';

    city_url = 'http://www.psbc.com/cms/CityQuery.do';
    city_param={'Param':'-1'};

    dict_url = 'http://www.psbc.com/cms/XianQuery.do';
    dict_param = {'Param':'-1'};

    dot_url = 'http://www.psbc.com/cms/WangdianQuery.do';
    ##非第一次查询参数
    dot_param = {'Param': '-1',
                 'recordNumber':'-1',
                 'currentIndex':'-1'};
    ## 按每个区县编码查询网点信息时第一次查询参数
    dot_first_param = {'Param': '-1'};



    def start_requests(self):
        rqs = scrapy.Request(self.province_url,method='POST',callback=self.parse_province);
        yield rqs;

    ## 解析省份信息
    def parse_province(self, response):
        provinceList = response.xpath('//option');
        for p in provinceList:
            name = p.xpath('text()').extract_first();
            code = p.xpath('@value').extract_first();
            meta = {'pname':name,'pcode':code};
            param = {};
            param['Param']=code;
            yield scrapy.FormRequest(self.city_url,callback=self.parse_city,formdata=param,meta=meta);

    ## 解析城市信息
    def parse_city(self,response):
        pmeta = response.meta;
        ces = response.xpath('//a');
        for c in ces:
            name = c.xpath('text()').extract_first();
            code = c.xpath('@onclick').extract_first()[11:15];
            meta = {'cname':name,'ccode':code};
            meta.update(pmeta);
            param = {};
            param['Param'] = code;
            yield scrapy.FormRequest(self.dict_url,callback=self.parse_dict,formdata=param,meta=meta);

    ## 解析区县信息
    def parse_dict(self,response):
        cmeta = response.meta;
        des = response.xpath('//a');
        for d in des:
            name = d.xpath('text()').extract_first();
            code = d.xpath('@onclick').extract_first()[15:21];
            meta = {'dname':name,'dcode':code};
            meta.update(cmeta);
            param = {};
            param['Param']=code;
            yield scrapy.FormRequest(self.dot_url,callback=self.parse_dot,formdata=param,meta=meta);


    ## 解析第一次查询网点信息
    def parse_dot(self,response):
        dmeta = response.meta;
        dotes = response.xpath('//tr');
        recordNumber = int(response.xpath('//input[@name="recordNumber"]/@value').extract_first());
        pages = int(recordNumber/10)+1;
        ## 先解析第一次查到的信息
        for es in dotes:
            des = es.xpath('td');
            if len(des) != 4:
                continue;
            else:
                es_name = des[0].xpath('text()').extract_first();
                es_addr = des[1].xpath('text()').extract_first();
                es_time = des[2].xpath('text()').extract_first();
                es_tel = des[3].xpath('text()').extract_first();
                dot = ems.items.EmsItem();
                dot['name'] = es_name;
                dot['addr'] = es_addr;
                dot['timestr'] = es_time;
                dot['tel'] = es_tel;
                dot['province']=dmeta['pcode'];
                dot['provinceName']=dmeta['pname'];
                dot['city']=dmeta['ccode'];
                dot['cityName']=dmeta['cname'];
                dot['dict']=dmeta['dcode'];
                dot['dictName']=dmeta['dname'];
                yield dot;

        ## 进行下一次请求
        i = 1;
        while i < pages:
            currentIndex = i*10;
            param = {'Param':dmeta['dcode'],'currentIndex':str(currentIndex),'recordNumber':str(recordNumber)};
            i = i+1;
            yield scrapy.FormRequest(self.dot_url,callback=self.parse_dot_other,formdata=param,meta=dmeta);



    ## 解析非第一次查询网点信息
    def parse_dot_other(self, response):
        dotes = response.xpath('//tr');
        dmeta = response.meta;
        ## 解析查到的信息
        for es in dotes:
            des = es.xpath('td');
            if len(des) != 4:
                continue;
            else:
                es_name = des[0].xpath('text()').extract_first();
                es_addr = des[1].xpath('text()').extract_first();
                es_time = des[2].xpath('text()').extract_first();
                es_tel = des[3].xpath('text()').extract_first();
                dot = ems.items.EmsItem();
                dot['name'] = es_name;
                dot['addr'] = es_addr;
                dot['timestr'] = es_time;
                dot['tel'] = es_tel;
                dot['province']=dmeta['pcode'];
                dot['provinceName']=dmeta['pname'];
                dot['city']=dmeta['ccode'];
                dot['cityName']=dmeta['cname'];
                dot['dict']=dmeta['dcode'];
                dot['dictName']=dmeta['dname'];
                yield dot;