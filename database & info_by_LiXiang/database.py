def raw_exec(string):
    '''
    执行SQL指令 返回相关结果
    :param string:
    :return:
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute(string)

    result_list = []
    for item in cursor:
        result_list.append(item)
    con.close()

    return result_list

def hash(src):
    """
    哈希md5加密方法
    :param src: 字符串str
    :return:加密后的32位md5码
    """
    import hashlib
    src = (src + "请使用私钥加密").encode("utf-8")
    m = hashlib.md5()
    m.update(src)
    return m.hexdigest()

def IsExistUser(userID):
    """
    验证登录用户是否存在
    :param userID: 用户名 str
    :return: 加密密码 str
    """
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select password from user where userID= ?",(userID,))
    r = c.fetchall()
    if r:
        '''for i in range(len(r)):
            print(r[i])'''
    else:
        '''print("not exit!")'''
        return None
    con.close()
    return r[0][0]

def Insert_User(userID,nickname,tel,password):
    '''
    注册用户信息添加到用户表
    :param userID: 用户名
    :param nickname: 昵称
    :param tel: 手机号
    :param password: 加密密码
    :return: 成功返回true
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    try:
        c.execute("insert into user (userID,nickname,tel,password) \
         values (?,?,?,?)", (userID, nickname, tel, password))
        con.commit()
        con.close()
    except Exception:
        con.rollback()
        sg = False
        con.close()
    finally:
        return sg
    return sg

def getUserLoginStatus(userid):
    '''
    获取用户的登录状态
    :param userid: 用户ID
    :return: 用户登录状态，'1'为已登录，'0'为未登录
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select log_status from user where userID= ? ", (userid,))
    r = c.fetchall()
    status = r[0][0]
    return status

def statusChange_Login(userid):
    '''
    将用户状态修改为已登录
    :param userid: 用户ID
    :return: 成功返回True，失败为False
    '''
    import sqlite3
    sg = True
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    try:
        c.execute("update user set log_status ='1' where userID= ? ", (userid,))
        con.commit()
        con.close()
    except Exception:
        con.rollback()
        sg = False
        con.close()
    finally:
        return sg
    return sg

def statusChange_Logout(userid):
    '''
    将用户状态修改为未登录
    :param userid: 用户ID
    :return: 成功返回True，失败为False
    '''
    import sqlite3
    sg = True
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    try:
        c.execute("update user set log_status ='0' where userID= ? ", (userid,))
        con.commit()
        con.close()
    except Exception:
        con.rollback()
        sg = False
        con.close()
    finally:
        return sg
    return sg

def getUserKeyword(userid, wxid):
    '''
    获取用户设置的关键词列表
    :param userid:用户ID
    :param wxid:微信ID
    :return:用户设置关键词列表
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select distinct keyword from WX_keyWords_set where userID= ? and WX_id= ?", (userid, wxid))
    kw = []
    for item in cursor:
        kw.append(item[0])
    con.commit()
    con.close()
    return kw

def getGroupName(userid,wxid,kw):
    '''
    查询用户设置的关键词关联的群聊
    :param userid: 用户ID
    :param wxid: 微信ID
    :param kw: 关键词
    :return: 关键词作用的所以群组
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select apply_area from WX_keyWords_set where userID= ? and WX_id= ? and keyword = ?", (userid, wxid,kw))
    grp = []
    for item in cursor:
        grp.append(item[0])
    con.commit()
    con.close()
    return grp

def insertWxGroupMessage(userid, wxid, msg_member, msg_group, msg_time, msg):
    '''
    将微信群聊消息保存到数据库
    :param userid: 用户ID
    :param wxid: 微信ID
    :param msg_member: 发送方微信ID
    :param msg_group:群来源
    :param msg_time:发送时间
    :param msg:消息内容
    :return:返回是否保存成功
    '''

    print([userid, wxid, msg_member, msg_group, msg_time, msg])

    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    try:
        c.execute("insert into WX_group_msg (userID,WX_id,source_WX_id,src_WXgrp,msg_time, msg) \
         values (?,?,?,?,?,?)", (userid, wxid, msg_member, msg_group, msg_time, msg))
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        con.rollback()
        sg = False
        print('[-]Error')
        con.close()
    finally:
        return sg

def setKeywords_0(userid,wxid,key,group):
    '''
    微信设置关键词初始化，将所有的群组状态置为0
    :param userid:用户ID
    :param wxid:微信ID
    :param key:关键词
    :param group:作用的群聊名称（列表）
    :return: 是否成功的bool值
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    for i in range(len(group)):
        try:
            c.execute("insert into WX_keyWords_set (userID,WX_id,keyword,apply_area,chosen) \
                 values (?,?,?,?,?)", (userid, wxid, key, group[i],0))
            con.commit()
            #con.close()
        except Exception as e:
            print(e)
            con.rollback()
            sg = False
            print('[-]Error')
            #con.close()
        #finally:
            #return sg
    con.close()
    return sg

def setKeywords_1(userid,wxid,key,group):
    '''
    微信设置关键词和应用群组,将群组状态置为1
    :param userid:用户ID
    :param wxid:微信ID
    :param key:关键词
    :param group:作用的群聊名称（列表）
    :return: 是否成功的bool值
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    for i in range(len(group)):
        try:
            c.execute("update WX_keyWords_set set chosen=1 where userID=? and WX_id=? and keyword=? and apply_area=?", (userid, wxid, key, group[i]))
            con.commit()
            #con.close()
        except Exception as e:
            print(e)
            con.rollback()
            sg = False
            print('[-]Error')
            #con.close()
        #finally:
            #return sg
    con.close()
    return sg

def deleteKeywordOfGroup(userid,wxid,keyword,grp):
    '''
    删除一个关键词作用的一个群聊
    :param userid:用户ID
    :param wxid:微信ID
    :param keyword:关键词
    :param grp:要删除的一个群
    :return:成功为1，失败为0
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    try:
        c.execute("delete from WX_keyWords_set where userID=? and WX_id=? and keyword=? and apply_area =?",(userid, wxid, keyword, grp))
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        con.rollback()
        sg = False
        print('[-]Error')
        con.close()
    finally:
        return sg


def deleteKeyword(userid,wxid,keyword):
    '''
    删除关键词
    :param userid:用户ID
    :param wxid:微信ID
    :param keyword:关键词
    :return:成功1，失败0
    '''

    apy_are = []
    apy_are = getGroupName(userid,wxid,keyword)
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    for i in range(len(apy_are)):
        sg = True
        try:
            c.execute("delete from WX_keyWords_set where userID = ? and WX_id = ? and keyword = ? and apply_area = ?  ", (userid,wxid,keyword,apy_are[i]))
            con.commit()
            con.close()
        except Exception as e:
            print(e)
            con.rollback()
            sg = False
            print('[-]Error')
            con.close()
        #finally:
    return sg


def addKeywordGroup(userid,wxid,key,group):
    '''
    增加一个关键词作用的群聊
    :param userid: 用户ID
    :param wxid: 微信ID
    :param key: 关键词
    :param group: 群名称
    :return: 成功为“1”，失败为“0”
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    sg = True
    try:
        c.execute("insert into WX_keyWords_set (userID,WX_id,keyword,apply_area) \
                 values (?,?,?,?)", (userid, wxid, key, group))
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        con.rollback()
        sg = False
        print('[-]Error')
        con.close()
    finally:
        return sg

def getUseridAndWxidWithLogStatus():
    '''
    将登陆状态为1的用户信息输出
    :return: 用户ID和wxid
    '''
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select userID,WX_id from Wechat where Wechat.userID = User.userID and User.log_status=1")
    info = []
    for item in cursor:
        info.append(item[0])
    con.commit()
    con.close()
    return info

def getChosen(userid,wxid,key):
    import sqlite3
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    cursor = c.execute("select chosen from WX_keyWords_set where userID= ? and WX_id= ? and keyword = ?", (userid, wxid,key))
    #info = []
    for item in cursor:
        info=item[0]
    con.commit()
    con.close()
    return info


def changeKeywordGroupStatus(userid,wxid,key,grp):
    '''
    关键词操作群组改变，将传入的群组列表的群组的状态置1
    :param userid:用户ID
    :param wxid:微信ID
    :param key:关键词
    :param grp:群聊名称列表
    :return:成功为True，失败为False
    '''
    import sqlite3
    sg = True
    con = sqlite3.connect('Jarvis-forChat.db')
    c = con.cursor()
    for i in range(len(grp)):
        try:
            c.execute("update WX_keyWords_set set chosen=0 where userID= ? and WX_id= ? and keyword = ?",
                       (userid, wxid, key))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            sg = False
            print('[-]Error')
        #finally:
        #    return sg
    for i in range(len(grp)):
        try:
            c.execute("update WX_keyWords_set set chosen=1 where userID=? and WX_id=? and keyword =? and grp=?",
                      (userid, wxid, key, grp[i]))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            sg = False
            print('[-]Error')
        #finally:
        #    return sg
    #con.commit()
    con.close()
    return sg

def keyWordGroupStatus(userID, WX_id, keyword):
    '''
获取相应关键词作用的群组状态
    :param userID: 用户名 字符串类型
    :param WX_id: 微信账号 字符串类型
    :param keyword: 关键词 字符串类型
    :return: tuple类型，群名：状态(1/0)
    '''
    import sqlite3
    conn = sqlite3.connect('Jarvis-forChat.db')
    c = conn.cursor()
    list = []
    try:
        cursor = c.execute("select apply_area, chosen from WX_keyWords_set where userID =? and WX_id = ? and keyword = ?",
                       (userID, WX_id, keyword))
        for row in cursor:
            if row[1] == 1:
                value = 1
            else:
                value = 0

            tuple = (row[0], value)
            list.append(tuple)
    except Exception as e:
        print(e)
        conn.rollback()
        sg = False
        print('[-]Error')
    conn.close()
    return list