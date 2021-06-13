import moduleSecurity2 as ModuleSecurity

_decompress = ModuleSecurity.Decompress()

hello = '110|86|48|111|76|118|95|103|115|52|72|57|98|86|109|119|99|82|79|57|52|55|97|51|80|73|118|90|86|50|81|36|119|101|99|104|97|116|35|97|110|100|114|111|105|100|64|49|52|48|55|0|0|144|28|0|120|50|10|255|227|131|252|64|0|133|209|194|192|120|109|93|151|81|6|171|113|251|146|161|48|148|115|192|145|81|130|64|0|1|234|0|159|140|120|0'
hello = '160|80|7|2|96|16|160|16|198|85|151|151|43|227|53|89|56|157|100|221|203|224|1|248|128|31|17|142|153|64|183|51|92|37|252|125|87|135|143|197|0|30|236|20|207|103|86|110|3|215|13|50|4|0|60|26|1|13|30|114|244|35|28|50|0|125|54|32|68|113|4|2|249|143|14|1|193|130|12|113|204|160|35|200|51|120|0'
oinList = hello.split('|')
print('数据：', oinList)
print('长度：', len(oinList))
oinBytes = bytes('', 'utf-8')
for v in oinList:
    oinBytes += int(v).to_bytes(1, 'big')
resdata = _decompress.update(oinBytes)
print('====', len(resdata))
print('|'.join([str(v) for v in resdata]))
print('|'.join([hex(v) for v in resdata]))