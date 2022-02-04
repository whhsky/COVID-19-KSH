import copy
import datetime
import json
import pandas as pd
from pyecharts.charts import Line, Map, Timeline, Pie, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from demo.models import Bentuxianyou31, J2Yxz, J2Ylj, Xyyq, Gnlssj


def xyqz(): # 新增确诊/现有确诊
    y = list(J2Yxz.objects.values_list('confirm', flat=True)) # 新增
    y1 = list(J2Ylj.objects.values_list('nowconfirm', flat=True)) # 现有
    x = list(J2Yxz.objects.values_list('dateid', flat=True)) # 日期

    tl = Timeline()
    xxx = ['新增确诊', '现有确诊']
    y = [y, y1]
    for i in range(len(xxx)):
        bar = (
            Line()
                .add_xaxis(x)
                .add_yaxis(xxx[i], y[i], symbol='circle',
                           is_smooth=True,
                           is_symbol_show=True,
                           symbol_size=6,
                           linestyle_opts=opts.LineStyleOpts(width=2),
                           label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
                           itemstyle_opts=opts.ItemStyleOpts(
                               color="skyblue", border_color="#fff", border_width=2
                           ))
                .set_series_opts(markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="max", name="max"), opts.MarkLineItem(type_="min", name="min")]),
                                 markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="max"),
                                                                         opts.MarkPointItem(type_="min", name="min")]))
                .set_global_opts(title_opts=opts.TitleOpts(title='全国' + xxx[i] + '人数趋势',
                                                           title_textstyle_opts=opts.TextStyleOpts(color='#ffffff')),
                                 visualmap_opts=opts.VisualMapOpts(textstyle_opts=opts.TextStyleOpts(color='#ffffff'),
                                                                   max_=int(max(y[i])), is_piecewise=True,
                                                                   pos_right='5%', pos_top='60%'),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45, color='#ffffff')),
                                 tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),

                                 yaxis_opts=opts.AxisOpts(name="Y", splitline_opts=opts.SplitLineOpts(is_show=True),
                                                          axislabel_opts=opts.LabelOpts(rotate=90, color='#ffffff')),

                                 legend_opts=opts.LegendOpts(pos_left='50%',
                                                             textstyle_opts=opts.TextStyleOpts(color='#ffffff')),
                                 )
        )
        tl.add(bar, xxx[i])
        tl.add_schema(is_auto_play=True, pos_bottom='88%', pos_left='25%',
                      label_opts=opts.LabelOpts(color='#ffffff', font_size=12))
    return tl.dump_options_with_quotes()

def zgdt(): # 中国现有确诊地图
    df = pd.read_csv('demo/csv/国内疫情数据.csv')
    time = df.drop_duplicates(subset=['dateId'], keep='last')

    tl = Timeline()
    for i in time['dateId']:
        df1 = copy.copy(df[df['dateId'] == i])
        df1.drop_duplicates(subset=['province'], keep='last', inplace=True)

        c = (
            Map()
                .add('累计确诊', [list(i) for i in zip(df1['province'], df1['confirm'])], 'china')
                .set_global_opts(title_opts=opts.TitleOpts(title='中国累计确诊时间线', pos_left='38%', title_textstyle_opts=opts.TextStyleOpts(color='#ffffff')),
                                 visualmap_opts=opts.VisualMapOpts(pos_right='0%', textstyle_opts=opts.TextStyleOpts(color='#ffffff'),
                                     is_piecewise=True, max_=int(df1['confirm'].max()), min_=int(df1['confirm'].min()),
                                     pieces=[
                                         {"min": 5001},
                                         {"min": 2001, 'max': 5000},
                                         {"min": 1801, "max": 2000},
                                         {"min": 1401, "max": 1800},
                                         {"min": 1001, "max": 1400},
                                         {"min": 801, "max": 1000},
                                         {"min": 601, "max": 800},
                                         {"min": 401, "max": 600},
                                         {"min": 201, "max": 400},
                                         {"min": 5, "max": 200, },
                                         {"max": 5}
                                     ]
                                ), toolbox_opts=opts.ToolboxOpts(), legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='#ffffff'), pos_right='85%'))
        )

        tl.add(c, i)
        tl.add_schema(is_auto_play=True, play_interval=1500, label_opts=opts.LabelOpts(color='#ffffff', font_size=12), pos_bottom='1%')
    return tl.dump_options_with_quotes()

def yqbt(): # 疫情饼图
    df = pd.DataFrame(Xyyq.objects.all().values())
    df = df.astype({'currentconfirmedcount': 'int64', 'confirmedcount': 'int64', 'curedcount': 'int64', 'deadcount':'int64'})
    df = df.sort_values('confirmedcount', ascending=False)  # 根据累计确诊去排序-降序
    df = df.drop_duplicates('provincename', keep='first')  # 根据省份去重,取第一次出现的数据
    df['provincename'] = df['provincename'].str.strip('省').str.strip('市').str.strip('壮族自治区').str.strip('自治区').str.strip('回族自治区').str.strip(
        '维吾尔自治区')  # pyecharts去除这些参数

    tl = Timeline()
    x = ['累计确诊', '累计死亡', '累计治愈', '现有确诊'][::-1]
    y = ['confirmedcount', 'deadcount', 'curedcount', 'currentconfirmedcount'][::-1]
    for i in range(len(x)):
        c = (
                Pie()
                .add(x[i], data_pair=[list(i) for i in zip(df['provincename'], df[y[i]])],
                     radius=['15%', '35%'],  center=["55%", "60%"])
                .set_global_opts(title_opts=opts.TitleOpts(title='中国疫情情况', pos_left='75%', pos_top='5%', title_textstyle_opts=opts.TextStyleOpts(color='#ffffff')),
                                 legend_opts=opts.LegendOpts(is_show=False))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
        tl.add(c, x[i])
        tl.add_schema(is_auto_play=True, pos_bottom='85%', orient='vertical', width='80px', height='400px', pos_right='5%', pos_top='16%',
                      label_opts=opts.LabelOpts(color='#ffffff', font_size=12), is_inverse=True)

    return tl.dump_options_with_quotes()


# 近31省市区现有病例
def bg():
    address = list(Bentuxianyou31.objects.values_list('address', flat = True))
    xyqz = list(Bentuxianyou31.objects.values_list('xyqz', flat = True))

    c = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add_xaxis(address)
            .add_yaxis('', xyqz)
            .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="max",name="max"),opts.MarkLineItem(type_="min",name="min")]),
                                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max",name="max"),opts.MarkPointItem(type_="min",name="min")]))
            .set_global_opts(title_opts=opts.TitleOpts(title='近期31省区市本土现有病例', title_textstyle_opts=opts.TextStyleOpts(color='#ffffff'), pos_left='35%', pos_top='5%'),
                visualmap_opts=opts.VisualMapOpts(textstyle_opts=opts.TextStyleOpts(color='#ffffff'),
                    max_=int(max(xyqz)), min_=int(min(xyqz)), is_piecewise=True, pos_right='5%', pos_top='40%'),
                xaxis_opts=opts.AxisOpts(name="省市区", axislabel_opts=opts.LabelOpts(rotate=90, color='#ffffff'),
                                         axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow")),
                tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
                datazoom_opts=opts.DataZoomOpts(is_show=False, type_='inside', range_start=30),
                 legend_opts=opts.LegendOpts(pos_right='5%', pos_top='5%', textstyle_opts=opts.TextStyleOpts(color='#ffffff')),
                 yaxis_opts=opts.AxisOpts(name="数量",  axislabel_opts=opts.LabelOpts(rotate=90, color='#ffffff'), splitline_opts=opts.SplitLineOpts(is_show=True)))
        )
    return c.dump_options_with_quotes()

# 高风险树形图
def gfx(t):
    import json
    from pyecharts import options as opts
    from pyecharts.charts import Tree

    with open(f"demo/data/{t}.json", "r", encoding="utf-8") as f:
        j = json.load(f)
    if t == '高风险':
        x = 'orangered'
        y = 1.5
    elif t == '中风险':
        x = 'darkorange'
        y = 1
    c = (
        Tree()
        .add("", [j], collapse_interval=20, is_roam=True, layout="radial", initial_tree_depth=y,  label_opts=opts.LabelOpts(color='#ffffff', font_size=9))
        .set_global_opts(title_opts=opts.TitleOpts(title=f"{t}地区", title_textstyle_opts=opts.TextStyleOpts(color=x, font_size=16),))
    )
    return c.dump_options_with_quotes()