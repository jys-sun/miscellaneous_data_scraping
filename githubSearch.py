import threading
from time import ctime
from github import Github
import pandas as pd
import calendar
import time


def saveData(saveFilePath,dataList):   
    Mychart = pd.DataFrame(dataList)
    writer = pd.ExcelWriter(saveFilePath, engine='xlsxwriter')
    Mychart.to_excel(writer)
    writer.save()
    print("spreadsheet saved at :"+saveFilePath)

def scraping(token,searchKeyword,advancedQuery,outputFolder,saveFileIndex=''):
    """ token (str): github token for API requests
        searchKeyword (str): keywords used for github search as well as the output speadsheet name
        advancedQuery (str): additional filtering conditions for github search, since the returned result for github search is max 1000 repositories per request, it is better to set a time window for each request
        outputFolder (str): the folder path for the output spreadsheets
        saveFileIndex (str): used for indexing the speadsheet
    """
    indexOverall = 0
    g = Github(token,per_page=560,retry=8)
    SearchList ={"SearchKeyword":[],"IsOrgRepo":[],"OwnerName":[],"RepoName":[],"RepoSlug":[],"Language":[],"StarsCount":[],"ForksCount":[],
                "Description":[],"CreatedAt":[],"PushedAt":[],"IsFork":[]}
    repositories = g.search_repositories(query=searchKeyword+advancedQuery)

    for rItems in repositories:
        start_time=time.time()
        search_rate_limit = g.get_rate_limit().search
        remaining_limit = search_rate_limit.remaining
        print("remaining limit is :"+str(remaining_limit))
        print(search_rate_limit)
        if remaining_limit>2:            
            SearchList["SearchKeyword"].append(searchKeyword)
            SearchList["IsOrgRepo"].append(rItems.owner.type)
            SearchList["OwnerName"].append(rItems.owner.login)
            SearchList["RepoName"].append(rItems.name)
            SearchList["RepoSlug"].append(rItems.full_name)
            SearchList["Language"].append(rItems.language)
            SearchList["StarsCount"].append(rItems.stargazers_count)
            SearchList["ForksCount"].append(rItems.forks_count)
            SearchList["Description"].append(rItems.description)
            SearchList["CreatedAt"].append(rItems.created_at)
            SearchList["PushedAt"].append(rItems.pushed_at)
            SearchList["IsFork"].append(rItems.fork)
            indexOverall+=1
        else:
            reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 5  #  wait 5 more seconds 
            time.sleep(sleep_time)
        end_time=time.time()
        times=round(end_time-start_time,2)
        print('total scraping time is{}s'.format(times))
        print(indexOverall)

    saveData(outputFolder+searchKeyword+saveFileIndex+'.xlsx',SearchList)
    print("scraping completed for "+searchKeyword+saveFileIndex)



if __name__ == '__main__':

    threads = []
    t1 = threading.Thread(target=scraping,args=("my token1", 'mediacal imaging software','in:readme language:c++ forks:>10','C:\\Users\\myAccount\\Desktop\\','_01'))
    t2 = threading.Thread(target=scraping,args=("my token2", 'neuroscience software','in:readme language:c++ forks:>10','C:\\Users\\myAccount\\Desktop\\','_01'))

    threads.append(t1)
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()
    
    for t in threads:
         t.join() 

    print ("all threads completed %s" %ctime())