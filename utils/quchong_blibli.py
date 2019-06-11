import psycopg2


def run_1():
    v_list = []
    conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
    cur = conn.cursor()

    cur.execute("select * from data_blibli;")

    data = cur.fetchall()
    for each_data in data:
        v_id = each_data[0]
        if v_id not in v_list:
            v_list.append(v_id)
            cur.execute(
                """insert into data_blibli_copy(video_id,video_title,video_url,like_cnt,view_cnt,
                coin_cnt,favorite_cnt,pub_time,do_time,type_name,cid,video_time,is_download) values 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                each_data + (False,)
            )
            conn.commit()
    conn.close()
    print('ok')


def run_2():
    conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
    cur = conn.cursor()

    cur.execute("select * from data_blibli_shishang_shenghuo_other;")

    data = cur.fetchall()
    for each_data in data:
        cur.execute(
            """insert into data_blibli_all(video_id,video_title,video_url,like_cnt,view_cnt,
            coin_cnt,favorite_cnt,pub_time,do_time,type_name,cid,video_time,redis_task_id,is_download) values 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            each_data
        )
        conn.commit()
    conn.close()
    print('ok')


if __name__ == '__main__':
    run_2()
