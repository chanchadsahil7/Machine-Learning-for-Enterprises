## import statements  ##
import MySQLdb
import pandas as pd
import os
from sqlalchemy import create_engine
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff


## change these values according to your credentials for the database ##
username = "root"
pwd = "pass"
dbname = "mlcharts"

def get_columns(filename):
    ## returns the column names as a list ##
    filedata = pd.read_csv(filename)
    return list(filedata.columns.values)

def get_cid(email):
    ## retrieves and returns the company id using the email ##
    conn = get_connection()
    cur = conn.cursor()
    query = "select cid from admin where email="+ "'" + str(email) + "'"
    cur.execute(query)
    t = cur.fetchall()
    cid = t[0][0]
    return cid

def check_is_admin(email):
    conn = get_connection()
    cur = conn.cursor()
    query = "select cid from admin where email=" + "'" + str(email) + "'"
    cur.execute(query)
    t = cur.fetchall()
    if t:
        cid = t[0][0]
        return True
    return False

def get_numerical_metrics(filename,metrics):
    #getting type of metrics
    file_dt = pd.read_csv(filename)
    dic_metrics_type = {'numerical_missing':[],'numerical_non_missing':[], 'non_numerical':[]}
    for i in metrics:
        if(file_dt[i].dtype == "int64" or file_dt[i].dtype == "float64"):
            count_of_null_values=list(file_dt[i].isnull()).count(False)
            if(count_of_null_values == 0):
                dic_metrics_type['numerical_non_missing'].append(i)
            else:
                dic_metrics_type['numerical_missing'].append(i)
        else:
            dic_metrics_type['non_numerical'].append(i)
    return dic_metrics_type

def get_file_name(filename,cid):
    conn = get_connection()
    cur = conn.cursor()
    query = "Select name from company where cid="+str(cid)
    cur.execute(query)
    t = cur.fetchall()
    company_name = t[0][0]
    s = os.path.basename(filename)
    s = s.strip('.csv')
    table_name = company_name+'_'+s
    conn.close()
    return table_name

def get_connection():
    #connection establishment
    conn = MySQLdb.connect(host = "localhost",user = username,password = pwd,db = dbname)
    return conn

def get_engine():
    engine = create_engine("mysql+mysqldb://"+username+":"+pwd+"@localhost/"+dbname)
    return engine

def fill_missing_values(filename,cleaning_metrics,dividing_metrics,cid):
    conn = get_connection()
    cur = conn.cursor()
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
    metrics = dividing_metrics['metrics']
    dic_metrics_type = {'numerical_missing':[],'numerical_non_missing':[], 'non_numerical':[]}
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
    dataframe_before.to_sql(con = engine, if_exists = 'replace', name = table_name,index = False)
    conn.close()

def get_box_chart(df):
    header = df.columns
    data = []
    for i in header:
        trace_name = i + '_'
        exec("%s = go.Box(y=%s,name='%s')"%(trace_name,df[i].tolist(),i))
        exec("data.append(%s)"%trace_name)
    layout = go.Layout(title = "Box Plot Chart")
    figure = go.Figure(data = data, layout = layout)
    return py.plot(figure, auto_open = False, output_type = 'div')


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
        exec ("%s = go.Scatter(y = %s,name = '%s',mode = 'markers')" % (trace_name, df[i].tolist(), i))
        exec ("data.append(%s)" % trace_name)
    layout = go.Layout(title = "Scatter Chart")
    figure = go.Figure(data = data, layout = layout)
    return py.plot(figure, auto_open = False, output_type = 'div')

def get_density_chart(df):
    fig = ff.create_2d_density(df['Age'],df['HourlyRate'])
    return py.plot(fig, auto_open = False, output_type = 'div')

def get_bar_chart(df):
    header = df.columns
    data = []
    for i in header:
        trace_name = i + '_'
        exec ("%s = go.Bar(y = %s,name = '%s')" % (trace_name, df[i].tolist(), i))
        exec ("data.append(%s)" % trace_name)
    layout = go.Layout(title = "Bar Chart",barmode = 'stack')
    figure = go.Figure(data = data, layout = layout)
    return py.plot(figure, auto_open = False, output_type = 'div')

def gen_charts(tablename,data,cid):
    conn = get_connection()
    cur = conn.cursor()
    dataframe_before = pd.read_sql('select name from metrics where cid=%s'%(int(cid)), conn)
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
    div3 = get_bar_chart(dataframe_before)
    div4 = get_density_chart(dataframe_before)
    l = []
    l.append(div)
    l.append(div1)
    l.append(div2)
    l.append(div3)
    l.append(div4)
    return l

def get_filters(cid):
    conn = get_connection()
    cur = conn.cursor()

    ## for fetching the filters from filters table having cid == cid ##
    query = "SELECT NAME FROM filters WHERE cid = %s"%(int(cid))
    cur.execute(query)
    filters = [name[0] for name in cur.fetchall()]
    filters = ",".join(filters)

    ## for fetching the company name from company table having cid == cid ##
    query = "SELECT name FROM company WHERE cid = %s" %(int(cid))
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

