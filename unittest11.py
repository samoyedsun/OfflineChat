import moduleSecurity as ModuleSecurity

strdata = '53 c3 38 91 7b 96 5c 0c f4 de 60 7a 45 62 bd 6d'
strlist = strdata.split(' ')
serverKey = bytes('', 'utf-8')
for ele in strlist:
    serverKey += int(ele, 16).to_bytes(1, 'big')
mToken = '46_7LS_QihDWQCf14nfbVVLTqr6xiL0pz8luZGoop2nWobXqEjmoySKfKBZeYf0q2bgc1hCouzJuIF9ulae7vri2FRrJzwMnDs7FLc9z4Lx09o$desktop_m_wx-10040714-android-10040714-wx-wx5450e72520b1f41e-oLv_gs4H9bVmwcRO947a3PIvZV2Q$c0a46adc25d09eb8bf20cffb1f2534d3$android_wechat'
mAccount = 'oLv_gs4H9bVmwcRO947a3PIvZV2Q$wechat#android@1407'

mhzxSecurityObjToServer = ModuleSecurity.MhzxSecurity(mAccount, mToken, serverKey)
strdata = '6f0082d345e4a9a82c3b670d7cebc798686d1107e10cb9'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToServer.decryption(strreal)
clientKey = bytes('', 'utf-8')
for i in range(3, len(uncodes) - 4):
    clientKey += uncodes[i].to_bytes(1, 'big')
print(len(clientKey))

mhzxSecurityObjToClient = ModuleSecurity.MhzxSecurity(mAccount, mToken, clientKey)
strdata = '685330d601361ddd45f388ddf04901c35e3afb2e77e6fee8cab4c196d607ab43d19e47fa68ddcb9c668106f8a11daffb6d70434bf0adac72f6a00ecea06ab4ba97fbc160f7fe846ae7277a40f49151a6328c755d'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toClient:', uncodedData)

strdata = '89e190f2612dee1913789942'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toClient:', uncodedData)

strdata = '03189458bc38e7aeac942e1080'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToServer.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toServer:', uncodedData)

strdata = '651b115997edb5a996dc94bf1733b1a078ea1b1de8d220f3bfbe1c79abf6fb2c8934fa60e90cb14432abbaeb05fc8cd6b020d3f9bb22c986e511143caf804f8985c0ca8397d9c7436074219c2891a1a6e37456baf908bcbf293ba561614ea75404ed8ec201bc3b18bd69dc225f87a96310ef70f4d39bf6d1c0554ce799a2cef425a55196ee4fb20f0ed7faab175e07cb5fce022d5345b25a4cd6b50c05fbf5aa22a93a7c7206dc507bd48fa6a8f9279c3fa219cb1155322005ac51ad1c5081bdf6c3088862d9df674334f2e2f1ab97e00ac562269ec5f790766b65eceb27188223b959a098e454947a2b7203832b45ee8e70e3ee64b57de727dfa3244f254caeeb5cb4f796687267a313308db3b1edec2540d06f94ef32d290f6749c44a89641d6bce3f778ecba52e4625e6a4c7ea7db2b7a6223f977cd2f182690fca97c60f2e16f64408086df5b494acd984c0cad7000b9d3cfa588a08229cd821d6cc19292ba42512fc5ae10bbc5004692f608e519b1d2ef030fc94e30b8888b7ed753c2fcd93ed245e0d95f1843e53944c4d4db671618b4c6948d5547a57aabcf77b4957e5fc446b88edf8385baa9ea3f3124efa6089774d2b9e66ad18267e938d8e9cda99dca534dca430f884568613b17d3ed9e0437dd3f64ebd49ed27fa1920c6c98abd20afde777a22f2b1f4a1da1ec8bd0b3c5d35aeea11975e864f8843ccebe922edd7bfac3bab504da094d4ac9fe16c129608ec182e2466ee175f07ff1697d250f023ede87b38e6e01f0c13ca4287ead31c38b482bb231d27c8b2c28e1791bb25924588ffd96ac464a4a67ddcf76d4ec9f840d8f138a220fd30006c7de4ab9baa5a4b8ffd21a55cf3886a44e1a43d6cb72e09027a1d2297fd689095e3535e175a7cc15fd8c9157d17f63fda55eec0166967c0693a5ac531863b0ed3dbdf16077bc667eb50043604b958ccc4a01422636481086ab7151cdb082cc3b22da917e6c5a4f2dfd3d75496b43af3d80b72b40c2254b12128c34f6f545d3fcdc1c7586e90ac2f512d47cae80b4d0ad66afabecc4e77dfd207c18db1ec2e741a8848b2075b1666d3140501c21eec54745a26d7726170e45408446b16c1849df47a1a70baa092dbff690261a9d0785a438d803e642f6ffc58680a747d5e28bfa742726458fe3d21a0aad8549f118506b9403b3be2df295dbf071902fa4d9b9d8963eddc58d3a5f49e9e62c47faccd0554042ed8b015f18fe3a755360a545268e20c1b2a8522241e39979e426f0603cd44bd8d3f35832464c5989bfdaa4c3f065c2e4b79f428f36e22dce38b5ea333c5ffe7ef8f9798b1fd05117ae70e75cfc77baa58bf18f3c92e9c59d37c579c1efa9ccade42c3e235e5615ec981419a443c99f0856542d48806e24251445a07fd26b8683db3822555f0878a4d17078bcc5f53eb17555f0f9057b6074dd6c8a114e8ac0fcd75a38f5035635dc3ebc0015d9b11f641a18c85c2115dbf6cbf5c10635a7c867c335b6d463143375f95cdc0c60dc52b898990c4ffd0433937ed9cd132bcb586ea11f15e1e01d8c77382956169a0596758433569f67aa9ca49e8028737ce85f76e0119f2e23e1d4ed33ce9dd638bd2f11af'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toClient:', uncodedData)

strdata = '155b5008cb25a7aa71348177f3dd01d2c8d15e50e63d9b14df1a6267d832349318b79e8f30619f'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'

strdata = 'b04b1acae9284d485af138de69'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToServer.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toServer:', uncodedData)

strdata = '6f4f9a8d891cdb29ddc293'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toClient:', uncodedData)

strdata = 'da2b7d15f2'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToServer.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toServer:', uncodedData)

strdata = '4f953ae4d6eab81753c492'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
print('toClient:', uncodedData)

strdata = 'c460aee3f848d047a494d26526ac8a67f0f54435d288bc960aa325973008387198b4e61cc540407db2ee98ea7d4bcb910ec8e66fb858d2997015d0d14fb195f725b455fd3519dcc58af54fdeaee690f215d8bc22a7674352897da7d75351e11670d62ff2139c685c3edcfbe317cf79a71c1dfe40d12d75cbcc1d565d7ca4f65c10b95c844d8e7ba00fabf7c68b420c712eec9b368f7a772e219a7bae976052c45144e39e09cd73d53f5761224f2a0b5de8a5c2d121a30accfc7c721853e9915f9c53c78a79c798503a00d00df62b32b30e0d45ab0a97dde209df792338dbc4d33da6cd6edecbbe27a3463f1eda89fa14aa47c0a7ddf4d3e169e817204278449475bf9fddd288e77fe513a0dce76288f2e2ff89fc9d51656ba1c1b9f9af71dda71ea8b104fce1e21fa501deb2a797f5996d4ef83dec0757fa8a7efad281f43d311974e0ff57f528405ef6cb944bc106e87be0eb09ad7258484d8095e8ae3cd9e4bf09784dfdd103ae8996009f8d402bc8cad2a40104696d100f424c5f9de10a9dfb28aa93e19279ea1e5c2278d4d4f42a3dfaf81dc557c1dc20fe63ac0ec042648019c34c01655bd1e58b54879defb12a47c7f7dbfc77cc33474415ff4f0f557a0ec030135204387437cb707d93752cff86361058c3d951a09e5346ea9a8b8576a3650d77478da08e8480195d1148becc3cda6545063a9dbf599d4ce4bc4bbd44068862fdca4342dc4509fb5170fedecc8fadc845418c97f59d6a7f004810abd3cb5432fbe03c483d253f84bac6da92ce98853bed099d7401b2ea46761ae4ff08701d6133e8a01c7c7f3211d70311f7784a28dcd0c034a478b188d631f9c5ec7e2c1fc15f6e4790d417dbb035f2b22cad6312d5e27fed00a711beed16043f2a22edd0fb5a273238b7adc64ab285e9d41d9b4fa40fd94c60434adf34fccfa2215f60d0e24cf42fe3d57e481b111092fe257923000cbf911c8e909e515d6965f7ce7adb7745d8117590b7f71d72778fe0fcfc6edc7f8fc84472e0a3f35657053729bfd87fd1cab85178f2f3a3b331972897453f3ae5e4ce8f341c27730bd34930135caa79fe29e524c1aec1e49aedfa103b46081909c2019ad6da8e38b2d0eae2854278f8d7d2ba7fff97a5ac1dc32faab38f943e3bd9e8a2ae00733f50ca361e00c718d63fafd3f9886c91db2f4f091b5f731235ce8fc9123e6ac538f05a6d422bddd5f01915c38942181ab9210662b9432e91717442840e5f3f11cb3951a2a9af9dde0372684af58131ea3e054317db930356451d8f12105713d8a54cf811d4793339cc377a8d53e595a47bdfb22b15d3fa405e1f33c41480c6d5077186616984749719ff6273980a336fdf0f88039e3f86ade863c27324a8310e52641043e46e1c633d2e258f2cfa0744a942d0bbae47d9b7b5564ecbd4fe95d0faa5e4cee68c57342fee238c19b515700bcf231fefaf1f46ef5b776a3d7d6a3397cd5ae4839a471c630ebbd425e6052f75209072b0dfae71d86f4aa8a51530010e43e9327ae7036f00cc41d353b789af4fc6146203e4c076e22b4ebcdf41a161a9e7895271231237da2cc39a2091427f2db761f8f14a138bb9f93bb85efd'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToClient.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'

print('===================================')
strdata = '692d4b55636ff4d7ea5750c15c3419256b7213be4a65c35ee79bc962e25c7364d3c6b7a1dd4f13c54d254ae3c1a194facc5d3f2be265a3ee7d0c718558389b8781698ba0a374a66330df3cbd078cc1d3900b4e6f973211d8f1ef6ce5cbfe2c99562c00ab0df3b855c4e9b68b2ce078584fbcaab8f5f1ac1098788a0575c488894733e68f62a6298e1fadaf4468e6df8272e7bfa5d1fe1797b5e65363bbb685eff752397074bdc27dcd0b267fd867edcb3453d8f6500336775ba64e1cdf8ccdbca95a92e456ab9d19375ef479619167a907b0e86f123982c23cfdeb34547642ad8567b97922790664e0fbdd95c9163019441c99b180bd73678b528c47969ce9fb4f1f91214ac8bda8b34ef44b34f2f9861ec8a6fa7aed7f6cd0011c2f8fdb97653b2616dbaff58098c409a4aa9d8af740211dbe85c009399cd1283a06884d8ffc'
strreal = bytes('', 'utf-8')
for i in range(0, len(strdata), 2):
    ele = strdata[i] + strdata[i + 1]
    strreal += int(ele, 16).to_bytes(1, 'big')
uncodes = mhzxSecurityObjToServer.decryption(strreal)
uncodedData = ''
for i in range(len(uncodes)):
    uncodedData += hex(uncodes[i]) + '|'
