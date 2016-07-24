import json

from flask import Flask
from flask import render_template

from sql_util import SqlUtil

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('show_charts.html')


@app.route('/get_pie', methods=['post', 'get'])
def get_pie():
    sql = '''SELECT count(*)  AS 'event_count',
            (CASE WHEN  LENGTH(trim(t.city)) < 1
            THEN '其他' ELSE t.city END) AS 'event_city'
            FROM segmentfault_events t
            GROUP BY t.city
            ORDER BY count(*) DESC
                '''
    data = SqlUtil.query_all(sql)
    result = {
        'title': {'text': '线下活动城市分布',
                  'subtext': '数据来自SegmentFault',
                  'sublink': 'https://segmentfault.com/events'},

        'legend': {'data': [x['event_city'] for x in data]},
        'series': {'name': '城市:数量',
                   'data':
                       [{'value': x['event_count'], 'name': x['event_city']} for x in data]
                   }
    }
    return json.dumps(result)


@app.route('/get_count_per_year', methods=['get', 'post'])
def get_count_per_year():
    sql = '''
        SELECT
        substr(t.c_date, 1, 4)AS 'year',
        count(*)AS 'count'
        FROM
        segmentfault_events t
        GROUP BY
        substr(t.c_date, 1, 4)
    '''
    data = SqlUtil.query_all(sql)
    result = {
        'title': {'text': '线下活动年度数量分布',
                  'subtext': '数据来自SegmentFault',
                  'sublink': 'https://segmentfault.com/events'},

        'legend': {'data': ['数量']},
        'xAxis': {
            'data': [x['year'] for x in data]
        },
        'yAxis': {},
        'series': {'name': '数量',
                   'data':
                       [x['count'] for x in data]
                   }
    }
    return json.dumps(result)


@app.route('/get_count_per_day')
def get_count_per_day():
    sql = '''
        SELECT
        count(*) AS 'count',
            t.`week` AS 'week'
        FROM
            segmentfault_events t
        GROUP BY
        t.`week`
        ORDER BY
        t.`week_number`
    '''
    data = SqlUtil.query_all(sql)
    result = {
        'title': {'text': '线下活动星期数量分布',
                  'subtext': '数据来自SegmentFault',
                  'sublink': 'https://segmentfault.com/events'},

        'legend': {'data': ['数量']},
        'xAxis': {
            'data': [x['week'] for x in data]
        },
        'yAxis': {},
        'series': {'name': '数量',
                   'data':
                       [x['count'] for x in data]
                   }
    }
    return json.dumps(result)


@app.route('/get_count_per_month', methods=['post', 'get'])
def get_count_per_month():
    sql = '''
            SELECT
            count(*)AS 'count',
            concat(substr(t.c_date, 6, 2),'月' )AS 'month'
            FROM
            segmentfault_events t
            GROUP BY substr(t.c_date, 6, 2)
            ORDER BY substr(t.c_date, 6, 2)
        '''
    data = SqlUtil.query_all(sql)
    result = {
        'title': {'text': '线下活动月份数量分布',
                  'subtext': '数据来自SegmentFault',
                  'sublink': 'https://segmentfault.com/events'},

        'legend': {'data': ['数量']},
        'xAxis': {
            'data': [x['month'] for x in data]
        },
        'yAxis': {},
        'series': {'name': '数量',
                   'data':
                       [x['count'] for x in data]
                   }
    }
    return json.dumps(result)


@app.route('/get_world_cloud', methods=['post', 'get'])
def get_world_cloud():
    sql = ''' SELECT t.`name` FROM segmentfault_events t '''
    data = SqlUtil.query_all(sql)
    names = [x['name'] for x in data]
    word_dict = {}
    for word in names:
        for a in word.split():
            if a.encode('utf-8').isalpha():  # 判断是不是英文,只统计英文的 keyword
                if a in word_dict.keys():
                    word_dict[a] += 1
                else:
                    word_dict[a] = 1
    print(len(word_dict))
    result = {
        'title': {'text': 'SegmentFault线下活动 keyword',
                  'subtext': '数据来自SegmentFault',
                  'sublink': 'https://segmentfault.com/events'},

        'tooltip': {
            'show': 'true'
        },
        'series': [{'name': '关键字',
                    'data':
                        [
                            {'name': k, 'value': v, 'itemStyle': 'createRandomItemStyle()'} for k, v in
                            word_dict.items() if v > 2
                            ]
                    }]
    }
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
