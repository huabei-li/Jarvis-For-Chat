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
    cursor = c.execute("select keyword from WX_keyWords_set where userID= ? and WX_id= ?", (userid, wxid))
    kw = []
    for item in cursor:
        kw.append(item[0])
    con.commit()
    con.close()
    return kw
