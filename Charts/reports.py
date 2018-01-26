import MySQLdb
import pandas as pd
import os
import json
from sqlalchemy import create_engine
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

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

def get_columns(filename):
	filedata = pd.read_csv(filename)
	return list(filedata.columns.values)

'''def get_connection():
	#connection establishment
	conn = MySQLdb.connect(host="localhost",user="root",password="pass",db="sample")
	return conn'''

def get_numerical_metrics(filename,metrics):
	'''conn=get_connection()
	cur=conn.cursor()'''
	#getting type of metrics
	file_dt=pd.read_csv(filename)
	dic_metrics_type={'numerical_missing':[],'numerical_non_missing':[], 'non_numerical':[]}
	for i in metrics:
		if(file_dt[i].dtype == "int64" or file_dt[i].dtype == "float64"):
			count_of_null_values=list(file_dt[i].isnull()).count(False)
			if(count_of_null_values==0):
				dic_metrics_type['numerical_non_missing'].append(i)
			else:
				dic_metrics_type['numerical_missing'].append(i)
		else:
			dic_metrics_type['non_numerical'].append(i)
	#remove the columns
	# for i in dic['remove']:
	#     file_dt.drop([i],axis=1,inplace=True)
	# #populate filter table
	# id=1
	# for i in dic['filters']:
	# 	cur.execute("""INSERT INTO filters VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
	# 	id=id+1
	# conn.commit()
	# id=1
	# for i in dic_metrics_type['non_numerical']:
	# 	cur.execute("""INSERT INTO filters VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
	# 	id=id+1
	# conn.commit()
	# #populate metrics table
	# id=1
	# for i in dic_metrics_type['numerical_missing']:
	#     cur.execute("""INSERT INTO metrics VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
	# 	id=id+1
	# conn.commit()
	# id=1
	# for i in dic_metrics_type['numerical_non_missing']:
	#     cur.execute("""INSERT INTO metrics VALUES (%s,%s,%s,%s)""",(id,i,1,cid))
	# 	id=id+1
	# conn.commit()
	# #storing the database with table_name before
	# table_name=get_function_name(filename,cid,'before')
	# engine = create_engine("mysql+mysqldb://root:"+"@localhost/sample")
	# data.to_sql(con=engine, if_exists='replace', name=table_name,index=False)
	# conn.close()
	return dic_metrics_type

'''def get_function_name(filename,cid,st):
	conn=get_connection()
	cur=conn.cursor()
	query="Select name from company where id="+str(cid)
	cur.execute(query)
	t=cur.fetchall()
	company_name=t[0][0]
	s=os.path.basename(filename)
	s=s.strip('.csv')
	table_name=company_name+'_'+s+'_'+st
	conn.close()
	return table_name

def data_cleaning_and_table_creation(filename,cid,metrics):
	conn=get_connection()
	table_name = get_function_name(filename,cid,'before')
	dataframe_before = pd.read_sql('select * from '+table_name,conn)
	for i in metrics:
		if(metrics[i] == 'mean'):
			dataframe_before[i].fillna(dataframe_before[i].mean(),inplace = True)
		elif(metrics[i] == 'median'):
			dataframe_before[i].fillna(dataframe_before[i].median(),inplace = True)
		elif(metrics[i] == 'mode'):
			dataframe_before[i].fillna(dataframe_before[i].mode,inplace = True)
		else:
			pass
	conn.close()
	table_name=get_function_name(filename,cid,'after')
	engine = create_engine("mysql+mysqldb://root:"+"@localhost/sample")
	data.to_sql(con=engine, if_exists='replace', name=table_name,index=False)'''

def get_file_name(filename,cid):
	conn=get_connection()
	cur=conn.cursor()
	query="Select name from company where cid="+str(cid)
	cur.execute(query)
	t=cur.fetchall()
	company_name=t[0][0]
	s=os.path.basename(filename)
	s=s.strip('.csv')
	table_name=company_name+'_'+s
	conn.close()
	return table_name

def get_connection():
	#connection establishment
	conn = MySQLdb.connect(host="localhost",user="root",password="pass",db="mlcharts")
	return conn

def get_engine():
	engine = create_engine("mysql+mysqldb://root:pass"+"@localhost/mlcharts")
	return engine

def fill_missing_values(filename,cleaning_metrics,dividing_metrics,cid):
	conn=get_connection()
	cur=conn.cursor()
	dataframe_before = pd.read_csv(filename)
	for i in cleaning_metrics:
		if(cleaning_metrics[i] == 'mean'):
			dataframe_before[i].fillna(dataframe_before[i].mean(),inplace = True)
		elif(cleaning_metrics[i] == 'median'):
			dataframe_before[i].fillna(dataframe_before[i].median(),inplace = True)
		elif(cleaning_metrics[i] == 'mode'):
			dataframe_before[i].fillna(dataframe_before[i].mode,inplace = True)
		else:
			pass
	#getting type of metrics
	metrics=dividing_metrics['metrics']
	dic_metrics_type={'numerical_missing':[],'numerical_non_missing':[], 'non_numerical':[]}
	for i in metrics:
		if(dataframe_before[i].dtype == "int64" or dataframe_before[i].dtype == "float64"):
			count_of_null_values=list(dataframe_before[i].isnull()).count(False)
			if(count_of_null_values==0):
				dic_metrics_type['numerical_non_missing'].append(i)
			else:
				dic_metrics_type['numerical_missing'].append(i)
		else:
			dic_metrics_type['non_numerical'].append(i)
	#remove the columns
	for i in dividing_metrics['remove']:
		dataframe_before.drop([i],axis=1,inplace=True)
	#populate_filters_table
	for i in dividing_metrics['filters']:
		cur.execute("""INSERT INTO filters(name,row_status,cid) VALUES (%s,%s,%s)""",(i,1,cid))
	conn.commit()
	for i in dic_metrics_type['non_numerical']:
		cur.execute("""INSERT INTO filters(name,row_status,cid) VALUES (%s,%s,%s)""",(i,1,cid))
	conn.commit()
	for i in dic_metrics_type['numerical_missing']:
		cur.execute("""INSERT INTO metrics(name,row_status,cid) VALUES (%s,%s,%s)""",(i,1,cid))
	conn.commit()
	for i in dic_metrics_type['numerical_non_missing']:
		cur.execute("""INSERT INTO metrics(name,row_status,cid) VALUES (%s,%s,%s)""",(i,1,cid))
	conn.commit()
	table_name = get_file_name(filename,cid)
	engine = get_engine()
	dataframe_before.to_sql(con=engine, if_exists='replace', name=table_name,index=False)
	conn.close()

def get_box_chart(df):
	header = df.columns
	data = []
	for i in header:
		trace_name = i + '_'
		exec("%s = go.Box(y=%s,name='%s')"%(trace_name,df[i].tolist(),i))
		exec("data.append(%s)"%trace_name)
	layout = go.Layout(title="Box Plot Chart")
	figure = go.Figure(data=data, layout=layout)
	return py.plot(figure, auto_open=False, output_type='div')


def get_dist_plot(df):
	group_labels = list(df.columns)
	data=[]
	for i in group_labels:
		data.append(df[i].tolist())
	fig = ff.create_distplot(data,group_labels)
	return py.plot(fig, auto_open=False, output_type='div')

def get_scatter_plot(df):
	header = df.columns
	data = []
	for i in header:
		trace_name = i + '_'
		exec ("%s = go.Scatter(y=%s,name='%s',mode='markers')" % (trace_name, df[i].tolist(), i))
		exec ("data.append(%s)" % trace_name)
	layout = go.Layout(title="Box Plot Chart")
	figure = go.Figure(data=data, layout=layout)
	return py.plot(figure, auto_open=False, output_type='div')

def gen_charts(tablename,data,cid):
	conn = MySQLdb.connect(host="localhost", user="root", password="pass", db="mlcharts")
	cur = conn.cursor()
	dataframe_before = pd.read_sql('select name from metrics where cid=1', conn)
	metrics = list(set(list(dataframe_before['name'])))
	query = 'select '+ ",".join(metrics) + ' from ' + tablename
	l = []
	for i in data:
		s = i + "='" + str(data[i]) + "'"
	l.append(s)
	query = '{} WHERE {}'.format(query, ' AND '.join(l))
	dataframe_before = pd.read_sql(query, conn)
	div = get_box_chart(dataframe_before)
	div1 = get_dist_plot(dataframe_before)
	div2 = get_scatter_plot(dataframe_before)
	l = []
	l.append(div)
	l.append(div1)
	l.append(div2)
	return l

def get_filters(cid):
	conn = get_connection()
	cur = conn.cursor()

	## for fetching the filters from filters table having cid == cid ##
	query = """SELECT NAME FROM filters WHERE cid = """ + str(1)
	cur.execute(query)
	filters = [name[0] for name in cur.fetchall()]
	filters = ",".join(filters)

	## for fetching the company name from company table having cid == cid ##
	query = """SELECT name FROM company WHERE cid = """ + str(cid)
	cur.execute(query)
	company_name = cur.fetchall()[0][0]

	## for fetching all the table names in a database and getting the table name which has company_name as prefix ##
	query = "SELECT table_name FROM information_schema.tables where table_schema='mlcharts'"
	cur.execute(query)
	for table in cur.fetchall():
		if table[0].startswith(company_name + "_"):
			table_name = table[0]
			break

	## for fetching the filters data from the table data ##

	filters_data = pd.read_sql("SELECT " + filters + " FROM " + table_name, conn)

	## for generating the unique values from the filters data ##
	filters_unique_data = {}
	for col in filters_data:
		values = [val for val in list(filters_data[col].unique()) if pd.isnull(val) == False]
		filters_unique_data[col] = values

	filters_unique_data['tablename'] = table_name

	## closing the connection ##
	conn.close()
	return filters_unique_data

