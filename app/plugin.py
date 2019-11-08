import pymysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api


class DBFuncs:
    # def __init__(self): # db 연결 유지

    def get_sql(self, sql):  # sql 실행 / 성공 시 딕셔너리 형태로 반환 실패 시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host='localhost', port=3306, user='NLP', password='haltheta', charset='utf8', db='qna_list'
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                curs.execute(sql)
                rs = curs.fetchall()

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn != None:
                conn.close()

            return rs

    def get_question_list(self):  # 질문 리스트 가져오기 딕셔너리 형태
        res = self.get_sql('select * from q_list')

        return res

    def question_count(self):  # 질문 갯수 반환
        res = self.get_sql('select COUNT(question) as count from q_list')

        return res

    def answer_count(self):  # 답변 갯수 반환
        res = self.get_sql('select COUNT(id) as count from a_list')

        return res

    def get_answer(self, id):  # 성공 시 답변 / 실패 시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host='localhost', port=3306, user='NLP', password='haltheta', charset='utf8', db='qna_list'
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'select answer from a_list where id = %s'
                curs.execute(sql, id)
                ans = curs.fetchall()

                rs = ans[0]['answer']

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn != None:
                conn.close()

            return rs

    def add_answer(self, a):  # 답변 등록 / 답변 id 반환 실패시 -1
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host='localhost', port=3306, user='NLP', password='haltheta', charset='utf8', db='qna_list'
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into a_list (answer) values (%s)'
                curs.execute(sql, (a))
                conn.commit()

                rs = curs.lastrowid

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn != None:
                conn.close()

            return rs

    def add_question(self, q, a_no):  # 질문 등록 / 성공 시 1 실패 시 -1 반환
        conn = None
        rs = -1

        try:
            conn = pymysql.connect(
                host='localhost', port=3306, user='NLP', password='haltheta', charset='utf8', db='qna_list'
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'insert into q_list (question, answer_no, l_pt) values (%s, %s, 0)'
                curs.execute(sql, (q, a_no))
                conn.commit()

                rs = 1

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn != None:
                conn.close()

            return rs

    def modify_pt(self, q_id, change):
        conn = None
        rs = -1
        pt = 0

        try:
            conn = pymysql.connect(
                host='localhost', port=3306, user='NLP', password='haltheta', charset='utf8', db='qna_list'
            )

            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                sql = 'select l_pt from q_list where id = %s'
                curs.execute(sql, q_id)
                rs = curs.fetchall()

                pt = rs[q_id - 1]['l_pt']

                if change == -1:
                    pt -= 1
                else:
                    pt += 1

                sql = 'update q_list set l_pt = %s where id = %s'
                curs.execute(sql, (pt, q_id))
                conn.commit()
                rs = 1

        except pymysql.err.Error as e:
            print(e)

        finally:
            if conn != None:
                conn.close()

            return rs


class API:
    def __init__(self):
        self.app = Flask(__name__)
        api = Api(self.app)

        api.add_resource(Plugin, '/')
        api.add_resource(RequestAnalysis, '/plugin/RA')
        api.add_resource(AddQnA, '/plugin/AQA')

    def run_app(self):
        self.app.run(debug=True)
        # debug never in production


class Plugin(Resource):
    def get(self):
        return "Plugin For AI QnA Board"


class RequestAnalysis(Resource):
    def __init__(self):
        self.db = DBFuncs();

    def get(self):
        return "QnA API - Request Analysis"

    def put(self):
        res = -1
        analyzed = -1

        try:
            question = request.get_json().get('question')
            # print(question)

            if question is not None:
                analyzed = 1
                # 자연어 처리 함수 여기에

            if analyzed != -1:
                answer = self.db.get_answer(analyzed)
                # print(answer)
                res = 1

        except Exception as e:
            print("Error in RA")
            print(e)

        finally:
            if res == 1:
                return jsonify({"answer": answer})
            else:
                return jsonify({"answer": res})


class AddQnA(Resource):
    def __init__(self):
        self.db = DBFuncs();

    def get(self):
        return "QnA API - Add QnA"

    def post(self):
        res = -1
        a_id = -1

        try:
            question = request.get_json().get('question')
            answer = request.get_json().get('answer')

            if answer is not None:
                a_id = self.db.add_answer(answer)

            if a_id != -1:
                res = self.db.add_question(question, a_id)

                if res != -1:
                    res = 1

        except Exception as e:
            print("Error in AQA")
            print(e)

        finally:
            return jsonify({"result": res})


if __name__ == "__main__":
    CA = API()
    CA.run_app()

# 예제 나중에 지우기
'''
    qna_db = DBFuncs()
    row = qna_db.get_question_list()
    if row != -1:
        for i in row:
            print(i['question'])

    count = qna_db.question_count()
    if count != -1:
        print(count[0]['count'])

    res = qna_db.add_answer('답변 벡터값에 대한 벡터 분류로 구분합니다.')
    if res == -1:
        print('insert error')
    else:
        res = qna_db.add_question('유사한 질문은 어떻게 구분하나요?', res)

    res = qna_db.modify_pt(1, -1)
    if res != -1:
        row = qna_db.get_question_list()
        if row != -1:
            for i in row:
                print(i['l_pt'])

    res = qna_db.get_answer(2)
    print(res)
    
    # curl -i -H "Content-Type: application/json" -X POST -d "{\"question\":\"Rest API \uD14C\uC2A4\uD2B8\",\"answer\":\"REST API \uD14C\uC2A4\uD2B8\"}" http://localhost:5000/plugin/AQA
'''