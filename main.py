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
NAME_REFS[u'樊亮水Lance'] = [u'樊亮水LanCe']
NAME_REFS[u'沈家门囝2019'] = [u'司沈家门田2019', u'司沈家门田201', u'沈家门国2019', u'沈家门国201']
NAME_REFS[u'大成宇宙'] = [u'大成宇审', u'士大成宇宙']
NAME_REFS[u'春风化雨'] = [u'空春风化雨']
NAME_REFS[u'风和日丽'] = [u'风和日所']
NAME_REFS[u'老鼠辉辉'] = [u'O老鼠辉辉']
NAME_REFS[u'轻轻松松'] = [u'吉轻轻松松']
NAME_REFS[u'静心净德'] = [u'静心净']
NAME_REFS[u'海笑石烂'] = [u'海笑石']
NAME_REFS[u'云里雾中'] = [u'解云里雾中', u'经云里雾中', u'美云里雾中', u'经云里雾', u'要云里雾中']
NAME_REFS[u'wsy-448'] = [u'WSy-448']
NAME_REFS[u'KallyWang'] = [u'YKallyWang']
NAME_REFS[u'李时勤'] = [u'李时董', u'实李时勤', u'广李时勤', u'这李时勤']
NAME_REFS[u'邓昭明'] = [u'装邓昭明', u'数邓昭明']
NAME_REFS[u'凡不拙'] = [u'汤凡不拙']
NAME_REFS[u'冉朝阳'] = [u'母冉朝阳']
NAME_REFS[u'陈老兔'] = [u'陈老免', u'陈老矣']
NAME_REFS[u'邓玉洁'] = [u'武邓玉洁', u'邓玉']
NAME_REFS[u'郁方明'] = [u'美郁方明']
NAME_REFS[u'施小强'] = [u'三施小强']
NAME_REFS[u'卢松琴'] = [u'一卢松琴', u'卢松缈']
NAME_REFS[u'张亚林'] = [u'金张亚林']
NAME_REFS[u'曲天赫'] = [u'无曲天赫']
NAME_REFS[u'KallyWang'] = [u'YKallyWan']
NAME_REFS[u'jack21'] = [u'jaCk21', u'jacK21']
NAME_REFS[u'Yilia'] = [u'Yili']
NAME_REFS[u'peter'] = [u'petel']
NAME_REFS[u'董军'] = [u'董军8', u'董军B', u'董军国', u'董军江', u'董军胆', u'董军l']
NAME_REFS[u'张慧'] = [u'我张慧']
NAME_REFS[u'孙健'] = [u'顺孙健', u'僧孙健', u'啊孙健']
NAME_REFS[u'王怡'] = [u'王恰']
NAME_REFS[u'AO'] = [u'AC']


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
    _cntr = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.cntr.html')
    _luck = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.luck.html')
    _excl = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.excl.html')
    _joic = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.joic.html')
    _hope = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.hope.html')
    _amnt = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.amnt.html')
    _favr = os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.favr.html')
    print(_xlsx)
    print(_send)
    print(_play)
    print(_cntr)
    print(_luck)
    print(_excl)
    print(_joic)
    print(_hope)
    print(_amnt)
    print(_favr)

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
    cdict = {}                  #盈亏表
    ldict = {}                  #拼手速榜
    hdict = {}                  #最小抢包榜
    jdict = {}                  #最大不接龙
    edict = {}                  #最大抢包榜
    adict = {}                  #抢红包总额
    fdict = {}                  #连庄榜
    zdict = {}                  #个人榜
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
        run = '第'+str(count).zfill(2)+'轮'

        if count > 1 and fdict.get('第'+str(count-1).zfill(2)+'轮', '') and fdict['第'+str(count-1).zfill(2)+'轮']['sender'] == sender:
            fdict['第'+str(count).zfill(2)+'轮'] = {'sender': sender, 'kiss': fdict['第'+str(count-1).zfill(2)+'轮']['kiss'] + 1}
        else:
            fdict['第'+str(count).zfill(2)+'轮'] = {'sender': sender, 'kiss': 1}

        print('第'+str(count).zfill(2)+'轮', fdict['第'+str(count).zfill(2)+'轮'])

        adict[run] = 0.0
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

            adict[run] = round(adict[run]+float(amount), 2)

            if player in zdict:
                zdict[player][run] = amount
            else:
                zdict[player] = {run: amount}

            minimum = float(hdict.get(run, '200\n无名氏').split('\n')[0])
            if minimum == float(amount):
                hdict[run] += '\n' + player
            elif minimum > float(amount):
                hdict[run] = str(amount) + '\n' + player
            else:
                pass

            maximum = float(edict.get(run, '0\n无名氏').split('\n')[0])
            runner  = float(jdict.get(run, '0\n无名氏').split('\n')[0])
            if maximum == float(amount):
                edict[run] += '\n' + player
            elif runner == float(amount):
                jdict[run] += '\n' + player
            elif maximum < float(amount):
                if edict.get(run, ''):
                    jdict[run] = edict[run]
                edict[run] = str(amount) + '\n' + player
            elif runner < float(amount):
                jdict[run] = str(amount) + '\n' + player
            else:
                pass

        print('Minimum: ' + hdict[run])
        print('Maximum: ' + edict[run])
        print('Runner:  ' + jdict[run])

        count += 1
        #if count == 5:
        #    break
    book.close()

    for key in pdict.keys():
        if key in sdict.keys():
            cdict[key] = round(float(sdict[key]) - float(pdict[key]), 2)
        else:
            cdict[key] = round(0.0 - float(pdict[key]), 2)

    for key in zdict.keys():
        for i in range(1, count):
            run = '第'+str(i).zfill(2)+'轮'
            if run not in zdict[key]:
                zdict[key][run] = 0.0

    #for key in zdict.keys():
    #    print(key, "\t", zdict[key])

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

    #按从小到大的顺序显示红包奉献榜
    clist = list(cdict.items())
    clist.sort(key=lambda x:x[1],reverse=False)
    cbar = Bar()
    cbar.add_xaxis([x[0] for x in clist])
    cbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包奉献榜——"+str(len(clist))+"人"+"(最大盈利："+clist[0][0]+"/"+str(abs(clist[0][1]))+"；最大亏损："+clist[-1][0]+"/"+str(clist[-1][1])+")", [x[1] for x in clist])
    cbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45)))
    cbar.render(_cntr)

    #按从小到大的顺序显示拼手速榜
    llist = list(ldict.items())
    llist.sort(key=lambda x:x[1],reverse=False)
    lbar = Bar()
    lbar.add_xaxis([x[0] for x in llist])
    lbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包幸运榜", [x[1] for x in llist])
    lbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45)))
    lbar.render(_luck)

    #按从小到大的顺序显示最小抢包榜
    hlist = list(hdict.items())
    hlist.sort(key=lambda x:x[0],reverse=False)
    hbar = Bar()
    hbar.add_xaxis(['/'.join(x[1].split('\n')[1:]) for x in hlist])
    hbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包希望榜", [x[1].split('\n')[0] for x in hlist])
    hbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
    hbar.render(_hope)

    #按从小到大的顺序显示最小抢包榜
    jlist = list(jdict.items())
    jlist.sort(key=lambda x:x[0],reverse=False)
    jbar = Bar()
    jbar.add_xaxis(['/'.join(x[1].split('\n')[1:]) for x in jlist])
    jbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包开心榜", [x[1].split('\n')[0] for x in jlist])
    jbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
    jbar.render(_joic)

    #按从小到大的顺序显示最大抢包榜
    elist = list(edict.items())
    elist.sort(key=lambda x:x[0],reverse=False)
    ebar = Bar()
    ebar.add_xaxis(['/'.join(x[1].split('\n')[1:]) for x in elist])
    ebar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包卓越榜", [x[1].split('\n')[0] for x in elist])
    ebar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
    ebar.render(_excl)

    #按从小到大的顺序显示最大抢包榜
    alist = list(adict.items())
    alist.sort(key=lambda x:x[0],reverse=False)
    abar = Bar()
    abar.add_xaxis([x[0] for x in alist])
    abar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包信用榜", [x[1] for x in alist])
    abar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
    abar.render(_amnt)

    #按从小到大的顺序显示连庄榜
    flist = list(fdict.items())
    flist.sort(key=lambda x:x[0],reverse=False)
    fbar = Bar()
    fbar.add_xaxis([x[1]['sender'] for x in flist])
    fbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包爱神之吻榜", [x[1]['kiss'] for x in flist])
    fbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
    fbar.render(_favr)

    for key in zdict.keys():
        zlist = list(zdict[key].items())
        zlist.sort(key=lambda x:x[0],reverse=False)
        zbar = Bar()
        zbar.add_xaxis([x[0] for x in zlist])
        zbar.add_yaxis("交大校友交流学习群"+_date[:4]+"年"+_date[4:6]+"月"+_date[6:]+"日红包风采榜——"+key, [x[1] for x in zlist])
        zbar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45, font_size=10)))
        zbar.render(os.path.join(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])+'.'+key+'.html'))

