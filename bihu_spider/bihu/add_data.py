# coding:utf-8
import requests
import random
import time

class AddData(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    
    def post_add(self, data_dict):
        url = 'https://www.soniubi.com/e/locoy/diguo7.2.php?_xz_action=addNews&_xz_pubkey=0.123456'
        data = {
            'classid':14,
            'title':data_dict['title'],
            'newstime':time.strftime('%Y-%m-%d %H:%m',time.localtime(time.time())),
            'newstext':data_dict['content'],
            'zuozhe':data_dict['userName'],
            'caijiurl':'https://bihu.com/article/'+str(data_dict['id']),
            'zuozheid':data_dict['userId'],
            'fenlei':data_dict['boardName'],
            'zuozhetouxiang':'https://bihu2001.oss-cn-shanghai.aliyuncs.com/' + data_dict['userIcon'],
            'newspath':'',
            'checked':'1',
            'oldchecked':'1',
            'onclick':random.randint(2000,3000)
        }
        print(data)
        response = requests.post(url=url,data=data, headers=self.headers).content
        print(response)


    def run(self):
        data_dict = {
            "boardCode" : "EOS", "boardId" : "5", "boardName" : "EOS", "boards" : [ { "boardCode" : "EOS", "boardId" : 5, "boardName" : "EOS" } ], "cmtList" : [ ], "cmts" : 16, 
            "content" : '<div><p><img src=\"https://bihu2001.oss-cn-shanghai.aliyuncs.com/img/f99d079518bdc2236861f5b3d672cb91.png?x-oss-process=style/size_lg\" style=\"max-width:100%;\"><br></p><p>POW、POS、DPOS，无论在那种共识里面，节点最主要也是最重要的工作就是打包交易，传递价值，而掌控节点的人其实就是区块链世界里面的价值搬运工。价值搬运工可以获得系统奖励，还可以获得交易手续费，用以支撑这些节点人付出的电力、机器和智商输出。<br></p><p></p><p></p><p><br></p><p>之前我算过一笔帐，一个BTS≈2.5元的时候，BTS见证人每天可以获得等值2000多人民币的工资，（一天！！！我每天码字都没有那么多钱，感觉我被码代码的碾压了）。</p><p><br></p><p>见证人每天最主要的工作是打包交易生成区块，出一个块奖励1BTS。而BTS系统要求5s出一个块，那么1天奖励总额是17280个（折合约4.3w人民币），分给活跃的见证人。目前BTS的见证人是23个。</p><p><br></p><p>当然，BTS不值钱的时候，见证人每天收到的BTS也不值一提。</p><p><br></p><p>所以，你发现没有，见证人和投资人拥有的都是代币，只有代币升值了，你才能获得收入。这种逻辑在传统世界里面也能找得映射，但却不完全一样：雇佣者（见证人）打工获得工资，投资者（代币购买人）投资获得公司股份，公司成长了，给雇佣者更多年终奖，给股东更多分红。</p><p><br></p><p>这里，雇佣者和股东的”贫富差距”特别大，地位也差很多。而在区块链世界里面，见证人和代币购买人要平等得多，买代币也被认为是贡献系统，系统以成长价值做为奖励。</p><p><br></p><p>区块链世界里面，打工的和投资的都是买的原始股票。</p><p><br></p><p><br></p><h4><strong>01.&nbsp;</strong><strong>怎么给区块链打工</strong></h4><p><br></p><p>估计很多人看到了见证人的日工资，已哭晕在厕所。超1级市场获得，还可以不通过子弹购买，简直是太诱人了。之前看到估算，1枚比特币挖矿成本是8k刀，当时比特币市场最高的时候到过2w刀，自己算一下溢价，是不是有点吓人。而且比特币的节点我认为成本还是最高的，因为各个节点是竞争关系，而非合作关系，会造成一些竞争损耗。可想而知，那些以节点合作关系存在的算法，如POS和DPOS，当它们的节点利润会有多高了。</p><p><br></p><p>那么如何给区块链打工？答案肯定是当见证人！BTS的见证人、EOS的见证人、ETH改POS后的见证人。只有见证人有权利打包交易，从而获得奖励。</p><p><br></p><p>不同共识里，对于打包交易的见证人叫法不一样。我们把这种用非真金获得代币的人叫旷工，而他们的打包行为我们统一叫做挖矿（遵从了中本聪最初始的叫法——“Miner&amp;Mining”）。矿工通过挖矿来获取系统奖励，同时打包交易到区块获得手续费。</p><p><br></p><p><br></p><p>如何才能当见证人？</p><p><br></p><p>很简单，POW里面看算力，POS和DOSP里面看投票。如BTC和现阶段的ETH，你可以买对应的矿机，然后自己安装运转起来就可以，不需要经过任何人的允许，但是能不能挖到矿就得看算力和运气了。而DPOS是投票机制，系统选择最高得票作为见证人。</p><p><br></p><p><br></p><h4><strong>02.&nbsp;</strong><strong>我能当见证人吗？</strong></h4><p><br></p><p>这个问题得问自己，你有多少矿机？你在社区里面有多少人支持？</p><p><br></p><p>这几种共识发展到现在，区块链世界已经比较清晰了，<strong>能获得奖励的要不有钱要不有人，像极了大国政治</strong>。POW里面谁算力多，挖到矿更容易，其实就是比财富多少。DPOS里谁获得的投票越多，谁就能当见证者，其实就是看人脉多少。</p><p><br></p><p>如BTS系统里面，见证人要不就是能力超强的开发者，要不就是持币大户，要不就是开发能力超强且是持币大户。请问你是哪个？</p><p><br></p><p>有人怀疑这几种算法的公平性，我告诉你，世界从来就没有绝对的公平。</p><p><br></p><p>但我记得，奥地利的总理就是平民出身，然后一路逆袭的。散户相当是平民，当见证人唯一的出路也就只有兢兢业业为社区做贡献，获得社区人员认同和投票了。比如像现在的我，写写文章，普及普及社区知识。</p><p><br></p><p><br></p><h4><strong>03. EOS见证人节点</strong></h4><p><br></p><p>EOS对于见证人出块奖励是1EOS，而且是3s出一个块，一天奖励28800个EOS，按照今天50元一个EOS，奖励总额折合人民币144万。而EOS见证人节点固定是21个，那么平均每个人能得到≈7万人民币一天。</p><p><br></p><p>如果你一直在节点生产队里面，不作恶且长期保持投票领先，那拿到奖励很稳的。这还是EOS在低点的时候，500的时候是多少？1000的时候是多少？真的很诱人。</p><p><br></p><p>但是不要被幸福冲昏了头脑，你是在和全世界再竞争这21个节点。</p><p><br></p><p>目前，EOS见证人节点投票系统还没出来，基于DPOS共识系统基本不会差别太多。可以参考BTS的Witness投票系统，可以投票、弃票或者委托自己的投票权，像人大代表投票是一样的。大家可以关注一下EOS的见证人节点，会是一门好生意。自己做不了的话，可以考虑合作投票。</p><p><br></p><p><br></p><p><br></p><p><strong>总的来说，见证人是社区共识，拥戴出来的候选人要不有领导力，带领社区前进；要不是持币大户，拥有左右币价的权利；要不就是社区开发者，能让社区变得更加完善。</strong></p><p><br></p><p><br></p><p><br></p><p>欢迎关注微信公众号：<strong>区块链卡咩</strong></p><p>欢迎关注本人微博：<strong>比特币卡咩</strong></p><p>希望交流的朋友可以添加我的个人微信：kamiesheep</p></div>', 
            "creatime" : 'NumberLong("1519652272000")', "del" : False, "down" : 0, "downList" : [ ], "downs" : 0, "follow" : 0, "fs" : 1, "id" : 2020, "imgList" : [ { "name" : "img/f99d079518bdc2236861f5b3d672cb91.png", "resId" : "0" } ], "money" : 38.92, "rtf" : 1, "snapContent" : "POW、POS、DPOS，无论在那种共识里面，节点最主要也是最重要的工作就是打包交易，传递价值，而掌控节点的人其实就是区块链世界里面的价值", "title" : "谈EOS节点能获得的利润（7万一天的工资？）", "up" : 0, "upList" : [ ], "updatime" : 'NumberLong("1519652272000")',"ups" : 42,"userIcon" : "img/a82de06f7912de1b8d9a11181c18b21c.png", "userId" : 10411, "userName" : "区块链卡咩", "valid" : 0 
            }
        self.post_add(data_dict)

    def main(self):
        self.run()


if __name__=="__main__":
    adds = AddData()
    adds.main()




