import pymysql


class Database:
    def __init__(self):  # db 설정
        self.host = 'localhost'
        self.port = 3306
        self.user = 'NLP'
        self.pw = 'haltheta'
        self.charset = 'utf8'
        self.db = 'qna_list'

    def get_sql(self, sql):  # sql 실행 / 성공 시 딕셔너리 형태로 반환 실패 시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, password=self.pw, charset=self.charset, db=self.db
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                curs.execute(sql)
                rs = curs.fetchall()

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()

            return rs

    def get_question_list(self):  # 질문 리스트 가져오기 딕셔너리 리스트
        return self.get_sql('select * from q_list')

    def question_count(self):  # 질문 갯수 반환
        return self.get_sql('select COUNT(question) as count from q_list')[0]['count']

    def answer_count(self):  # 답변 갯수 반환
        return self.get_sql('select COUNT(id) as count from a_list')[0]['count']

    def answer_max(self):  # 답변 최대값 반환
        return self.get_sql('select MAX(id) as max from a_list')[0]['max']

    def get_answer(self, a_id):  # 성공 시 답변 / 실패 시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, password=self.pw, charset=self.charset, db=self.db
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'select answer from a_list where id = %s'
                curs.execute(sql, a_id)
                ans = curs.fetchall()

                rs = ans[0]['answer']

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()

            return rs

    def add_answer(self, answer):  # 답변 등록 / 답변 id 반환 실패시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, password=self.pw, charset=self.charset, db=self.db
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into a_list (answer) values (%s)'
                curs.execute(sql, answer)
                conn.commit()

                rs = curs.lastrowid

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()

            return rs

    def add_question(self, question, a_no):  # 질문 등록 / 성공 시 1 실패 시 -1 반환
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, password=self.pw, charset=self.charset, db=self.db
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into q_list (question, answer_no, l_pt) values (%s, %s, 0)'
                curs.execute(sql, (question, a_no))
                conn.commit()

                rs = 1

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()

            return rs

    def modify_pt(self, q_id, change): # id의 질문의 l_pt(포인트) +- 하기 // 성공시 1, 실패시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, password=self.pw, charset=self.charset, db=self.db
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                if change == -1:
                    sql = 'update q_list set l_pt = l_pt - 1 where id = %s'
                else:
                    sql = 'update q_list set l_pt = l_pt + 1 where id = %s'

                curs.execute(sql, q_id)
                conn.commit()
                rs = 1

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()

            return rs


# 예제 나중에 지우기
'''
if __name__ == "__main__":
    db = Database()

    print("question_count: %s" % db.question_count())
    print("answer_count: %s" % db.answer_count())
    print("answer_max: %s" % db.answer_max())
    print("answer for id 1: %s" % db.get_answer(1))
    # print("add answer returns id #")
    # print("add question returns 1 when successful: %s" %db.add_question("DB TEST", db.add_answer("DB TEST")))
    print("modifies l_pt of question by -1: %s" % db.modify_pt(1, -1))

    row = db.get_question_list()
    if row is not None or row != -1:
        for i in row:
            print(i['question'])
    print(row[0])
'''