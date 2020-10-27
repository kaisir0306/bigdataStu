# coding=UTF-8
from pyhive import hive
import datetime
import sys, requests
import os
import re
def save_file(file_dir, content):
    f = open(file_dir, 'w')
    f.write(content)
    f.close()


def create_dir(sql_dir):
    if os.path.exists(sql_dir):
        print
        sql_dir, 'has exists'
        exit
    else:
        os.makedirs(sql_dir)
        print
        sql_dir + ' 创建成功'

#是否是回文数
def is_huiwen(phone):
    reversed_str=str(phone)
    if reversed_str==reversed_str[-1::-1]:
        return 1
    else:
        return 0

def is_same(phone):
    reversed_str = str(phone)
    last_num=reversed_str[-1] #取最后一位
    new_str=reversed_str[::-1][1:] #反转后取第二位到最后一位
    num=0
    for i in new_str:
        if i==last_num and i!='4':
            num=num+1
        else:
            return num

##判断是否是
def tow_num(phone):
    reversed_str = str(phone)
    new_str = reversed_str[::-1][0:4]
    new_set=set(new_str)
    se=list(new_set)
    if len(se)==2 and '4' not in se and int(se[0])+1==int(se[1]):
        return 1
    elif len(se)==2 and '4' not in se and int(se[0])-1==int(se[1]):
        return 1
    else:
        return 0

##判断后三位是否是连续数字
def is_continuous(phone):
    reversed_str=str(phone)
    new_str=reversed_str[::-1]
    nums=list()
    for i in new_str:
        nums.append(int(i))
    if  nums[0]+1==nums[1] and nums[1]+1==nums[2] and nums[0]+2==nums[2] and 4 not in nums :
        return  1
    elif nums[0]-1==nums[1] and nums[1]-1==nums[2] and nums[0]-2==nums[2] and 4 not in nums :
        return 1
    else:
        return 0
# def  shabizhoupeng(phone):
#     reversed_str = str(phone)
#     t = re.compile(r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$')
#     s = re.search(t, reversed_str)
#     if()


if __name__ == '__main__':
    file_name = os.path.split(os.path.realpath(__file__))[0] + "/dw_u_user_phone_type_s.txt"
    f = open(file_name, 'w')
    conn = hive.Connection(host='10.89.89.48', port=10000, username='hive')
    cursor = conn.cursor()
    cursor.execute("select id,phone  from bdp_ods_private.ods_ucenter_user_profile  ")
    for result in cursor.fetchall():
       try:
           re_list=list(result)
           re_list.extend([is_same(re_list[1]),tow_num(re_list[1]),is_continuous(re_list[1]),is_huiwen(re_list[1])])
           final_result=re_list[0]+','+str(re_list[2])+","+str(re_list[3])+","+str(re_list[4])+","+str(re_list[5])+"\n"
           f.write(final_result)
       except Exception as e:
           print(e)
    f.close()
    # cmd = 'hive -e ' + "\"LOAD DATA LOCAL INPATH \'" + file_name + "\' overwrite into table bdp_dw.dw_u_user_phone_type_s\""
    # val = os.system(cmd)