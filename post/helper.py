from math import ceil


def paging(thePage=1, postMax=0, pageShow=2, pageCount=10):
    '''

    :param thePage: 当前页
    :param pageMax: 最大文章数(来源于数据库count)
    :param pageShow: pagShow * 2 + 1 = 前端要显示的页码标签数量。如要显示 9 个页码标签，则pageShow = 4
    :param pageCount: 每一页要显示的文章数
    :return: 返回 postBegin: 给数据库切片用, postEnd: 给数据库切片用,
            thePage: 加工过的当前页，避免用户请求超出正常范围的页面,
            pageMax: 最大页数, pages: 包含了页码标签中要显示的动态页码, 一个能够被前端遍历的对象。
    '''

    def thePages(pageMax=1, pageshowed=1, thePage=1):
        if thePage < 1:
            thePage = 1
            pages = range(thePage, pageshowed + 1)
        elif thePage > pageMax:
            thePage = int(pageMax)
            pages = range(thePage - pageshowed, thePage + 1)
        else:
            pages = range(thePage - (pageshowed / 2), thePage + (pageshowed / 2))
        return pages, thePage


    if postMax < pageCount:
        print(postMax, '最大文章数')
        postMax = pageCount

    pageMax = ceil(postMax / pageCount)

    pageshowed = pageShow * 2
    print(pageMax, '最大页')
    if pageMax < 3:
        if pageMax == 1:
            pages = [1]
        if pageMax == 2:
            pages = [1, 2]

    elif pageMax < pageshowed + 1:
        if pageMax % 2 == 1:
            pageshowed = pageMax - 1
            pages, thePage = thePages(pageMax=pageMax, pageshowed=pageshowed, thePage=thePage)
        else:
            if pageMax < 5:
                pageshowed = 2
                pages, thePage = thePages(pageMax=pageMax, pageshowed=pageshowed, thePage=thePage)
            else:
                pageshowed = pageMax / 2
                pages, thePage = thePages(pageMax=pageMax, pageshowed=pageshowed, thePage=thePage)

        pass
    else:
        if thePage <= pageShow:
            pages = range(1, pageCount)
        elif thePage >= pageMax - pageShow:
            pages = range(pageMax - pageshowed, pageMax + 1)
        else:
            pages, thePage = thePages(pageMax=pageMax, pageshowed=pageshowed, thePage=thePage)


    if thePage > pageMax:
        thePage = int(pageMax)
    if thePage < 1:
        thePage = 1

    postBegin = (thePage - 1) * pageCount
    postEnd = thePage * pageCount
    print(postBegin, postEnd, '开始结尾')

    return postBegin, postEnd, thePage, pageMax, pages
