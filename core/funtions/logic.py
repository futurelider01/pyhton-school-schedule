import pandas as pd
from datetime import datetime
import os

PARENT = os.getcwd()
LOG_PATH = f'./core/logging.csv'

jadval = pd.read_excel(f'./core/source/all_jadval.xlsx',header=[0,1,2])
WEEK=('Dushanba', 'Seshanba','Chorshanba', 'Payshanba', 'Juma', 'Shanba','Hammasi')
SINFLAR = ['10C', '9A',  '5B', '11B', '9C','9O', '5A', '7A', '6A', '8C', '6B', '7C', '10A', '10O','11A', '8A','10B']

teachers = jadval['Teachers']['Unnamed: 1_level_1']['Unnamed: 1_level_2']
TEACHERS = teachers.to_list()

def today_():
    today=datetime.now().weekday()+1
    d={1:'Dushanba',2:"Seshanba",3:"Chorshanba",4:"Payshanba",5:"Juma",6:"Shanba",7:"Yakshanba"}
    return d[today]

def get_grade(chat_id):
    log = pd.read_csv(LOG_PATH)
    sinf = log[log['chat_id']==int(chat_id)]['sinf']
    return sinf.values[0]

def get_role(chat_id):
    log = pd.read_csv(LOG_PATH)
    sinf = log[log['chat_id']==int(chat_id)]['role']
    return sinf.values[0]
def get_name(chat_id):
    log = pd.read_csv(LOG_PATH)
    sinf = log[log['chat_id']==int(chat_id)]['name']
    return sinf.values[0]

def modify_data4teachers(data):
    if len(data)>2:
        res = f"{data[0]} siz uchun bir haftalik dars jadvali:\n"
        for i in data[1:]:
            temp=f'{i[0]}\n'
            for soat, sinf in i[1:]:
                temp+=f"{soat}-soatda {sinf} sinf\n"
            res+=temp+'\n'
        
    else:
        res = f"{data[0]} siz uchun {data[1][0]} kungi dars jadvali:\n"
        for soat, sinf in data[1][1:]:
            res+=f"{soat}-soat {sinf} sinf\n"
    return res

def get_classes_for_teacher(teacher_name: str, day_of_week=None, flag=False, classes: list=[]):
    data = []
    if flag:
        data = [teacher_name]
    if day_of_week is not None:
        day_with_lessons=[day_of_week]
        
        for i in range(1,8):
            try:
                d=jadval[teachers==teacher_name][day_of_week][f"{i}-soat"]['sinf'].dropna().to_list()
                if d!=[]:
                    d.insert(0,i)
                    day_with_lessons.append(tuple(d))
            except:pass

        classes.append(tuple(day_with_lessons))
    
        data.append(tuple(day_with_lessons))
        # print(data)
        return data
    
    if day_of_week is None:
        data = [teacher_name]
        for day in WEEK:
            
            var = get_classes_for_teacher(teacher_name, day)
            data.append(var[0])
    # print(data)
    return data

# ----------------------------------------------------------------------------------------------------#

def modify_data4pupils(data: pd.DataFrame):
    if isinstance(data, pd.DataFrame):
        subjects = data['Subject'].unique()
        subjects_num=[]
        for i,sub in enumerate(subjects,1):
            subjects_num.append([i, sub])
        subjects_num = pd.DataFrame(subjects_num, columns=['num','Subject'])
        merged =  pd.merge(subjects_num, data, on='Subject')
        res=''
        for row in merged.values:
            res+=f"{row[3]}. {row[0]}-soat {row[1]}. Ustoz: {row[2]}. {row[4]}-xona\n"
        return res
    return data

def get_classes_for_pupil(sinf_param, day_of_week):
    pd.options.mode.copy_on_write = True
    schedule = pd.DataFrame(columns=['Subject','Teacher','sinf','xona'], dtype='str')
    for i in range(1,8):
        try:
            try:
                jadval[day_of_week]
            except KeyError as e:
                return f"Hafta kunini to'g'ri kiriting!\nError with '{day_of_week}'"
            
            sinf_xona = jadval[day_of_week][f'{i}-soat']

            mask = sinf_xona['sinf'].fillna('0').str.contains(sinf_param)

            teach_sub = jadval[mask][['Teachers','Subject']]
            teach_sub['id'] = teach_sub.index
        
            res = sinf_xona[mask]
            res['id'] = res.index
            if not res.empty:
                a=pd.concat([teach_sub,res],axis=1)
                a=a.rename(columns={('Teachers', 'Unnamed: 1_level_1', 'Unnamed: 1_level_2'):'Teacher',
                                        ('Subject', 'Unnamed: 2_level_1', 'Unnamed: 2_level_2'): 'Subject'})
                filtered_data = a[['Subject','Teacher','sinf','xona']]
                if not schedule.empty:
                    schedule = pd.concat([schedule, filtered_data] , axis=0)
                else:
                    schedule = filtered_data.copy()
        except:
            pass
    schedule['xona'] = schedule['xona'].astype('int').astype('str')
    schedule=schedule.reset_index(drop=True)
    if schedule.empty:
        return f'{sinf_param}-sinf uchun jadval Topilmadi.\nSinfingizni qaytadan to\'g\'ri kiriting.'
        
    return schedule

def all_ids():
    df = pd.read_csv(LOG_PATH)
    return df['chat_id'].to_list()


if __name__=="__main__":
    teacher_name='Aldebayev Asqar'
    day_of_week = 'Payshanba'
    all_lessons = get_classes_for_teacher(teacher_name,day_of_week, flag=True)
    # print(all_lessons)
    # print(modify_data4teachers(all_lessons))
    res=get_classes_for_pupil('10-O','Chorshanba')
    # res=modify_data4pupils(res)
    print(res)