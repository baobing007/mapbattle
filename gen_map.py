# -*- coding: utf-8 -*-
import json, urllib.request, math

# ===== 34个省级行政区元数据 =====
# area: 面积(万km²)  abbr:简称  alias:别称  adcode: DataV行政区划代码
META = {
 'bj' :{'name':'北京','cap':'北京','abbr':'京','alias':'燕京','area':1.64,'emoji':'🐼','feat':'故宫·长城·烤鸭·京剧·胡同·天安门·颐和园','color':'#FA7921','adcode':110000},
 'tj' :{'name':'天津','cap':'天津','abbr':'津','alias':'津门','area':1.19,'emoji':'🚢','feat':'相声·狗不理·五大道·煎饼果子·杨柳青年画·天津之眼','color':'#FFBA08','adcode':120000},
 'heb':{'name':'河北','cap':'石家庄','abbr':'冀','alias':'燕赵大地','area':18.88,'emoji':'🏯','feat':'避暑山庄·山海关·驴肉火烧·赵州桥·吴桥杂技·白洋淀','color':'#6A4C93','adcode':130000},
 'sx' :{'name':'山西','cap':'太原','abbr':'晋','alias':'三晋大地','area':15.67,'emoji':'🍜','feat':'平遥古城·刀削面·云冈石窟·陈醋·晋商·五台山·悬空寺','color':'#C1666B','adcode':140000},
 'nmg':{'name':'内蒙古','cap':'呼和浩特','abbr':'蒙','alias':'草原之乡','area':118.67,'emoji':'🐎','feat':'大草原·烤全羊·那达慕·蒙古包·呼伦贝尔·马头琴','color':'#7FB069','adcode':150000},
 'ln' :{'name':'辽宁','cap':'沈阳','abbr':'辽','alias':'辽沈大地','area':14.86,'emoji':'🦀','feat':'沈阳故宫·锅包肉·大连海鲜·二人转·千山·满族文化','color':'#E55934','adcode':210000},
 'jl' :{'name':'吉林','cap':'长春','abbr':'吉','alias':'白山松水','area':18.74,'emoji':'🌽','feat':'长白山·雾凇·人参·朝鲜冷面·一汽·鹿茸','color':'#9BC53D','adcode':220000},
 'hlj':{'name':'黑龙江','cap':'哈尔滨','abbr':'黑','alias':'北国龙疆','area':45.25,'emoji':'❄️','feat':'冰雪大世界·红肠·太阳岛·五常大米·北极村·北大荒','color':'#5BC0EB','adcode':230000},
 'sh' :{'name':'上海','cap':'上海','abbr':'沪','alias':'申城','area':0.63,'emoji':'🏙️','feat':'外滩·小笼包·东方明珠·生煎·石库门·本帮菜','color':'#2A9D8F','adcode':310000},
 'js' :{'name':'江苏','cap':'南京','abbr':'苏','alias':'金陵','area':10.72,'emoji':'🍤','feat':'苏州园林·鸭血粉丝·太湖·碧螺春·昆曲·夫子庙·中山陵','color':'#E76F51','adcode':320000},
 'zj' :{'name':'浙江','cap':'杭州','abbr':'浙','alias':'钱塘','area':10.55,'emoji':'🍵','feat':'西湖·龙井·乌镇·东坡肉·越剧·千岛湖·丝绸','color':'#F4A261','adcode':330000},
 'ah' :{'name':'安徽','cap':'合肥','abbr':'皖','alias':'徽州','area':14.01,'emoji':'🍲','feat':'黄山·徽菜·宏村·毛峰茶·黄梅戏·宣纸','color':'#E9C46A','adcode':340000},
 'fj' :{'name':'福建','cap':'福州','abbr':'闽','alias':'榕城','area':12.40,'emoji':'🍵','feat':'鼓浪屿·土楼·铁观音·佛跳墙·妈祖·武夷山','color':'#264653','adcode':350000},
 'jx' :{'name':'江西','cap':'南昌','abbr':'赣','alias':'豫章','area':16.69,'emoji':'🍊','feat':'庐山·景德镇·滕王阁·瓦罐汤·井冈山·脐橙','color':'#2A9D8F','adcode':360000},
 'sd' :{'name':'山东','cap':'济南','abbr':'鲁','alias':'齐鲁','area':15.79,'emoji':'🍺','feat':'泰山·孔庙·青岛啤酒·煎饼卷大葱·趵突泉·蓬莱阁','color':'#E76F51','adcode':370000},
 'hen':{'name':'河南','cap':'郑州','abbr':'豫','alias':'中原','area':16.70,'emoji':'🍜','feat':'少林寺·龙门石窟·胡辣汤·牡丹·豫剧·殷墟·烩面','color':'#F4A261','adcode':410000},
 'hub':{'name':'湖北','cap':'武汉','abbr':'鄂','alias':'荆楚','area':18.59,'emoji':'🐟','feat':'黄鹤楼·热干面·武当山·三峡·武昌鱼·神农架','color':'#E9C46A','adcode':420000},
 'hun':{'name':'湖南','cap':'长沙','abbr':'湘','alias':'潇湘','area':21.18,'emoji':'🌶️','feat':'张家界·辣椒·岳麓山·臭豆腐·岳阳楼·湘绣·马王堆','color':'#E63946','adcode':430000},
 'gd' :{'name':'广东','cap':'广州','abbr':'粤','alias':'羊城','area':17.97,'emoji':'🍲','feat':'广州塔·早茶·丹霞山·粤剧·潮汕牛肉丸·醒狮·煲仔饭','color':'#06D6A0','adcode':440000},
 'gx' :{'name':'广西','cap':'南宁','abbr':'桂','alias':'八桂','area':23.76,'emoji':'🥥','feat':'桂林山水·螺蛳粉·漓江·壮锦·德天瀑布·涠洲岛','color':'#118AB2','adcode':450000},
 'hn' :{'name':'海南','cap':'海口','abbr':'琼','alias':'琼崖','area':3.54,'emoji':'🌴','feat':'三亚·椰子·天涯海角·文昌鸡·黎锦·亚龙湾·清补凉','color':'#06D6A0','adcode':460000},
 'cq' :{'name':'重庆','cap':'重庆','abbr':'渝','alias':'山城','area':8.24,'emoji':'🌶️','feat':'火锅·洪崖洞·磁器口·大足石刻·小面·三峡','color':'#EF476F','adcode':500000},
 'sc' :{'name':'四川','cap':'成都','abbr':'川','alias':'天府之国','area':48.61,'emoji':'🐼','feat':'大熊猫·火锅·九寨沟·川剧变脸·峨眉山·都江堰·蜀绣','color':'#FFD166','adcode':510000},
 'gz' :{'name':'贵州','cap':'贵阳','abbr':'黔','alias':'黔中','area':17.62,'emoji':'🏞️','feat':'黄果树·茅台·酸汤鱼·梵净山·蜡染·侗族大歌','color':'#06D6A0','adcode':520000},
 'yn' :{'name':'云南','cap':'昆明','abbr':'云','alias':'彩云之南','area':39.41,'emoji':'🌸','feat':'石林·米线·丽江古城·普洱茶·泼水节·玉龙雪山·鲜花饼','color':'#118AB2','adcode':530000},
 'xz' :{'name':'西藏','cap':'拉萨','abbr':'藏','alias':'雪域','area':122.84,'emoji':'🏔️','feat':'布达拉宫·珠峰·纳木错·酥油茶·唐卡·藏传佛教','color':'#457B9D','adcode':540000},
 'shx':{'name':'陕西','cap':'西安','abbr':'陕','alias':'三秦','area':20.56,'emoji':'🏯','feat':'兵马俑·城墙·华山·羊肉泡馍·秦腔·大雁塔·黄土高原','color':'#F4A261','adcode':610000},
 'gs' :{'name':'甘肃','cap':'兰州','abbr':'甘','alias':'陇原','area':42.58,'emoji':'🍜','feat':'牛肉面·敦煌·莫高窟·嘉峪关·七彩丹霞·月牙泉·河西走廊','color':'#E9C46A','adcode':620000},
 'qh' :{'name':'青海','cap':'西宁','abbr':'青','alias':'三江源','area':72.23,'emoji':'🏔️','feat':'青海湖·可可西里·塔尔寺·茶卡盐湖·手抓羊肉·三江源','color':'#457B9D','adcode':630000},
 'nx' :{'name':'宁夏','cap':'银川','abbr':'宁','alias':'塞上江南','area':6.64,'emoji':'🐫','feat':'西夏陵·枸杞·沙坡头·手抓羊肉·贺兰山·镇北堡','color':'#E76F51','adcode':640000},
 'xj' :{'name':'新疆','cap':'乌鲁木齐','abbr':'新','alias':'西域','area':166.49,'emoji':'🐫','feat':'天山·葡萄沟·羊肉串·喀纳斯·和田玉·火焰山·大盘鸡','color':'#2A9D8F','adcode':650000},
 'tw' :{'name':'台湾','cap':'台北','abbr':'台','alias':'宝岛','area':3.60,'emoji':'🏝️','feat':'阿里山·日月潭·卤肉饭·珍珠奶茶·台北101·太鲁阁','color':'#118AB2','adcode':710000},
 'hk' :{'name':'香港','cap':'香港','abbr':'港','alias':'东方之珠','area':0.1107,'emoji':'🌆','feat':'维港·迪士尼·早茶·太平山·烧腊·星光大道','color':'#EF476F','adcode':810000},
 'mo' :{'name':'澳门','cap':'澳门','abbr':'澳','alias':'濠江','area':0.033,'emoji':'🎰','feat':'大三巴·葡式蛋挞·妈阁庙·水蟹粥·威尼斯人·猪扒包','color':'#FFD166','adcode':820000},
}

# 扩充数据（经联网核实）：省级别称(更多雅称，仅表格展示) / 省会城市别称 / 省会城市特色
ALIAS_MORE = {
 'bj':['幽燕','京华','北平'], 'tj':['津沽','沽上'], 'heb':['畿辅之地','冀州'], 'sx':['晋阳','并州'],
 'nmg':['塞北','漠南'], 'ln':['辽海','奉天'], 'jl':['关东'], 'hlj':['北大仓','黑土地'],
 'sh':['华亭','沪上'], 'js':['江淮'], 'zj':['之江'], 'ah':['皖'], 'fj':['八闽'], 'jx':['赣鄱'],
 'sd':['海右'], 'hen':['中州'], 'hub':['楚'], 'hun':['湘'],
 'gd':['岭南','南粤'], 'gx':['桂海'], 'hn':['琼'],
 'cq':['巴渝','渝州'], 'sc':['巴蜀'], 'gz':['黔'], 'yn':['云岭','滇'], 'xz':['吐蕃','藏地'],
 'shx':['秦','关中'], 'gs':['陇'], 'qh':['河源'], 'nx':['朔方'], 'xj':['回疆'],
 'tw':['鲲岛'], 'hk':['香江','港岛'], 'mo':['妈港'],
}
CAP_ALIAS = {
 'bj':['燕京','北平'], 'tj':['津沽','直沽'], 'heb':['石门'], 'sx':['晋阳','并州','龙城'],
 'nmg':['归绥','青城'], 'ln':['盛京','奉天'], 'jl':['北国春城','喜都','黄龙府'], 'hlj':['冰城','东方莫斯科'],
 'sh':['申城','华亭','沪上'], 'js':['金陵','建康'], 'zj':['临安','钱塘','武林'], 'ah':['庐州'],
 'fj':['榕城','三山'], 'jx':['洪城','豫章'], 'sd':['泉城','历下'], 'hen':['商都','绿城'],
 'hub':['江城'], 'hun':['星城','潭州'], 'gd':['羊城','花城','穗城'], 'gx':['邕城','绿城'],
 'hn':['椰城'], 'cq':['山城','渝州','巴渝'], 'sc':['蓉城','锦官城'], 'gz':['林城','筑城'],
 'yn':['春城'], 'xz':['逻些','日光城'], 'shx':['长安','镐京'], 'gs':['金城'],
 'qh':['青唐城','夏都'], 'nx':['凤凰城'], 'xj':['乌市','迪化'], 'tw':['北市'], 'hk':['香江','港岛'], 'mo':['濠江','妈港'],
}
CAP_FEAT = {
 'bj':['故宫','天安门','长城','天坛','烤鸭','颐和园'],
 'tj':['相声','狗不理','五大道','天津之眼','古文化街'],
 'heb':['赵州桥','西柏坡','正定古城','苍岩山','白洋淀'],
 'sx':['晋祠','平遥','刀削面','双塔寺','煤炭','陈醋'],
 'nmg':['大召寺','草原','手把肉','白塔','昭君墓'],
 'ln':['沈阳故宫','足球','老边饺子','张氏帅府','工业','中山广场'],
 'jl':['伪满皇宫','汽车城','长影世纪城','净月潭','南湖'],
 'hlj':['冰雪大世界','中央大街','红肠','冰雕','索菲亚教堂','松花江'],
 'sh':['外滩','东方明珠','豫园','南京路','石库门','城隍庙'],
 'js':['中山陵','夫子庙','盐水鸭','明城墙','玄武湖','总统府'],
 'zj':['西湖','灵隐寺','龙井茶','钱塘江','丝绸','雷峰塔'],
 'ah':['包公祠','黄山','李鸿章故居','庐剧','三河古镇','逍遥津'],
 'fj':['三坊七巷','鼓山','鱼丸','西湖公园','林则徐纪念馆'],
 'jx':['滕王阁','庐山','炒粉','八一起义纪念馆','绳金塔'],
 'sd':['趵突泉','大明湖','把子肉','千佛山','泉城广场','黑虎泉'],
 'hen':['少林寺','黄河','烩面','二七纪念塔','商都','玉米楼'],
 'hub':['黄鹤楼','热干面','东湖','武汉大学','长江大桥','户部巷'],
 'hun':['岳麓山','橘子洲','臭豆腐','马王堆','广电','火宫殿'],
 'gd':['广州塔','早茶','陈家祠','白云山','花市','沙面'],
 'gx':['青秀山','桂林','老友粉','民歌湖','五象广场'],
 'hn':['骑楼老街','椰风','假日海滩','火山口','五公祠'],
 'cq':['洪崖洞','火锅','解放碑','磁器口','轻轨','长江索道'],
 'sc':['大熊猫','宽窄巷子','锦里','火锅','蜀绣','武侯祠'],
 'gz':['黔灵山','甲秀楼','肠旺面','大数据','花溪'],
 'yn':['石林','滇池','鲜花饼','翠湖','民族村','金马碧鸡坊'],
 'xz':['布达拉宫','大昭寺','八廓街','藏面','罗布林卡'],
 'shx':['兵马俑','大雁塔','城墙','钟楼','凉皮','回民街'],
 'gs':['黄河铁桥','牛肉面','白塔山','水车','五泉山'],
 'qh':['塔尔寺','青海湖','东关清真寺','酿皮','北禅寺'],
 'nx':['西夏王陵','沙湖','手抓','鼓楼','南门广场'],
 'xj':['天山','国际大巴扎','烤包子','红山','二道桥'],
 'tw':['101','夜市','故宫博物院','士林','西门町'],
 'hk':['维港','迪士尼','茶餐厅','海洋公园','太平山'],
 'mo':['大三巴','葡京','蛋挞','旅游塔','官也街'],
}

# 七大地理分区（后续扩展：区域着色 / 分区练习 / 薄弱省统计 的前置数据）
REGION={
 'bj':'华北','tj':'华北','heb':'华北','sx':'华北','nmg':'华北',
 'ln':'东北','jl':'东北','hlj':'东北',
 'sh':'华东','js':'华东','zj':'华东','ah':'华东','fj':'华东','jx':'华东','sd':'华东','tw':'华东',
 'hen':'华中','hub':'华中','hun':'华中',
 'gd':'华南','gx':'华南','hn':'华南','hk':'华南','mo':'华南',
 'cq':'西南','sc':'西南','gz':'西南','yn':'西南','xz':'西南',
 'shx':'西北','gs':'西北','qh':'西北','nx':'西北','xj':'西北',
}

def download(adcode):
    url='https://geo.datav.aliyun.com/areas_v3/bound/%d.json'%adcode
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

def is_pos(node):
    return isinstance(node,list) and len(node)>=2 and isinstance(node[0],(int,float)) and isinstance(node[1],(int,float))

def iter_positions(node):
    if is_pos(node):
        yield node
    elif isinstance(node,list):
        for c in node:
            yield from iter_positions(c)

def iter_rings(geom):
    c=geom['coordinates']; out=[]
    if geom['type']=='Polygon':
        for ring in c:
            if ring and is_pos(ring[0]): out.append(ring)
    elif geom['type']=='MultiPolygon':
        for poly in c:
            for ring in poly:
                if ring and is_pos(ring[0]): out.append(ring)
    else:
        pos=list(iter_positions(c))
        if pos: out.append(pos)
    return out

# 统一投影范围：中国主体（含海南主岛、台湾、港澳），排除南海诸岛等境外岛
LON0,LON1,LAT0,LAT1 = 73.0,136.0,17.0,54.0
MAP_X0,MAP_X1,MAP_Y0,MAP_Y1 = 20,740,20,600
# 投影略缩小(0.80)，为猴子版"拉开间距"留出余量
SCALE = min((MAP_X1-MAP_X0)/(LON1-LON0),(MAP_Y1-MAP_Y0)/(LAT1-LAT0))*0.80
XO = MAP_X0 + ((MAP_X1-MAP_X0)-(LON1-LON0)*SCALE)/2
YO = MAP_Y0 + ((MAP_Y1-MAP_Y0)-(LAT1-LAT0)*SCALE)/2
def proj(pt):
    x=float(pt[0]); y=float(pt[1])
    return (XO+(x-LON0)*SCALE, YO+(LAT1-y)*SCALE)

def perp(a,b,p):
    (x1,y1),(x2,y2),(x0,y0)=a,b,p
    dx=x2-x1; dy=y2-y1
    if dx==0 and dy==0: return math.hypot(x0-x1,y0-y1)
    t=((x0-x1)*dx+(y0-y1)*dy)/(dx*dx+dy*dy)
    t=max(0,min(1,t))
    return math.hypot(x0-(x1+t*dx), y0-(y1+t*dy))
def rdp(pts,eps):
    if len(pts)<3: return pts
    dmax=0; idx=0
    for i in range(1,len(pts)-1):
        d=perp(pts[0],pts[-1],pts[i])
        if d>dmax: dmax=d; idx=i
    if dmax>eps:
        L=rdp(pts[:idx+1],eps); R=rdp(pts[idx:],eps)
        return L[:-1]+R
    return [pts[0],pts[-1]]

def _keep_ring(ring):
    lats=[p[1] for p in ring]
    return not (len(lats)>2 and sum(lats)/len(lats) < 16)

def geom_paths(geom):
    d=''
    for ring in iter_rings(geom):
        if not _keep_ring(ring): continue
        pr=[proj(p) for p in ring]
        pr=rdp(pr,1.5)
        if pr[0]!=pr[-1]: pr.append(pr[0])
        nums=[]
        for i,(x,y) in enumerate(pr):
            nums.append(('M' if i==0 else 'L')+('%.1f %.1f'%(x,y)))
        d+=' '.join(nums)+' Z '
    return d

def main_pts(geom):
    out=[]
    for ring in iter_rings(geom):
        if not _keep_ring(ring): continue
        for p in ring:
            out.append(proj(p))
    return out

# ---- 下载全部34省几何 ----
geoms={}
for k,m in META.items():
    g=download(m['adcode'])
    geoms[k]=g['features'][0]['geometry']

# ---- 猴子版参数 ----
# 面积等比例 + 真实长宽比；整体缩小、留间距；中心锁在真实地理中心，
# 仅做轻量"推开重叠 + 弱回弹到真实中心"，保证相对位置与中国一致
maxarea=max(m['area'] for m in META.values())
SCALE_AREA = 12000.0/maxarea   # 整体缩小，避免大面积省份过大、互相挤占
SHRINK=0.82                    # 略缩留缝
MAX_SIDE=118.0
MIN_SIDE=17.0

# ---- 托盘网格（按面积降序占位，减少大块互相遮挡） ----
keys_by_area=sorted(META.keys(), key=lambda k:-META[k]['area'])
COLS=7; GX=104.0; SX=46.0; GY=120.0; SY=662.0
home={}
for i,k in enumerate(keys_by_area):
    r=i//COLS; c=i%COLS
    home[k]=(round(SX+c*GX,1), round(SY+r*GY,1))
VH = int(SY + ((len(META)-1)//COLS)*GY + 74)

# 先算每省真实中心、真实bbox长宽比、简化路径
# 注：北京/天津几何质心与河北几乎重合（被河北包围），猴子版改用城市代表点作中心，
# 避免三块挤在一起、方位错乱（北京在天津西北、河北居中包围）
CENTER_OVERRIDE={'bj':(116.4,40.2),'tj':(117.4,39.1)}
prov={}
for key,m in META.items():
    geom=geoms[key]
    d=geom_paths(geom)
    pts=main_pts(geom)
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    rcx=sum(xs)/len(xs); rcy=sum(ys)/len(ys)
    if key in CENTER_OVERRIDE:
        lon,lat=CENTER_OVERRIDE[key]
        mcx0=XO+(lon-LON0)*SCALE; mcy0=YO+(LAT1-lat)*SCALE
    else:
        mcx0=rcx; mcy0=rcy
    prov[key]=dict(d=d, rcx=rcx, rcy=rcy, mcx0=mcx0, mcy0=mcy0,
                   rx0=min(xs), rx1=max(xs), ry0=min(ys), ry1=max(ys))

# 猴子版：面积等比例矩形（整体缩小），中心=真实地理中心
rectsz={}
for key,m in META.items():
    P=prov[key]
    bw_real=max(P['rx1']-P['rx0'],1.0); bh_real=max(P['ry1']-P['ry0'],1.0)
    ratio=bw_real/bh_real
    apix=SCALE_AREA*m['area']
    bw=math.sqrt(apix*ratio)*SHRINK; bh=math.sqrt(apix/ratio)*SHRINK
    if max(bw,bh)>MAX_SIDE:
        s=MAX_SIDE/max(bw,bh); bw*=s; bh*=s
    if min(bw,bh)<MIN_SIDE:
        s=MIN_SIDE/min(bw,bh); bw*=s; bh*=s
    rectsz[key]=(bw,bh)

# 布局：中心从真实地理中心出发，迭代中"推开重叠"的同时"弱回弹到真实中心"，
# 这样既拉开间距/消除重叠，又锁住各省份的相对东西、南北位置（不会再把河南推到上海东边）
pos={}
for key in META:
    bw,bh=rectsz[key]
    pos[key]=(prov[key]['mcx0'], prov[key]['mcy0'], bw, bh)
for _ in range(900):
    moved=False
    ks=list(pos)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            ki,kj=ks[i],ks[j]
            cax,cay,bwa,bha=pos[ki]; cbx,cby,bwb,bhb=pos[kj]
            ox=min(cax+bwa/2,cbx+bwb/2)-max(cax-bwa/2,cbx-bwb/2)
            oy=min(cay+bha/2,cby+bhb/2)-max(cay-bha/2,cby-bhb/2)
            if ox>0 and oy>0:
                ddx=cax-cbx; ddy=cay-cby
                if abs(ddx)>=abs(ddy):
                    s=1 if ddx>=0 else -1
                    sh=(ox/2+0.5)*s
                    pos[ki]=(cax+sh,cay,bwa,bha); pos[kj]=(cbx-sh,cby,bwb,bhb)
                else:
                    s=1 if ddy>=0 else -1
                    sv=(oy/2+0.5)*s
                    pos[ki]=(cax,cay+sv,bwa,bha); pos[kj]=(cbx,cby-sv,bwb,bhb)
                moved=True
    # 弱回弹：每轮把中心轻轻拉回(覆盖后的)真实地理中心，防止长期迭代漂移、锁住中国地理形状
    for key in META:
        cx,cy,bw,bh=pos[key]
        tx,ty=prov[key]['mcx0'],prov[key]['mcy0']
        pos[key]=(cx+(tx-cx)*0.05, cy+(ty-cy)*0.05, bw, bh)
    if not moved: break

# fit 松弛后的布局到地图区（留20px白边）
minx=min(p[0]-p[2]/2 for p in pos.values()); maxx=max(p[0]+p[2]/2 for p in pos.values())
miny=min(p[1]-p[3]/2 for p in pos.values()); maxy=max(p[1]+p[3]/2 for p in pos.values())
FIT=min((MAP_X1-40)/(maxx-minx),(MAP_Y1-40)/(maxy-miny))

DATA=[]
for key in META:
    cx,cy,bw,bh=pos[key]
    m=META[key]; P=prov[key]
    mcx=round(20+(cx-minx)*FIT,1); mcy=round(20+(cy-miny)*FIT,1)
    nbw=round(bw*FIT,1); nbh=round(bh*FIT,1)
    bx=round(mcx-nbw/2,1); by=round(mcy-nbh/2,1)
    hx,hy=home[key]
    fs = 12 if m['area']>=20 else (11 if m['area']>=5 else 9)
    DATA.append({
        'id':key,'name':m['name'],'cap':m['cap'],'abbr':m['abbr'],'alias':m['alias'],'aliasMore':'·'.join(ALIAS_MORE.get(key,[])),'region':REGION[key],
        'emoji':m['emoji'],'feat':m['feat'],'color':m['color'],'area':m['area'],'fs':fs,
        'realD':P['d'],'rcx':round(P['rcx'],1),'rcy':round(P['rcy'],1),
        'rbx':round(P['rx0']-5,1),'rby':round(P['ry0']-5,1),
        'rbw':round((P['rx1']-P['rx0'])+10,1),'rbh':round((P['ry1']-P['ry0'])+10,1),
        'mx':mcx,'my':mcy,'bx':bx,'by':by,'bw':nbw,'bh':nbh,
        'homeX':hx,'homeY':hy,
        'capAlias':'·'.join(CAP_ALIAS.get(key,[])),'capFeat':'·'.join(CAP_FEAT.get(key,[])),
    })
    print('%-4s block=%gx%g center=(%g,%g) home=(%g,%g)  true=(%g,%g)'%(key, nbw, nbh, mcx, mcy, hx, hy, round(P['rcx'],1), round(P['rcy'],1)))

data_js=json.dumps(DATA, ensure_ascii=False)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>地图大比拼</title>
<style>
 *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
 body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;
      background:linear-gradient(160deg,#fff7e6,#ffe3c2);min-height:100vh;color:#5a3e2b;}
 #app{max-width:800px;margin:0 auto;padding:14px 12px 30px;}
 .hidden{display:none!important;}
 #cover{text-align:center;padding:22px 14px 10px;}
 #cover h1{font-size:28px;margin:6px 0;color:#e63946;letter-spacing:2px;text-shadow:0 2px 0 #ffd166;}
 #cover .sub{font-size:13px;color:#a8743a;margin-bottom:6px;}
 #cover .tip{font-size:12px;color:#b0894f;margin-bottom:16px;}
 .diffs{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;}
 .diffcard{width:210px;background:#fff;border-radius:18px;padding:16px 14px;cursor:pointer;
   box-shadow:0 6px 16px rgba(230,57,70,.16);border:3px solid transparent;transition:transform .12s,border-color .12s;}
 .diffcard:hover{transform:translateY(-4px);border-color:#ffd166;}
 .diffcard .ico{font-size:42px;}
 .diffcard h3{margin:8px 0 4px;color:#e63946;font-size:17px;}
 .diffcard p{margin:0;font-size:11.5px;color:#8a6a45;line-height:1.5;}
 header.bar{display:flex;align-items:center;justify-content:space-between;gap:8px;
      background:#fff;border-radius:14px;padding:7px 12px;margin:10px 0;
      box-shadow:0 3px 10px rgba(230,57,70,.12);flex-wrap:wrap;}
 .progress{font-weight:bold;color:#e63946;font-size:14px;}
 .ctrls{display:flex;gap:6px;flex-wrap:wrap;align-items:center;}
 button{font-family:inherit;border:none;border-radius:10px;padding:6px 11px;
        font-size:12.5px;cursor:pointer;background:#ffe0b3;color:#7a4a16;font-weight:bold;transition:transform .1s;}
 button:active{transform:scale(.94);}
 #zoomTxt{min-width:44px;text-align:center;font-size:12px;font-weight:bold;color:#a8743a;}
 #stage{position:relative;width:100%;max-width:760px;margin:0 auto;overflow:auto;
        -webkit-overflow-scrolling:touch;max-height:76vh;border-radius:16px;background:rgba(255,255,255,.35);}
 #spacer{width:760px;height:__VH__px;}
 #zoomLayer{position:absolute;top:0;left:0;width:760px;height:__VH__px;transform-origin:top left;transform:scale(var(--z,1));}
 #gameArea{width:760px;height:__VH__px;display:block;touch-action:none;}
 .slot{fill:none;stroke:#c9a36f;stroke-width:2.2;stroke-dasharray:6 6;pointer-events:none;}
 .slot.lit{stroke:#ffcf4d;stroke-dasharray:0;stroke-width:2.4;}
 .slabel{font-weight:normal;fill:#a07a4a;text-anchor:middle;dominant-baseline:middle;pointer-events:none;}
 .piece path{stroke:rgba(255,255,255,.85);stroke-width:1.2;cursor:grab;fill-opacity:.82;}
 .piece .pshape{stroke:rgba(255,255,255,.85);stroke-width:1.2;cursor:grab;fill-opacity:.82;}
 .piece.done{pointer-events:none;}
 .piece.done path,.piece.done .pshape{fill-opacity:1;cursor:default;filter:drop-shadow(0 0 5px #ffd166);}
 .piece.done .plabel{font-weight:normal;}
 .plabel{font-weight:normal;fill:#fff;text-anchor:middle;dominant-baseline:middle;
         pointer-events:none;paint-order:stroke;stroke:rgba(0,0,0,.4);stroke-width:2.5px;}
 @keyframes bingoA{0%{opacity:0;transform:translateY(8px) scale(.5)}
   15%{opacity:1;transform:translateY(-4px) scale(1.15)}
   100%{opacity:0;transform:translateY(-46px) scale(1)}}
 .bingo{font-weight:900;fill:#e63946;text-anchor:middle;dominant-baseline:middle;pointer-events:none;
        transform-box:fill-box;transform-origin:center;animation:bingoA 1.5s ease-out forwards;}
 @keyframes pop{0%{transform:scale(.7)}60%{transform:scale(1.12)}100%{transform:scale(1)}}
 .mask{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:2000;padding:16px;}
 .mask.show{display:flex;}
 .card{background:#fff;border-radius:20px;padding:20px 24px;max-width:330px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.3);animation:pop .35s;width:100%;}
 .card .big{font-size:44px;}
 .card h2{margin:6px 0;color:#e63946;font-size:20px;}
 .card .row{margin:6px 0;font-size:14px;color:#5a3e2b;}
 .card .row b{color:#e63946;}
 .card button{margin-top:12px;background:#e63946;color:#fff;padding:8px 22px;font-size:14px;border:none;border-radius:10px;cursor:pointer;font-weight:bold;}
 .win .card{background:linear-gradient(160deg,#fff,#fff3d6);}
 .confetti{font-size:24px;letter-spacing:6px;margin-bottom:4px;}
 .timer{font-weight:bold;color:#2a9d8f;font-size:13px;margin-right:8px;}
 .best{font-size:13px;color:#a8743a;margin-top:10px;}
 .modeRow{display:flex;gap:12px;justify-content:center;margin-top:16px;flex-wrap:wrap;}
 .modeBtn{background:#fff;color:#e63946;border:2px solid #ffd166;box-shadow:0 4px 12px rgba(230,57,70,.12);padding:10px 18px;font-size:14px;border-radius:12px;cursor:pointer;font-weight:bold;}
 .modeBtn:hover{background:#fff3d6;}
 /* 分区练习浮层 */
 .regionGrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:14px 0;}
 .regionCard{background:#fff7e6;border:2px solid #ffd166;border-radius:14px;padding:10px 12px;text-align:left;}
 .regionCard.locked{opacity:.55;filter:grayscale(.4);}
 .regionCard .rname{font-weight:bold;color:#e63946;font-size:15px;}
 .regionCard .rprog{font-size:12px;color:#8a6a45;margin:2px 0 6px;}
 .rdiffs{display:flex;gap:6px;}
 .rdiff{font-size:18px;padding:4px 10px;background:#ffe0b3;border:none;border-radius:8px;cursor:pointer;}
 .rdiff:disabled{opacity:.4;cursor:not-allowed;}
 /* 知识问答板块 */
 #quiz{position:relative;width:100%;max-width:820px;margin:0 auto;padding:14px 12px 30px;box-sizing:border-box;}
 .qhead{text-align:center;font-size:13px;color:#a8743a;margin-bottom:12px;}
 .qitem{background:#fff;border-radius:14px;padding:12px 14px;margin-bottom:12px;box-shadow:0 3px 10px rgba(230,57,70,.10);}
 .qnum{display:inline-block;background:#e63946;color:#fff;border-radius:8px;padding:1px 8px;font-size:12px;font-weight:bold;margin-bottom:6px;}
 .qtext{font-size:15px;color:#5a3e2b;font-weight:bold;margin-bottom:8px;}
 .qopts{display:flex;flex-wrap:wrap;gap:8px;}
 .qopt{flex:1;min-width:90px;background:#ffe0b3;color:#7a4a16;padding:8px 6px;font-size:13px;border:none;border-radius:10px;cursor:pointer;}
 .qopt.sel{background:#e63946;color:#fff;}
 .qopt.correct{background:#2a9d8f;color:#fff;}
 .qopt.wrong{background:#e76f51;color:#fff;}
 .qopt:disabled{cursor:default;}
 .qsubmit{text-align:center;margin:6px 0 14px;}
 .qsubmit button{background:#e63946;color:#fff;border:none;padding:9px 26px;font-size:15px;border-radius:12px;cursor:pointer;font-weight:bold;}
 .qresult{text-align:center;margin-top:6px;}
 .scoreBig{font-size:48px;font-weight:900;color:#e63946;}
 .scoreBig span{font-size:20px;}
 .qfeed{font-size:12.5px;color:#2a9d8f;margin-top:6px;padding:5px 9px;background:#eafff7;border-radius:8px;text-align:left;}
 /* 省级行政区数据表 */
 #tableBody{overflow-x:auto;}
 .dtable{width:100%;min-width:560px;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 3px 10px rgba(230,57,70,.10);font-size:13px;}
 .dtable th{background:#ffe0b3;color:#7a4a16;padding:8px 6px;font-size:12px;white-space:nowrap;}
 .dtable td{padding:7px 6px;border-top:1px solid #ffe9cf;text-align:center;color:#5a3e2b;white-space:nowrap;}
 .dtable tr:nth-child(even) td{background:#fffaf2;}
 .plink,.clink{color:#e63946;cursor:pointer;text-decoration:underline;font-weight:bold;}
 .plink:hover,.clink:hover{color:#ff8a5c;}
</style>
</head>
<body>
<div id="app">
 <div id="cover">
   <h1>🗺️ 地图大比拼</h1>
   <div class="sub">拖动省份，拼出大中国！</div>
   <div class="tip">全国 34 省 · 下方托盘取省份，拖到地图对应位置</div>
   <div class="diffs">
     <div class="diffcard" data-diff="monkey">
       <div class="ico">🐒</div><h3>猴子玩的</h3>
       <p>方块地图·按面积与形状·标省份名字<br>最简单，认形状认名字</p>
     </div>
     <div class="diffcard" data-diff="kid">
       <div class="ico">🧒</div><h3>小孩玩的</h3>
       <p>真实省界地图·标省份名字<br>边玩边学 geography</p>
     </div>
     <div class="diffcard" data-diff="dad">
       <div class="ico">🧑</div><h3>爸爸玩的</h3>
       <p>真实省界地图·不标任何文字<br>纯靠眼力， hardest！</p>
     </div>
   </div>
   <div class="modeRow">
     <button id="regionBtn" class="modeBtn">🧩 分区练习</button>
     <button id="quizBtnP" class="modeBtn">📝 问答·小学生</button>
    <button id="quizBtnK" class="modeBtn">📝 问答·幼儿园</button>
    <button id="quizBtnN" class="modeBtn">📝 问答·托儿所</button>
    <button id="tableBtn" class="modeBtn">📋 省级行政区数据表</button>
   </div>
   <div id="coverBest" class="best"></div>
 </div>

 <div id="game" class="hidden">
   <header class="bar">
     <div class="progress">✨ <span id="cnt">0</span> / <span id="total">34</span></div>
    <span id="timer" class="timer">⏱ 00:00</span>
     <div class="ctrls">
       <button id="zoomOut">－</button>
       <span id="zoomTxt">100%</span>
       <button id="zoomIn">＋</button>
       <button id="zoomFit">适应</button>
       <button id="backBtn">← 首页</button>
       <button id="resetBtn">🔄 重来</button>
     </div>
   </header>
   <div id="stage">
     <div id="spacer"></div>
     <div id="zoomLayer"><svg id="gameArea" viewBox="0 0 760 __VH__" preserveAspectRatio="xMidYMid meet"></svg></div>
   </div>
 </div>

 <div class="mask" id="cardMask"><div class="card">
   <div class="big" id="cEmoji">🐼</div><h2 id="cName">北京</h2>
   <div class="row">省会：<b id="cCap">北京</b></div>
   <div class="row">简称：<b id="cAbbr">京</b>　别称：<b id="cAlias">燕京</b></div>
   <div class="row">面积：<b id="cArea">1.64</b> 万km²</div>
   <button id="cClose">知道啦 👍</button>
 </div></div>
 <div class="mask win" id="winMask"><div class="card">
   <div class="confetti">🎉 ✨ 🎊 ✨ 🎉</div>
   <div class="big">🏆</div>
   <h2 id="winTitle">太棒了！你拼出了大中国！</h2>
   <div class="row" id="winSub">全国 34 省全部归位 🗺️</div>
   <div class="row">你就是 <b>中国小达人</b>！</div>
   <div class="row" id="winTime"></div>
   <button id="winClose">再玩一次 🔁</button>
 </div></div>

 <div class="mask" id="regionMask"><div class="card" style="max-width:560px;width:92%">
   <h2>🧩 分区练习</h2>
   <p class="sub" style="font-size:12px;color:#a8743a">选一个大区，拼会一个再解锁下一个～</p>
   <div id="regionGrid" class="regionGrid"></div>
   <button id="regionBack">← 返回</button>
 </div></div>

 <div id="quiz" class="hidden">
   <header class="bar">
     <div class="progress" style="color:#e63946;font-weight:bold">📝 知识问答</div>
     <div class="ctrls">
       <button id="quizRestart">🔄 再测一次</button>
       <button id="quizBack">← 首页</button>
     </div>
   </header>
   <div id="quizBody"></div>
 </div>

 <div id="table" class="hidden">
   <header class="bar">
     <div class="progress" style="color:#e63946;font-weight:bold">📋 省级行政区数据表</div>
     <div class="ctrls"><button id="tableBack">← 首页</button></div>
   </header>
   <div id="tableBody"></div>
 </div>

 <div class="mask" id="infoMask"><div class="card">
   <div class="big" id="infoEmoji">🐼</div>
   <h2 id="infoTitle">简介</h2>
   <div class="row" id="infoBody"></div>
   <button id="infoClose">知道啦 👍</button>
 </div></div>

</div>
<script>
const VH=__VH__;
const DATA = __DATA__;
const DIFFS={
  monkey:{name:'猴子玩的',shape:'block',label:true,thresh:46},
  kid:{name:'小孩玩的',shape:'real',label:true,thresh:34},
  dad:{name:'爸爸玩的',shape:'real',label:false,thresh:34}
};
const SVGNS='http://www.w3.org/2000/svg';
const gameArea=document.getElementById('gameArea');
const cntEl=document.getElementById('cnt');
const cover=document.getElementById('cover');
const game=document.getElementById('game');
const cardMask=document.getElementById('cardMask');
const winMask=document.getElementById('winMask');
const stage=document.getElementById('stage');
const spacer=document.getElementById('spacer');
const zoomTxt=document.getElementById('zoomTxt');
const SAVE_PREFIX='mapBattle_v2_';
const DIFFS_ARR=[{k:'monkey',ico:'🐒'},{k:'kid',ico:'🧒'},{k:'dad',ico:'🧑'}];
const REGION_ORDER=['华北','东北','华东','华中','华南','西南','西北'];
const quizSec=document.getElementById('quiz');
const regionMask=document.getElementById('regionMask');
const regionGrid=document.getElementById('regionGrid');
const quizBody=document.getElementById('quizBody');
const totalEl=document.getElementById('total');
const timerEl=document.getElementById('timer');
const winTimeEl=document.getElementById('winTime');
const winTitleEl=document.getElementById('winTitle');
const winSubEl=document.getElementById('winSub');
const tableSec=document.getElementById('table');
const tableBody=document.getElementById('tableBody');
const infoMask=document.getElementById('infoMask');
const infoEmoji=document.getElementById('infoEmoji');
const infoTitle=document.getElementById('infoTitle');
const infoBody=document.getElementById('infoBody');
const infoClose=document.getElementById('infoClose');
let timerId=null, timerStart=0, timerElapsed=0;
let quizState=null;

function soundWrong(){ beep(196,0.25,'sawtooth',0.15); }

// 存档键（含大区，避免不同模式进度互相串）
function saveKey(){ return SAVE_PREFIX+state.difficulty+'_'+(state.region||'all'); }
function bestKey(){ return SAVE_PREFIX+'best_'+state.difficulty+'_'+(state.region||'all'); }
function fmtTime(s){ s=Math.max(0,Math.floor(s)); return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }

// 大区进度与解锁（以“小孩版”完成度衡量）
function regionProgress(rg){
  const ks=DATA.filter(d=>d.region===rg).map(d=>d.id);
  let done=new Set();
  try{ done=new Set((JSON.parse(localStorage.getItem(SAVE_PREFIX+'kid_'+rg)||'{"done":[]}').done)||[]); }catch(e){}
  return ks.filter(k=>done.has(k)).length;
}
function isRegionUnlocked(idx){
  if(idx===0) return true;
  return localStorage.getItem(SAVE_PREFIX+'regiondone_'+REGION_ORDER[idx-1])==='1';
}

// 计时
function startTimer(){ stopTimer(); timerStart=Date.now(); timerElapsed=0; if(timerEl) timerEl.textContent='⏱ 00:00';
  timerId=setInterval(()=>{ timerElapsed=(Date.now()-timerStart)/1000; if(timerEl) timerEl.textContent='⏱ '+fmtTime(timerElapsed); },500); }
function stopTimer(){ if(timerId){ clearInterval(timerId); timerId=null; } }

// 渲染分区浮层
function renderRegions(){
  if(!regionGrid) return;
  regionGrid.innerHTML='';
  REGION_ORDER.forEach((rg,idx)=>{
    const total=DATA.filter(d=>d.region===rg).length;
    const done=regionProgress(rg);
    const unlocked=isRegionUnlocked(idx);
    const card=document.createElement('div');
    card.className='regionCard'+(unlocked?'':' locked');
    const diffBtns=DIFFS_ARR.map(d=>'<button class="rdiff" data-d="'+d.k+'" '+(unlocked?'':'disabled')+'>'+d.ico+'</button>').join('');
    card.innerHTML='<div class="rname">'+(unlocked?'':'🔒 ')+rg+'</div><div class="rprog">'+(done===total&&total>0?'✅ ':'')+done+' / '+total+'</div><div class="rdiffs">'+diffBtns+'</div>';
    card.querySelectorAll('.rdiff').forEach(b=> b.onclick=()=>{ if(!unlocked) return; regionMask.classList.remove('show'); startGame(b.dataset.d, rg); });
    regionGrid.appendChild(card);
  });
}

// 知识问答
function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
// 托儿所难度用到的主值（取别称/特色串的第一个，避免多值串作为答案）
const capAliasMain=DATA.map(d=>(d.capAlias||d.cap||'').split('·')[0]);
const featAll=[...new Set(DATA.flatMap(d=>(d.feat||'').split('·')))];   // 所有省特色全集(去重)
const capFeatAll=[...new Set(DATA.flatMap(d=>(d.capFeat||d.feat||'').split('·')))]; // 所有省会特色全集(去重)
// 构造一道题：kind 决定题型，pool 是该题选项全集，答案与干扰项各抽2个
function mkQ(p, kind){
  let q, pool, ans;
  if(kind==='A'){ q=p.name+'省 的省会是哪里？'; pool=DATA.map(d=>d.cap); ans=p.cap; }
  else if(kind==='B'){ q=p.cap+' 是哪个省的省会？'; pool=DATA.map(d=>d.name); ans=p.name; }
  else if(kind==='abbrOf'){ q=p.name+' 的简称是什么？'; pool=DATA.map(d=>d.abbr); ans=p.abbr; }
  else if(kind==='abbrToProv'){ q=p.abbr+' 是哪个省份的简称？'; pool=DATA.map(d=>d.name); ans=p.name; }
  else if(kind==='aliasOf'){ q=p.name+' 的别称是什么？'; pool=DATA.map(d=>d.alias); ans=p.alias; }
  else if(kind==='aliasToProv'){ q=p.alias+' 是哪个省份的别称？'; pool=DATA.map(d=>d.name); ans=p.name; }
  else if(kind==='capAliasOf'){ q=p.cap+' 的别称是什么？'; pool=capAliasMain; ans=(p.capAlias||p.cap).split('·')[0]; }
  else if(kind==='capAliasToCity'){ const a=(p.capAlias||p.cap).split('·')[0]; q=a+' 是哪个省会城市的别称？'; pool=DATA.map(d=>d.cap); ans=p.cap; }
  else if(kind==='provFeatOf'){ const feats=p.feat.split('·'); ans=feats[Math.floor(Math.random()*feats.length)]; q=p.name+' 的特色是？'; pool=featAll; }
  else if(kind==='capFeatOf'){ const feats=(p.capFeat||p.feat).split('·'); ans=feats[Math.floor(Math.random()*feats.length)]; q=p.cap+' 的特色是？'; pool=capFeatAll; }
  pool=[...new Set(pool)];
  const opts=shuffle([ans].concat(shuffle(pool.filter(x=>x!==ans)).slice(0,2)));
  return {q, opts, ans};
}
function openQuiz(level){
  stopTimer();
  cover.classList.add('hidden'); game.classList.add('hidden'); quizSec.classList.remove('hidden');
  // 小学生：仅 A(省→省会)/B(城市→省)；幼儿园：额外混入简称、别称混合题
  const kinds = level==='kinder'
    ? ['A','abbrOf','abbrToProv','aliasOf','aliasToProv','B']
    : level==='nursery'
    ? ['A','B','capAliasOf','capAliasToCity','provFeatOf','capFeatOf']
    : ['A','B'];
  const qs=[]; const used=new Set(); let guard=0;
  while(qs.length<20 && guard<1000){
    guard++;
    const p=DATA[Math.floor(Math.random()*DATA.length)];
    if(used.has(p.id)) continue;            // 去重：同一省份只在全部题型中出现一次
    const kind = level==='primary' ? (qs.length%2===0?'A':'B') : kinds[Math.floor(Math.random()*kinds.length)];
    qs.push(mkQ(p, kind)); used.add(p.id);
  }
  quizState={qs:qs, ans:new Array(qs.length).fill(null), graded:false, level:level, idx:0};
  renderQuiz();
}
function renderQuiz(){
  if(!quizBody) return;
  const qtitle = quizState.level==='kinder' ? '📝 知识问答·幼儿园难度' : quizState.level==='nursery' ? '📝 知识问答·托儿所难度' : '📝 知识问答·小学生难度';
  const i=quizState.idx, q=quizState.qs[i], last=(i===quizState.qs.length-1);
  let h='<div class="qhead">'+qtitle+' · 第 '+(i+1)+' / '+quizState.qs.length+' 题</div>';
  h+='<div class="qitem"><div class="qnum">Q'+(i+1)+'</div><div class="qtext">'+q.q+'</div><div class="qopts">';
  q.opts.forEach(o=>{ const sel=quizState.ans[i]===o?' sel':''; h+='<button class="qopt'+sel+'" data-o="'+o+'">'+o+'</button>'; });
  h+='</div></div>';
  h+='<div class="qsubmit"><button id="quizNext">'+(last?'查看得分 📊':'下一题 →')+'</button></div>';
  quizBody.innerHTML=h;
  quizBody.querySelectorAll('.qopt').forEach(b=> b.onclick=()=>{ if(quizState.graded) return; quizState.ans[i]=b.dataset.o; renderQuiz(); });
  const nb=document.getElementById('quizNext');
  if(nb) nb.onclick=()=>{ if(quizState.graded) return; if(last) gradeQuiz(); else { quizState.idx++; renderQuiz(); } };
}
function gradeQuiz(){
  quizState.graded=true;
  let score=0;
  quizState.qs.forEach((q,i)=>{ if(quizState.ans[i]===q.ans) score+=Math.round(100/quizState.qs.length); });
  const qtitle = quizState.level==='kinder' ? '📝 知识问答·幼儿园难度' : quizState.level==='nursery' ? '📝 知识问答·托儿所难度' : '📝 知识问答·小学生难度';
  let h='<div class="qhead">'+qtitle+' · 你的得分</div>';
  h+='<div class="qresult" style="text-align:center;margin:4px 0 16px"><div class="scoreBig">'+score+'<span>分</span></div>'+(score===100?'🏆 满分小达人！':score>=60?'👍 不错哦，继续加油！':'💪 多练几次就熟啦～')+'</div>';
  quizState.qs.forEach((q,i)=>{
    const user=quizState.ans[i], ok=user===q.ans;
    h+='<div class="qitem"><div class="qnum">Q'+(i+1)+'</div><div class="qtext">'+q.q+'</div><div class="qopts">';
    q.opts.forEach(o=>{
      let cls='qopt';
      if(o===q.ans) cls+=' correct';
      else if(o===user) cls+=' wrong';
      h+='<button class="'+cls+'" disabled>'+o+'</button>';
    });
    h+='</div>';
    if(!ok) h+='<div class="qfeed">✅ 正确答案：'+q.ans+(user?'　你选了：'+user:'　（这题没选哦）')+'</div>';
    h+='</div>';
  });
  h+='<div class="qsubmit"><button id="quizNext">🔄 再测一次</button></div>';
  quizBody.innerHTML=h;
  const nb=document.getElementById('quizNext'); if(nb) nb.onclick=()=>openQuiz(quizState.level);
  if(score===100) soundWin(); else if(score<60) soundWrong();
}
function provIntro(d){
  return '简称 <b>'+d.abbr+'</b>　省名别称 <b>'+d.alias+(d.aliasMore?('·'+d.aliasMore):'')+'</b><br>省会：<b>'+d.cap+'</b>'+(d.capAlias?('　省会别称 <b>'+d.capAlias+'</b>'):'')+'<br>面积约 <b>'+d.area+'</b> 万km²<br>特色：'+d.feat;
}
function cityIntro(d){
  return '<b>'+d.cap+'</b> 是 <b>'+d.name+'</b> 的省会'+(d.capAlias?('　别称 <b>'+d.capAlias+'</b>'):'')+'<br>特色：'+d.feat;
}
function showInfo(emoji, title, body){
  if(infoEmoji) infoEmoji.textContent=emoji;
  if(infoTitle) infoTitle.textContent=title;
  if(infoBody) infoBody.innerHTML=body;
  if(infoMask) infoMask.classList.add('show');
}
function renderTable(){
  if(!tableBody) return;
  let h='<table class="dtable"><thead><tr><th>省份</th><th>简称</th><th>省名别称</th><th>省会</th><th>省会别称</th><th>面积(万km²)</th><th>特色</th></tr></thead><tbody>';
  DATA.forEach(d=>{
    const aMore = d.alias + (d.aliasMore?('·'+d.aliasMore):'');
    h+='<tr><td><a class="plink" data-id="'+d.id+'">'+d.name+'</a></td>'+
       '<td>'+d.abbr+'</td><td>'+aMore+'</td>'+
       '<td><a class="clink" data-id="'+d.id+'">'+d.cap+'</a></td>'+
       '<td>'+(d.capAlias||'—')+'</td>'+
       '<td>'+d.area+'</td><td>'+d.feat+'</td></tr>';
  });
  h+='</tbody></table>';
  tableBody.innerHTML=h;
  tableBody.querySelectorAll('.plink').forEach(a=> a.onclick=()=>{ const d=DATA.find(x=>x.id===a.dataset.id); showInfo(d.emoji, d.name, provIntro(d)); });
  tableBody.querySelectorAll('.clink').forEach(a=> a.onclick=()=>{ const d=DATA.find(x=>x.id===a.dataset.id); showInfo('🏙️', d.cap, cityIntro(d)); });
}
function refreshCoverBest(){
  const el=document.getElementById('coverBest');
  if(!el) return;
  const best=parseFloat(localStorage.getItem(SAVE_PREFIX+'best_kid_all'));
  el.textContent = isNaN(best)?'🏆 还没记录最佳用时，快来挑战！':'🏆 全国最佳（小孩版）：'+fmtTime(best);
}
refreshCoverBest();   // 版本隔离，避免旧存档串号
let state={difficulty:'kid', region:null};
let pieces=[];
let dragging=null,startX=0,startY=0,startTx=0,startTy=0;
let zoom=1;

let audioCtx=null;
function ac(){ if(!audioCtx) audioCtx=new (window.AudioContext||window.webkitAudioContext)(); if(audioCtx.state==='suspended') audioCtx.resume(); return audioCtx; }
function beep(f,dur,type,vol){ const c=ac(); const o=c.createOscillator(); const g=c.createGain(); o.type=type||'sine'; o.frequency.value=f; g.gain.value=vol||0.18; o.connect(g); g.connect(c.destination); o.start(); g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+dur); o.stop(c.currentTime+dur); }
function soundBingo(){ beep(988,0.10,'sine',0.2); setTimeout(()=>beep(1319,0.16,'triangle',0.2),110); }
function soundWin(){ [523,659,784,1047].forEach((f,i)=>setTimeout(()=>beep(f,0.22,'triangle',0.2),i*130)); }

function setZoom(z){
  zoom=Math.max(0.5,Math.min(2.6,z));
  stage.style.setProperty('--z',zoom);
  spacer.style.width=(760*zoom)+'px';
  spacer.style.height=(VH*zoom)+'px';
  zoomTxt.textContent=Math.round(zoom*100)+'%';
}
document.getElementById('zoomIn').onclick=()=>setZoom(zoom+0.15);
document.getElementById('zoomOut').onclick=()=>setZoom(zoom-0.15);
document.getElementById('zoomFit').onclick=()=>{ const z=Math.min((stage.clientWidth||760)/760,(window.innerHeight*0.7)/VH); setZoom(z); };

function loadSave(){ try{ return JSON.parse(localStorage.getItem(saveKey()))||{done:[]}; }catch(e){ return {done:[]}; } }
function save(){ const done=pieces.filter(p=>p.done).map(p=>p.id); localStorage.setItem(saveKey(),JSON.stringify({done})); }

function render(){
  const diff=DIFFS[state.difficulty];
  const shape=diff.shape, label=diff.label;
  let html='';
  pieces.forEach(p=>{
    if(shape==='block'){
      html+='<rect class="slot" x="'+p.bx+'" y="'+p.by+'" width="'+p.bw+'" height="'+p.bh+'" rx="8"/>';
    }else{
      html+='<path class="slot" d="'+p.realD+'"/>';
    }
    if(label){
      const cx=shape==='block'?(p.bx+p.bw/2):p.rcx;
      const cy=shape==='block'?(p.by+p.bh/2):p.rcy;
      html+='<text class="slabel" style="font-size:'+p.fs+'" x="'+cx+'" y="'+cy+'">'+p.name+'</text>';
    }
  });
  // 已完成的省份先画（沉到最底层），未完成的后画（在最上层，方便拖动）
  const order=[...pieces].sort((a,b)=>(a.done?0:1)-(b.done?0:1));
  order.forEach(p=>{
    const dc=p.done?' done':'';
    const cx0=shape==='block'?p.mx:p.rcx;
    const cy0=shape==='block'?p.my:p.rcy;
    const tx=p.done?0:Math.round(p.homeX-cx0,1);
    const ty=p.done?0:Math.round(p.homeY-cy0,1);
    p.tx=tx; p.ty=ty;
    let inner,cx,cy;
    if(shape==='block'){
      inner='<rect class="pshape" x="'+p.bx+'" y="'+p.by+'" width="'+p.bw+'" height="'+p.bh+'" rx="8" fill="'+p.color+'"/>';
      cx=p.bx+p.bw/2; cy=p.by+p.bh/2;
    }else{
      inner='<rect x="'+p.rbx+'" y="'+p.rby+'" width="'+p.rbw+'" height="'+p.rbh+'" fill="transparent"/><path d="'+p.realD+'" fill="'+p.color+'" fill-rule="evenodd"/>';
      cx=p.rcx; cy=p.rcy;
    }
    const txt=label?'<text class="plabel" style="font-size:'+p.fs+'" x="'+cx+'" y="'+cy+'">'+p.name+'</text>':'';
    html+='<g class="piece'+dc+'" transform="translate('+tx+','+ty+')">'+inner+txt+'</g>';
  });
  gameArea.innerHTML=html;
  const els=[...gameArea.querySelectorAll('.piece')];
  order.forEach((p,i)=>{ p.el=els[i]; bind(p); });
  updateCnt();
}
function bind(p){
  p.el.addEventListener('pointerdown',e=>onDown(e,p));
  p.el.addEventListener('pointermove',e=>onMove(e));
  p.el.addEventListener('pointerup',e=>onUp(e));
}
function svgScale(){ return gameArea.getBoundingClientRect().width/760; }
function onDown(e,p){
  if(p.done||!e.isPrimary) return; ac();
  dragging=p; startX=e.clientX; startY=e.clientY; startTx=p.tx; startTy=p.ty;
  p.el.setPointerCapture(e.pointerId); e.preventDefault();
}
function onMove(e){
  if(!dragging) return;
  const s=svgScale();
  dragging.tx=startTx+(e.clientX-startX)/s;
  dragging.ty=startTy+(e.clientY-startY)/s;
  dragging.el.setAttribute('transform','translate('+dragging.tx+','+dragging.ty+')');
}
function onUp(e){
  if(!dragging) return;
  const p=dragging; dragging=null;
  if(Math.hypot(p.tx,p.ty)<DIFFS[state.difficulty].thresh) snap(p,true);
}
function showBingo(cx,cy){
  const t=document.createElementNS(SVGNS,'text');
  t.setAttribute('x',cx); t.setAttribute('y',cy);
  t.setAttribute('class','bingo'); t.setAttribute('style','font-size:26px');
  t.textContent='🎉BINGO';
  gameArea.appendChild(t);
  setTimeout(()=>{ if(t.parentNode) t.parentNode.removeChild(t); },1500);
}
function snap(p,showCard){
  p.done=true; p.tx=0; p.ty=0;
  p.el.setAttribute('transform','translate(0,0)');
  p.el.classList.add('done');
  const i=pieces.findIndex(x=>x.id===p.id);
  const slot=gameArea.querySelectorAll('.slot')[i];
  if(slot) slot.classList.add('lit');
  const diff=DIFFS[state.difficulty];
  const cx=diff.shape==='block'?p.mx:p.rcx;
  const cy=diff.shape==='block'?p.my:p.rcy;
  showBingo(cx,cy); soundBingo();
  // 放置成功后沉到最底层（移到所有省份碎片之前），避免遮挡后续碎片
  const first=gameArea.querySelector('.piece');
  if(first && first!==p.el) gameArea.insertBefore(p.el, first);
  updateCnt(); save();
  if(showCard) showCard(p);
  if(pieces.every(x=>x.done)) setTimeout(showWin,700);
}
function updateCnt(){ cntEl.textContent=pieces.filter(p=>p.done).length; if(totalEl) totalEl.textContent=pieces.length; }
function showCard(p){
  document.getElementById('cEmoji').textContent=p.emoji;
  document.getElementById('cName').textContent=p.name;
  document.getElementById('cCap').textContent=p.cap;
  document.getElementById('cAbbr').textContent=p.abbr;
  document.getElementById('cAlias').textContent=p.alias;
  document.getElementById('cArea').textContent=p.area;
  cardMask.classList.add('show');
}
document.getElementById('cClose').onclick=()=>cardMask.classList.remove('show');
function showWin(){
  soundWin(); stopTimer();
  if(state.region) localStorage.setItem(SAVE_PREFIX+'regiondone_'+state.region,'1');
  const sec=timerElapsed;
  const prev=parseFloat(localStorage.getItem(bestKey()));
  let bestTxt='';
  if(isNaN(prev) || sec<prev){ localStorage.setItem(bestKey(), sec.toFixed(1)); bestTxt='🏆 新纪录！'; }
  else bestTxt='最佳 '+fmtTime(prev);
  if(winTimeEl) winTimeEl.textContent='⏱ 用时 '+fmtTime(sec)+'　'+bestTxt;
  if(winSubEl) winSubEl.textContent = state.region ? (state.region+' '+pieces.length+' 省全部归位 🗺️') : '全国 34 省全部归位 🗺️';
  winMask.classList.add('show');
}
document.getElementById('winClose').onclick=()=>winMask.classList.remove('show');

document.getElementById('resetBtn').onclick=()=>{
  localStorage.removeItem(saveKey());
  pieces.forEach(p=>{ p.done=false; });
  render(); startTimer();
};
function applySaved(sv){
  pieces.forEach(p=>{
    if(sv&&sv.done&&sv.done.includes(p.id)){ p.done=true; p.tx=0; p.ty=0; }
    else { p.done=false; }
  });
}
// 待选省份混乱布局：在底部托盘随机网格散布（不按原地理顺序），分区游戏时自然集中
function shuffleHome(ps){
  const n=ps.length; if(!n) return;
  const cols=Math.min(n, Math.max(3, Math.ceil(Math.sqrt(n*1.8))));
  const rows=Math.ceil(n/cols);
  const x0=40, x1=720, y0=VH-310, y1=VH-16;
  const cw=(x1-x0)/cols, ch=(y1-y0)/rows;
  const order=shuffle([...Array(n).keys()]);
  ps.forEach((p,k)=>{
    const g=order[k], gc=g%cols, gr=Math.floor(g/cols);
    const jx=(Math.random()-0.5)*cw*0.42, jy=(Math.random()-0.5)*ch*0.42;
    p.homeX=Math.round(x0+cw*(gc+0.5)+jx);
    p.homeY=Math.round(y0+ch*(gr+0.5)+jy);
  });
}
function startGame(diff, region){
  state.difficulty=diff; state.region=region||null;
  const pool = state.region ? DATA.filter(d=>d.region===state.region) : DATA;
  pieces=pool.map(d=>({...d, done:false, el:null}));
  shuffleHome(pieces);
  applySaved(loadSave());
  cover.classList.add('hidden'); game.classList.remove('hidden'); quizSec.classList.add('hidden');
  if(winTitleEl) winTitleEl.textContent = state.region ? (state.region+' 拼好啦！') : '太棒了！你拼出了大中国！';
  render();
  requestAnimationFrame(()=>{
    const w=stage.clientWidth||760;
    setZoom(Math.min(w/760, 0.7));   // 默认横向铺满，最大0.7，向下滚动取省份
    window.scrollTo(0,0);
  });
  startTimer();
}
function backToCover(){
  stopTimer(); save();
  game.classList.add('hidden'); quizSec.classList.add('hidden');
  cover.classList.remove('hidden'); refreshCoverBest();
}
document.querySelectorAll('.diffcard').forEach(b=> b.onclick=()=>startGame(b.dataset.diff, null));
document.getElementById('backBtn').onclick=backToCover;
document.getElementById('regionBtn').onclick=()=>{ regionMask.classList.add('show'); renderRegions(); };
document.getElementById('regionBack').onclick=()=>regionMask.classList.remove('show');
document.getElementById('quizBtnP').onclick=()=>openQuiz('primary');
document.getElementById('quizBtnK').onclick=()=>openQuiz('kinder');
document.getElementById('quizBtnN').onclick=()=>openQuiz('nursery');
document.getElementById('quizBack').onclick=()=>{ quizSec.classList.add('hidden'); cover.classList.remove('hidden'); refreshCoverBest(); };
document.getElementById('quizRestart').onclick=()=>openQuiz(quizState.level);
document.getElementById('tableBtn').onclick=()=>{ cover.classList.add('hidden'); tableSec.classList.remove('hidden'); renderTable(); };
document.getElementById('tableBack').onclick=()=>{ tableSec.classList.add('hidden'); cover.classList.remove('hidden'); refreshCoverBest(); };
document.getElementById('infoClose').onclick=()=>infoMask.classList.remove('show');
infoMask.addEventListener('click', e=>{ if(e.target===infoMask) infoMask.classList.remove('show'); });

// PC 滚轮缩放（Ctrl+滚轮也支持触控板捏合，浏览器会带 ctrlKey）
stage.addEventListener('wheel', e=>{
  e.preventDefault();
  setZoom(zoom + (e.deltaY<0?0.12:-0.12));
}, {passive:false});
// 手机双指捏合缩放
let pinchDist=0;
function tdist(t){ return Math.hypot(t[0].clientX-t[1].clientX, t[0].clientY-t[1].clientY); }
stage.addEventListener('touchstart', e=>{ if(e.touches.length===2){ dragging=null; panning=null; pinchDist=tdist(e.touches); } }, {passive:false});
stage.addEventListener('touchmove', e=>{
  if(e.touches.length===2){
    e.preventDefault();
    const d=tdist(e.touches);
    if(pinchDist>0) setZoom(zoom*(d/pinchDist));
    pinchDist=d;
  }
}, {passive:false});
stage.addEventListener('touchend', e=>{ if(e.touches.length<2) pinchDist=0; });
// 拖拽空白处平移画面：PC 左键拖 / 手机单指拖（点到省份则交给拖省份逻辑）
let panning=null;
stage.addEventListener('pointerdown', e=>{
  if(e.pointerType==='mouse' && e.button!==0) return;
  if(e.target.closest('.piece')) return;
  panning={x:e.clientX, y:e.clientY, sl:stage.scrollLeft, st:stage.scrollTop};
});
stage.addEventListener('pointermove', e=>{
  if(!panning) return;
  stage.scrollLeft = panning.sl - (e.clientX-panning.x);
  stage.scrollTop  = panning.st - (e.clientY-panning.y);
});
stage.addEventListener('pointerup', ()=> panning=null);
stage.addEventListener('pointercancel', ()=> panning=null);

pieces=[];
</script>
</body></html>'''

html=TEMPLATE.replace('__DATA__', data_js).replace('__VH__', str(VH))
with open('/sandbox/workspace/map_battle.html','w',encoding='utf-8') as f:
    f.write(html)
print('OK wrote', len(html), 'bytes; VH=', VH, '; provinces=', len(DATA), '; SCALE=%.3f SHRINK=%.2f FIT=%.3f'%(SCALE,SHRINK,FIT))
