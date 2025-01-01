import sys 

# 字体路径
sys_name = sys.platform
if sys_name.startswith('win32') or sys_name.startwith('cygwin'):
    print('windows 系统')
    font_path = "C:\\Windows\\Fonts\\" # win 10 路径
elif sys_name.startswith('linux'):
    print('linux系统')
    font_path = "/usr/share/fonts/" # linux 路径
    
elif sys_name.startswith('darwin'):
    print('Mac OS X 系统')
    font_path = "/System/Library/Fonts/" # mac 路径
else:
    print(f'未知系统: {sys_name}')
    sys.exit(1)

font_path += 'simfang.ttf'
print(f'当前系统 {sys_name=}, 字体路径 {font_path=}')

# 快捷回复
response_info = {
    "印刷体.pdf": {
        "merge_image":"all.jpg",
        "content":"""以色列在叙利亚的军事行动
时间：当地时间2024 年12 月9 日
事件概述：以色列在叙利亚采取了军事行动，美国国务院发言人马修·米勒在简报会上表示，
以色列称这些行动是为了保卫其边界，是应对叙利亚军队从该地区撤离而采取的“临时措施”，
并非永久性行动。
Military News
Washington D.C., Recent - The United States Department of Defense has announced the successful
completion of a joint military exercise with allies in the Pacific region. Dubbed "Pacific Resolve 2023," the
exercise took place from mid-November to late December and involved thousands of troops from the
U.S., Australia, Japan, South Korea, and other partner nations.
The primary objective of "Pacific Resolve 2023" was to enhance interoperability and strengthen the
collective defense capabilities of participating nations in response to regional security challenges.
【軍事ニュース】
東京、先日発表- 日本防衛省は、最近、国際連合（ＵＮ）の旗の下で、中東地域で行われた多国間軍事
演習「明るみの盾２０２３」に、日本の自衛隊が参加したことを発表した。この演習は、２０２３年１
１月初旬から中旬にかけて行われ、主に沙漠戦闘の訓練と人道支援活動の模擬を含む多様な課題を取り
上げた。
「明るみの盾２０２３」の主な目的は、参加国間の相互理解と信頼を深め、地域の安定と平和を維持す
るための共同防御能力を強化することだった。日本自衛隊は、地上作戦、航空偵察、医療救急などの分
野で、他国の軍隊と緊密に連携し、高度な戦術運用能力を発揮した。
【Nouvelles Militaires Réelles】
Paris, hier - Le Ministère français de la Défense a annoncé que des troupes françaises ont participé
récemment à une importante exercice militaire multinationale dans la région du Balkans. Cet exercice,
baptisé "Alliance Shield 2023", s'est déroulé du 1er novembre au 15 novembre et a impliqué plus d'une
dizaine de pays européens et asiatiques.
L'objectif principal de "Alliance Shield 2023" était d'améliorer la coordination et la coopération tactique
entre les forces armées participantes.
【Militärische Nachrichten】
Berlin, gestern veröffentlicht - Die deutsche Bundeswehr hat bekannt gegeben, dass sie in Kooperation
mit Partnerländern der NATO und anderer Internationaler Militärallianzen erfolgreich eine
Multinationalen Militärübung abschlossen hat. Die Übung, die den Namen "Trident Javelin" trägt, fand
von dem 15. bis dem 30. Oktober in Norddeutschland und in der baltischen See statt.
Ziel der Übung war die Verbesserung der Kooperationsfähigkeit und der taktischen Koordinierung
zwischen die teilnehmenden Streitkräfte. Besonders hervorgehoben wurden die Fähigkeiten der
Luftverteidigung, der Seeverteidigung und der landbasierter Kampfkräfte."""
    },
    "all_hand.png": {
        "merge_image": "all_hand.png",
        "content": """[语种]ch
[得分]0.8730145410487526

以军越过军事缓冲区，坦克向叙利亚首都
挺近。俄驻叙军事基地处于高度战备状奋

[语种]en
[得分]0.7894557019074758

Fortunately there will be a speech gien by a professor
Smith frm a fomus uniersity. Aiming to compore the
difference and the Simularity between China ond America Mr.S
will answer the question in patience and take the speech seniusy

[语种]japan
[得分]0.7636239142485068

も達法者の仕はご遺体を調べをし正確方
死因をだしまをえにラくニヒぞすもちろんえこには
北人の愛雨や気持なんて考がやていませんご遠体を前にしてあるの
はただををたという取り通しのつかかいだけてす


[语种]fr
[得分]0.7783048874453494

Ce dormeur du vad
CtrthurRimbaud(1854-1891)
C'estun trou de verdure ou chante une riviere
Ctccroctant follement awx herbes des haillons

[语种]de
[得分]0.7783048874453494

Du frische junge diel so ikend wiv der Mat.
nun iot der Herbst gekonmen und alles ist vorkei.
Mr einmal konnt'ick wakrhaft dieken
es war das erste Mal."""
    },
    "兵役法.docx":{
        "merge_image":"word.jpg",
        "content":"""

# 中华人民共和国兵役法

> 1984年5月31日第六届全国人民代表大会第二次会议通过　
> 根据1998年12月29日第九届全国人民代表大会常务委员会第六次会议《关于修改〈中华人民共和国兵役法〉的决定》第一次修正　
> 根据2009年8月27日第十一届全国人民代表大会常务委员会第十次会议《关于修改部分法律的决定》第二次修正　
> 根据2011年10月29日第十一届全国人民代表大会常务委员会第二十三次会议《关于修改〈中华人民共和国兵役法〉的决定》第三次修正　2021年8月20日第十三届全国人民代表大会常务委员会第三十次会议修订

目　　录
- 第一章　总　　则
- 第二章　兵役登记
- 第三章　平时征集
- 第四章　士兵的现役和预备役
- 第五章　军官的现役和预备役
- 第六章　军队院校从青年学生中招收的学员
- 第七章　战时兵员动员
- 第八章　服役待遇和抚恤优待
- 第九章　退役军人的安置
- 第十章　法律责任
- 第十一章　附　　则

## 第一章　总　　则

- 第一条　为了规范和加强国家兵役工作，保证公民依法服兵役，保障军队兵员补充和储备，建设巩固国防和强大军队，根据宪法，制定本法。
- 第二条　保卫祖国、抵抗侵略是中华人民共和国每一个公民的神圣职责。
- 第三条　中华人民共和国实行以志愿兵役为主体的志愿兵役与义务兵役相结合的兵役制度。
- 第四条　兵役工作坚持中国共产党的领导，贯彻习近平强军思想，贯彻新时代军事战略方针，坚持与国家经济社会发展相协调，坚持与国防和军队建设相适应，遵循服从国防需要、聚焦备战打仗、彰显服役光荣、体现权利和义务一致的原则。
- 第五条　中华人民共和国公民，不分民族、种族、职业、家庭出身、宗教信仰和教育程度，都有义务依照本法的规定服兵役。有严重生理缺陷或者严重残疾不适合服兵役的公民，免服兵役。依照法律被剥夺政治权利的公民，不得服兵役。
- 第六条　兵役分为现役和预备役。在中国人民解放军服现役的称军人；预编到现役部队或者编入预备役部队服预备役的，称预备役人员。
- 第七条　军人和预备役人员，必须遵守宪法和法律，履行公民的义务，同时享有公民的权利；由于服兵役而产生的权利和义务，由本法和其他相关法律法规规定。
- 第八条　军人必须遵守军队的条令和条例，忠于职守，随时为保卫祖国而战斗。
  - 预备役人员必须按照规定参加军事训练、担负战备勤务、执行非战争军事行动任务，随时准备应召参战，保卫祖国。
  - 军人和预备役人员入役时应当依法进行服役宣誓。
- 第九条　全国的兵役工作，在国务院、中央军事委员会领导下，由国防部负责。
  - 省军区(卫戍区、警备区)、军分区(警备区)和县、自治县、不设区的市、市辖区的人民武装部，兼各该级人民政府的兵役机关，在上级军事机关和同级人民政府领导下，负责办理本行政区域的兵役工作。
  - 机关、团体、企业事业组织和乡、民族乡、镇的人民政府，依照本法的规定完成兵役工作任务。兵役工作业务，在设有人民武装部的单位，由人民武装部办理；不设人民武装部的单位，确定一个部门办理。普通高等学校应当有负责兵役工作的机构。
- 第十条　县级以上地方人民政府兵役机关应当会同相关部门，加强对本行政区域内兵役工作的组织协调和监督检查。
  - 县级以上地方人民政府和同级军事机关应当将兵役工作情况作为拥军优属、拥政爱民评比和有关单位及其负责人考核评价的内容。
- 第十一条　国家加强兵役工作信息化建设，采取有效措施实现有关部门之间信息共享，推进兵役信息收集、处理、传输、存储等技术的现代化，为提高兵役工作质量效益提供支持。
  - 兵役工作有关部门及其工作人员应当对收集的个人信息严格保密，不得泄露或者向他人非法提供。
- 第十二条　国家采取措施，加强兵役宣传教育，增强公民依法服兵役意识，营造服役光荣的良好社会氛围。
- 第十三条　军人和预备役人员建立功勋的，按照国家和军队关于功勋荣誉表彰的规定予以褒奖。
  - 组织和个人在兵役工作中作出突出贡献的，按照国家和军队有关规定予以表彰和奖励。

## 第二章　兵役登记

- 第十四条　国家实行兵役登记制度。兵役登记包括初次兵役登记和预备役登记。

## 第十一章　附　　则

- 第六十四条　本法适用于中国人民武装警察部队。
- 第六十五条　本法自2021年10月1日起施行。

"""
    }
}