import sys
import csv
import datetime 
from Levenshtein import distance
import math

input_file = csv.DictReader(open(sys.argv[1]))
res = []
for row in input_file:
    res.append(dict(row))


def key_function(item_dictionary):
    '''Extract datetime string from given dictionary, and return the parsed datetime object'''
    datetime_string = item_dictionary['StockDate']
    return datetime.datetime.strptime(datetime_string, '%d-%b-%Y')
res.sort(key=key_function)

def company_match(res):
    company_name = input("Welcome Agent! Which stock you need to process? ")
    if not company_name:
        print("please enter the company name")
        return company_match(res)
    company_data = []
    for data in res:
        if distance(company_name, data['StockName']) == 1:
            near_company =  input("Oops! Do you mean "+data['StockName']+" ? y or n ")
            if near_company.lower() == 'y':
                company_name = data['StockName']
        if company_name == data['StockName']:
            company_data.append(data)
    print('\n')
    return company_data


def input_start_date(res):
    try:
        start_date = input("From which date you want to start ") 
        formated_start_date = datetime.datetime.strptime(start_date, '%d-%b-%Y')
        if formated_start_date < datetime.datetime.strptime(res[0]['StockDate'], '%d-%b-%Y'):
            print("your start date is not in range please enter a date between data")
            return input_start_date(res)
    except:
        print("Bad input for date. please input a right date ")
        return input_start_date(res)
    print('\n')
    return formated_start_date


def input_till_date(res,start_date_delta):
    try:
        till_date = input("Till which date you want to analyze ") 
        formated_till_date = datetime.datetime.strptime(till_date, '%d-%b-%Y')
        if formated_till_date < datetime.datetime.strptime(res[0]['StockDate'], '%d-%b-%Y') or formated_till_date < start_date_delta:
            print("your end date is less than range or finish is less than start please enter a date between range")
            return input_till_date(res,start_date_delta)
    except:
        print("Bad input for date. please input a right date ")
        return input_till_date(res,start_date_delta)
    print('\n')
    return formated_till_date


def company_need_data(company_data):
    need_data = []
    for parse_data in company_data:
        if datetime.datetime.strptime(parse_data['StockDate'], '%d-%b-%Y') <= till_date_delta or datetime.datetime.strptime(parse_data['StockDate'], '%d-%b-%Y') >= start_date_delta:
            need_data.append(parse_data)
    return need_data


def maxDiff(list_item, list_length): 
    if list_length == 1:
        return 1,0,(float(list_item[1]['StockPrice']) - float(list_item[0]['StockPrice'])) 

    max_diff = float(list_item[1]['StockPrice']) - float(list_item[0]['StockPrice'])  
    min_element = float(list_item[0]['StockPrice']) 
      
    for i in range( 1, list_length ): 
        j = 0
        if (float(list_item[i]['StockPrice']) - min_element > max_diff): 
            max_diff = float(list_item[i]['StockPrice']) - min_element 
            
        if (float(list_item[i]['StockPrice']) < min_element): 
            min_element = float(list_item[i]['StockPrice']) 
            j = i
      
    return j,i,max_diff 


def cal_mean(need_data,length):
    counter = 0
    mean = 0
    while counter <length -1:
        mean += float(need_data[counter]['StockPrice'])*((datetime.datetime.strptime(need_data[counter+1]['StockDate'], '%d-%b-%Y') - datetime.datetime.strptime(need_data[counter]['StockDate'], '%d-%b-%Y')).days) 
        counter+=1
    if datetime.datetime.strptime(need_data[length-1]['StockDate'], '%d-%b-%Y') <= till_date_delta:
        diff_date = (till_date_delta - datetime.datetime.strptime(need_data[length-1]['StockDate'], '%d-%b-%Y')).days
        mean+= float(need_data[length-1]['StockPrice'])*diff_date
    return (mean)/(length+diff_date)


def cal_std(need_data,length,mean):
    counter = 0
    std = 0
    while counter <length -1:
        std += float((float(mean-float(need_data[counter]['StockPrice']))**2)*((datetime.datetime.strptime(need_data[counter+1]['StockDate'], '%d-%b-%Y') - datetime.datetime.strptime(need_data[counter]['StockDate'], '%d-%b-%Y')).days))   
        counter+=1

    if datetime.datetime.strptime(need_data[length-1]['StockDate'], '%d-%b-%Y') <= till_date_delta:
        diff_date = (till_date_delta - datetime.datetime.strptime(need_data[length-1]['StockDate'], '%d-%b-%Y')).days
        std += ((mean - float(need_data[length-1]['StockPrice']))**2)*diff_date
    return math.sqrt(std/(length+diff_date))

while True:
    company_data = company_match(res)
    start_date_delta = input_start_date(res)
    till_date_delta = input_till_date(res,start_date_delta)
    need_data = company_need_data(company_data)
    length = len(need_data)
    mean = cal_mean(need_data,length)
    std = cal_std(need_data,length,mean)
    buy_date,sell_date,profit = maxDiff(need_data,length)
    print('Mean: {}, Std: {}, Buy date: {}, Sell date: {}, Profit {}'.format(mean, std,need_data[buy_date]['StockDate'],need_data[sell_date]['StockDate'],profit*100))
    print('\n')
    process = input("Do you want to continue? (y or n) ")
    if process == 'n':
        break
