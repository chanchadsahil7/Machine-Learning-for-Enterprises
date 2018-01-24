import pandas as pd
import MySQLdb

def filter_data(company_id):
    json_obj = {}
    total_users = {
        1: ['1@gmail.com', 'a'],
        2: ['2@gmail.com', 'b'],
        3: ['3@gmail.com', 'c'],
        4: ['2@gmail.com', 'd'],
        5: ['5@gmail.com', 'a'],
        6: ['6@gmail.com', 'b'],
        7: ['7@gmail.com', 'c'],
        8: ['8@gmail.com', 'd'],
        9: ['9@gmail.com', 'a'],
        10: ['10@gmail.com', 'b'],
        11: ['11@gmail.com', 'c'],
        12: ['12@gmail.com', 'd'],
        13: ['13@gmail.com', 'a']
    }

    company_list = []

    for keys in total_users:
        if total_users[keys][1] == company_id:
            company_list.append(total_users[keys])

    return company_list

def get_header(filename):
    pass

def get_columns(filename):

    filedata = pd.read_csv(filename)
    return list(filedata.columns.values)

def get_numerical_metrics(filename,metrics):
    file_dt=pd.read_csv(filename)
    dic={'numerical_missing':[],'numerical_non_missing':[], 'non_numerical':[]}
    for i in metrics:
        if(file_dt[i].dtype == "int64" or file_dt[i].dtype == "float64"):
            count_of_null_values=list(file_dt[i].isnull()).count(False)
            if(count_of_null_values==0):
                dic['numerical_non_missing'].append(i)
            else:
                dic['numerical_missing'].append(i)
        else:
            dic['non_numerical'].append(i)
    return dic

def populate_filters_metrics(filename,dic,cid):
    conn = MySQLdb.connect(host="localhost",user="root",password="",db="sample")
	cur=conn.cursor()
	id=1
	for i in dic['filters']:
		cur.execute("""INSERT INTO filters VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
		id=id+1
	conn.commit()
    id=1
    for i in dic['metrics']:
        cur.execute("""INSERT INTO metrics VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
		id=id+1
	conn.commit()
    file_data=pd.read_csv(filename)
    for i in dic['remove']:
        file_data.drop([i],axis=1,inplace=True)
    query="Select name from company where id="+str(cid)
    cur.execute(query)
    t=cur.fetchall()
    company_name=t[0][0]
    s=filename.strip('/')
    table_name=company_name+'_'+s[-1]
    engine = create_engine("mysql+mysqldb://root:"+"@localhost/sample")
    data.to_sql(con=engine, if_exists='replace', name=table_name,index=False)
