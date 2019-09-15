# ------------------------------------------------------------------------------------
# torrentParser1.03，用于解析torrent文件
# 修改了函数getStructure,增加其节点值显示
# 2018年5月9日
# ------------------------------------------------------------------------------------
import time

from bencode import bdecode


# -------------------------------------
# torrentParser类
# -------------------------------------
class TorrentParser(object):
    # 构造函数
    def __init__(self, filePathname):
        self.filePathname = filePathname
        with open(filePathname, 'rb') as fObj:
            self.fileDic = bdecode(fObj.read())

            # 得到文件路径名

    def getFilepathname(self):
        return self.filePathname

    # 得到所有键值
    def getKeys(self):
        return self.fileDic.keys()

    # 得到全部内容
    def getAllContent(self):
        return self.fileDic;

    # 得到文件结构
    def getStructure(self):
        retval = ''
        layer = 0

        for key in self.fileDic.keys():
            value = self.fileDic[key]
            retval = retval + self.getNextNode(key, value, layer)

        return retval

    # 向下递归查找文件结构,
    def getNextNode(self, key, value, layer):
        retval = "";
        layer += 1

        if type(value) == type({}) and len(value.keys()) > 0:
            for i in range(1, layer + 1):
                retval = retval + "\t"
            retval = retval + str(key) + "\n"

            for k in value.keys():
                v = value[k]
                retval = retval + self.getNextNode(k, v, layer)
        elif type(value) == type([]) and len(value) > 0:
            for i in range(1, layer + 1):
                retval = retval + "\t"
            retval = retval + str(key) + "\n"

            arr = value

            for it in arr:
                if type(it) == type({}) and len(it.keys()) > 0:
                    for nk in it.keys():
                        nv = it[nk]

                        retval = retval + '' + self.getNextNode(nk, nv, layer)
        else:
            for i in range(1, layer + 1):
                retval = retval + "\t"

            showValue = str(value)[0:50]  # 显示的值

            retval = retval + str(key) + ":" + showValue + "\n"

        return retval

    # 获得tracker服务器的URL
    def getAnnounce(self):
        if 'announce' in self.fileDic:
            return self.fileDic['announce'].decode('utf-8', 'ignore')
        return ''

    # 获得tracker服务器的URL列表
    def getAnnounceList(self):
        retval = []

        if 'announce-list' in self.fileDic:
            arr = self.fileDic['announce-list']

            for childArr in arr:

                if type(childArr) == type([]):
                    for item in childArr:
                        retval.append(item.decode('utf-8', 'ignore'))
                else:
                    retval.append(childArr.decode('utf-8', 'ignore'))

        return retval

    # 得到制作日期
    def getCreateTime(self):
        if 'creation date' in self.fileDic:
            unixTimestamp = self.fileDic['creation date']
            firmalTime = time.localtime(unixTimestamp)
            dt = time.strftime('%Y-%m-%d %H:%M:%S', firmalTime)

            return dt
        else:
            return ''

    # 获得编码方式
    def getEncoding(self):
        if 'encoding' in self.fileDic:
            return self.fileDic['encoding'].decode('utf-8', 'ignore')
        return ''

    # 是否包含多个文件
    def hasMultiFiles(self):
        if 'files' in self.fileDic['info']:
            return True
        else:
            return False

    # 获得文件名
    def getTitle(self):
        arr = []
        info = self.fileDic['info']

        if 'name.utf-8' in info:
            arr = info['name.utf-8']
        else:
            arr = info['name']

            # print(str(arr))

        return arr.decode('utf-8', 'ignore')

        # 获得备注(可选项)

    def getComment(self):
        if 'comment' in self.fileDic:
            return self.fileDic['comment'].decode('utf-8', 'ignore')
        return ''

    # 获得创建者(可选项)
    def getCreatedBy(self):
        if 'created by' in self.fileDic:
            return self.fileDic['created by'].decode('utf-8', 'ignore')
        return ''

    # 多文件的情况下，得到多个文件的个数
    def getFileCount(self):
        return len(self.fileDic['info']['files'])

    # 多文件的情况下，获得所有文件
    def getFiles(self):
        files = []

        for item in self.fileDic['info']['files']:
            file = {}

            for key in item.keys():
                value = item.get(key)

                if key == 'path':
                    # print('1.'+str(value))
                    # print('10.'+str(value[0]))
                    path = value[0].decode('utf8', 'ignore')
                    value = path
                if key == 'path.utf-8':
                    # print('2.'+str(value))
                    # print('20.'+str(value[0]))
                    path = value[0].decode('utf8', 'ignore')
                    value = path

                file[key] = value

            files.append(file)

        return files

    # 单文件情况下，取文件名
    def getSingleFileName(self):
        return self.getTitle();

    # 单文件情况下，取文件长度
    def getSingleFileLength(self):
        return self.fileDic['info']['length']

    # 单文件情况下，取文件md5sum
    def getSingleFileMd5sum(self):
        if 'md5sum' in self.fileDic['info']:
            return self.fileDic['info']['md5sum'].decode('utf-8', 'ignore')
        else:
            return ''

    # 单文件情况下，取文件长度
    def getSingleFilePieceLength(self):
        return self.fileDic['info']['piece length']

    # 单文件情况下，取文件pieces
    def getSingleFilePieces(self):
        return self.fileDic['info']['pieces']

    # 得到文件简报
    def getBrief(self):
        retval = ""
        retval = retval + "File:" + self.filePathname + "\n"
        retval = retval + "announce:" + self.getAnnounce() + "\n"

        arr = self.getAnnounceList()
        if (len(arr) > 0):
            retval = retval + "announce list:" + "\n"

            for it in arr:
                retval = retval + "\t" + it + "\n"

        retval = retval + "Create time:" + self.getCreateTime() + "\n"
        retval = retval + "Ecoding:" + self.getEncoding() + "\n"
        retval = retval + "Title:" + self.getTitle() + "\n"
        retval = retval + "Comment:" + self.getComment() + "\n"
        retval = retval + "Created by:" + self.getCreatedBy() + "\n"

        hasMulti = self.hasMultiFiles()
        retval = retval + "has multi files:" + str(hasMulti) + "\n"
        if hasMulti == True:
            retval = retval + "[多文件结构]" + "\n"

            retval = retval + "包含文件个数为:" + str(self.getFileCount()) + "\n"
            retval = retval + "Files:" + "\n"

            files = self.getFiles();
            index = 1
            for item in files:
                retval = retval + "\tfile#" + str(index) + "\n"

                for key in item.keys():
                    value = item.get(key)
                    retval = retval + "\t\t" + str(key) + ":" + str(value) + "\n"
                retval = retval + "\n"

                index = index + 1
        else:
            retval = retval + "[单文件结构]" + "\n"
            retval = retval + "文件名为:" + self.getSingleFileName() + "\n"
            retval = retval + "文件长度:" + str(self.getSingleFileLength()) + "byte\n"
            retval = retval + "文件md5sum:" + self.getSingleFileMd5sum() + "\n"
            retval = retval + "文件块长度:" + str(self.getSingleFilePieceLength()) + "byte\n"

        return retval


# -------------------------------------
# 入口
# -------------------------------------
def main():
    tp = TorrentParser(filePathname='./最新 加勒比 鈴木.torrent')
    print('文件名=' + tp.getFilepathname())
    print('DONE1')
    print('文件结构:\n' + tp.getStructure())
    print('DONE2')
    print('文件简报:\n' + str(tp.getBrief()))
    print('DONE3')
    print('文件内容:\n' + str(tp.getAllContent()))
    print('DONE4')


# Start
main()
