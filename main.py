# -*- coding: utf-8 -*-
"""
@author: aoqingy
"""
import os
import sys
import cv2
import json
import time
import model


def detect(path):
    _,result,_ = model.model(cv2.imread(path),
                             detectAngle = False,
                             config = dict(MAX_HORIZONTAL_GAP = 50,#字符之间最大间隔，用于文本行合并
                                           MIN_V_OVERLAPS = 0.6,
                                           MIN_SIZE_SIM = 0.6,
                                           TEXT_PROPOSALS_MIN_SCORE = 0.1,
                                           TEXT_PROPOSALS_NMS_THRESH = 0.3,
                                           TEXT_LINE_NMS_THRESH = 0.7,#文本行之间测iou值
                                           ),
                             leftAdjust = True, #对检测的文本行进行向左延伸
                             rightAdjust = True,#对检测的文本行进行向右延伸
                             alph = 0.01,       #对检测的文本行进行向右、左延伸的倍数
                             )

    return result


NAME_REFS = {}
NAME_REFS[u'大成宇宙'] = [u'大成宇审', u'士大成宇宙']
NAME_REFS[u'董军'] = [u'董军8', u'董军B', u'董军国', u'董军江']
NAME_REFS[u'jack21'] = [u'jaCk21']
NAME_REFS[u'樊亮水Lance'] = [u'樊亮水LanCe']
NAME_REFS[u'李时勤'] = [u'李时董', u'实李时勤', u'广李时勤']
NAME_REFS[u'张慧'] = [u'我张慧']
NAME_REFS[u'邓昭明'] = [u'装邓昭明']
NAME_REFS[u'云里雾中'] = [u'解云里雾中', u'经云里雾中', u'美云里雾中']
NAME_REFS[u'孙健'] = [u'顺孙健']
NAME_REFS[u'轻轻松松'] = [u'吉轻轻松松']
NAME_REFS[u'凡不拙'] = [u'汤凡不拙']
NAME_REFS[u'冉朝阳'] = [u'母冉朝阳']
NAME_REFS[u'陈老兔'] = [u'陈老免', u'陈老矣']
NAME_REFS[u'风和日丽'] = [u'风和日所']
NAME_REFS[u'邓玉洁'] = [u'武邓玉洁']


def correct_name(name):
    for key in NAME_REFS.keys():
        if name in NAME_REFS[key]:
            return key
    return name


def parse_text(result):
    for item in result:
        print(item['text'])


def parse_sender(result):
    for item in result:
        if u"的红包" in item['text']:
            return correct_name(item['text'][:-4])
    return ''


def parse_speed(result):
    for item in result:
        if u"被抢光" in item['text']:
            total,speed = item['text'].split(',')
            return total[:-2], speed[:-3]
    return '', ''


def parse_players(result):
    rplayers = []
    start = 0
    found = 0
    index = 0

    while True:
        if not start:
            if u"被抢光" in result[index]['text']:
                start = index + 1
            index += 1
            continue

        print('---', index, '---')

        # 貌似数量和时间识别不会出错
        # 名称和数量分别占第一个和第二个
        # 本段逻辑不能处理名称没有的情况，因此，如果微信昵称为单字（例如邓、学），
        # 可能导致整条红包记录无法解析。建议添加微信好友的方式修改好友注释为多字
        # （红包显示优先使用好友注释）
        # 最佳可能没有。如果没有，时间为第三个；如果有，时间和最佳分别占第三个和第四个。
        #player\namount\ntime
        #player\namount\ntime\nbest
        #player\namount\nbest\ntime
        #amount\nplayer\ntime
        #amount\nplayer\ntime\nbest
        #amount\nplayer\nbest\ntime

        rplayer = {}
        if result[index]['text'].endswith(u'元'):
            try:
                rplayer['amount'] = str(float(result[index]['text'][:-1]))
                rplayer['player'] = correct_name(result[index+1]['text'])
                index += 2
            except:
                rplayer['player'] = correct_name(result[index]['text'])
                rplayer['amount'] = str(float(result[index+1]['text'][:-1]))
                index += 2
                
        else:
            rplayer['player'] = correct_name(result[index]['text'])
            rplayer['amount'] = str(float(result[index+1]['text'][:-1]))
            index += 2

        #如果识别出多余的内容（非时间和最佳），忽略之
        if (index < len(result) and 
                not u'手气' in result[index]['text'] and
                not ':' in result[index]['text']):
            index += 1

        if ((index < len(result) and u'手气' in result[index]['text']) or 
                (index+1 < len(result) and u'手气' in result[index+1]['text'])):
            rplayer['largest'] = 'True'
            index += 1

        if ((index < len(result) and ':' in result[index]['text']) or 
                (index+1 < len(result) and ':' in result[index+1]['text'])):
            index += 1

        if ((index < len(result) and u'手气' in result[index]['text']) or
                (index+1 < len(result) and u'手气' in result[index+1]['text'])):
            rplayer['largest'] = 'True'
            index += 1

        rplayers.append(rplayer)

        if index >= len(result):
            break

    return rplayers


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("No path specified!")
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("Path invalid!")
        sys.exit(1)

    print(os.path.dirname(sys.argv[1]))
    print(os.path.basename(sys.argv[1]))
    _path = sys.argv[1]
    _date = os.path.basename(sys.argv[1])
    _xlsx = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.xlsx')
    _send = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.send.html')
    _play = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.play.html')
    _luck = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.luck.html')
    print(_xlsx)
    print(_send)
    print(_play)
    print(_luck)

    import xlrd
    import xlsxwriter

    book = xlsxwriter.Workbook(_xlsx)
    sheet = book.add_worksheet()

    iformat = book.add_format()
    iformat.set_text_wrap()
    iformat.set_font_name('Microsoft YaHei')
    iformat.set_bold(False)
    iformat.set_align('left')
    iformat.set_align('vcenter')
    iformat.set_font_color('black')

    vformat = book.add_format()
    vformat.set_text_wrap()
    vformat.set_font_name('Microsoft YaHei')
    vformat.set_bold(False)
    vformat.set_align('left')
    vformat.set_align('vcenter')
    vformat.set_font_color('red')

    sheet.set_column('A:A',6)
    sheet.set_column('B:B',18)
    sheet.set_column('C:C',10)
    sheet.set_column('D:M',12)

    #写标题行
    sheet.write('A1', u"序号", iformat)
    sheet.write('B1', u"发红包", iformat)
    sheet.write('C1', u"抢包时间", iformat)
    sheet.write('D1', u"抢包一", iformat)
    sheet.write('E1', u"抢包二", iformat)
    sheet.write('F1', u"抢包三", iformat)
    sheet.write('G1', u"抢包四", iformat)
    sheet.write('H1', u"抢包五", iformat)
    sheet.write('I1', u"抢包六", iformat)
    sheet.write('J1', u"抢包七", iformat)
    sheet.write('K1', u"抢包八", iformat)
    sheet.write('L1', u"抢包九", iformat)
    sheet.write('M1', u"抢包十", iformat)

    sdict = {}			#发红包榜
    pdict = {}			#抢红包榜
    ldict = {}                  #拼手速榜
    count = 1
    for _file in sorted(os.listdir(_path), reverse=False):
        print("=============================================")
        print(_file)
        result = detect(os.path.join(_path, _file))
        print(parse_text(result))

        sheet.write('A'+str(count+1), str(count), iformat)

        sender = parse_sender(result)
        sheet.write('B'+str(count+1), sender, iformat)
        sdict[sender] = sdict.get(sender, 0) + 10
        
        sheet.write('C'+str(count+1), '/'.join(parse_speed(result)), iformat)
        try:
            players = parse_players(result)
        except Exception as e:
            print("********************************************")
            print("********************************************")
            print("********************************************")
            count += 1
            continue

        for player in players:
            for p in sorted(player.items(), key=lambda x:x[0], reverse=False):
                print('{}:{}'.format(p[0], p[1]), end='\t')
            print('')

        LABELS = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        for i in range(0, 10):
            if len(players) <= i:
                continue

            player = players[i].get('player', '无名氏')
            amount = players[i].get('amount', 0.0)
            if players[i].get('largest', ''):
                sheet.write(LABELS[i]+str(count+1), player + '/' + str(amount), vformat)
            else:
                sheet.write(LABELS[i]+str(count+1), player + '/' + str(amount), iformat)
            pdict[player] = round(pdict.get(player, 0) + float(amount), 2)

            ldict[player] = ldict.get(player, 0) + 1

        count += 1
        #if count == 10:
        #    break
    book.close()

    from pyecharts import options as opts
    from pyecharts.charts import Bar

    #按从大到小的顺序显示红包发放榜
    slist = list(sdict.items())
    slist.sort(key=lambda x:x[1],reverse=True)
    sbar = Bar()
    sbar.add_xaxis([x[0] for x in slist])
    sbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包爱心榜", [x[1] for x in slist])
    sbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=30)))
    sbar.render(_send)

    #按从小到大的顺序显示红包收益榜
    plist = list(pdict.items())
    plist.sort(key=lambda x:x[1],reverse=False)
    pbar = Bar()
    pbar.add_xaxis([x[0] for x in plist])
    pbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包福利榜", [x[1] for x in plist])
    pbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45)))
    pbar.render(_play)

    #按从小到大的顺序显示拼手速榜
    llist = list(ldict.items())
    llist.sort(key=lambda x:x[1],reverse=False)
    lbar = Bar()
    lbar.add_xaxis([x[0] for x in llist])
    lbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包幸运榜", [x[1] for x in llist])
    lbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45)))
    lbar.render(_luck)

