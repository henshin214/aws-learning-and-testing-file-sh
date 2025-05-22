from flask import Flask,request,jsonify
import boto3
import pymysql.cursors

connect = pymysql.Connect(
    host='henshin.cluster-csd2q0i2sujm.us-east-1.rds.amazonaws.com',
    port=3306,
    user='henshin',
    passwd='qwer1234',
    db='henshin',
    charset='utf8'
)

cursor = connect.cursor()

sql = "CREATE TABLE henshin(id INTEGER PRIMARY KEY,value TEXT)"
try:
    cursor.execute(sql)
    connect.commit()
except:
    print("表已存在")
print('成功创建表格')


app = Flask(__name__)
@app.route('/', methods=['GET'])
def henshin():
    return "200"

@app.route('/post_data1', methods=['POST'])
def create_task():
    id=request.args.get('id')
    value=request.args.get('value')
    new_task = {
        'id': id,
        'value': value,
    }
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='arn:aws:dynamodb:us-east-1:178254122528:table/henshin',
        Item={
            'id': {
                'S': id,
             },
            'value': {
                'N': value
            }
        }
    )
    return jsonify({'task': new_task}), 200

@app.route('/post_data2', methods=['POST'])
def rds():
    id=request.args.get('id')
    value=request.args.get('value')
    rds = {
        'id': id,
        'value': value,
    }
    sql = "INSERT INTO henshin VALUES(%s,'%s')"
    data = (id, value)
    cursor.execute(sql % data)
    connect.commit()
    print('成功插入', cursor.rowcount, '条数据')
    return jsonify({'task': rds}), 200


@app.route('/get_value', methods=['GET'])
def get():
    id=request.args.get('id')
    client = boto3.client('dynamodb')
    response = client.get_item(
        TableName='arn:aws:dynamodb:us-east-1:178254122528:table/henshin',
        Key={
            'id': {
                'S': str(id),
            }
        }
    )
    dynamodb = int(response['Item']['value']['N'])
    connect = pymysql.Connect(
    host='henshin.cluster-csd2q0i2sujm.us-east-1.rds.amazonaws.com',
    port=3306,
    user='henshin',
    passwd='qwer1234',
    db='henshin',
    charset='utf8'
    )

    cursor = connect.cursor()
    sql = "SELECT * FROM henshin WHERE id=%s"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    if result:
        rds=int(result[0])
    # data = (f"{id}",)
    # cursor.execute(sql % data)
    # for row in cursor.fetchall():
    #     print("%s" % str(row))
    # rds = "%s" % str(row[1])
    sum=int(dynamodb)+int(rds)
    return {"message": str(sum)}, 200
if __name__ == '__main__':
    app.run(port=80,host="0.0.0.0")
