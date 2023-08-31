import pandas as pd
import json
import githubSettings
import extended_scraper
import os,time


def read_json_df(filename):
    jsonfile=open(filename,encoding="utf-8")
    obj=jsonfile.read()
    commitsJson=json.loads(obj)
    jsondf=pd.DataFrame(commitsJson)
    jsonfile.close()

    return jsondf

def read_excel_df(filename):
    df = pd.read_excel(filename,sheet_name=0)
    df=pd.DataFrame(df)
    return df


def read_keywords_list(path):
    with open(path) as wordfile:
        keywords_list = wordfile.read().splitlines()
    wordfile.close()

    return keywords_list

def get_timeline_repo(filepath,reposlug):
    indexOverall=0

    # for example, a json file storing all the repo slugs and the issue ids("issue_number") of the repo,
    jsonpath="D:\\UofT_Research\\forcolab\\jysun\\miscellaneous_data_scraping\\Example.json"
    repodf=read_json_df(jsonpath)

    currentrepo_timeline_dfs=[]


    for i in range(repodf.shape[0]):
        start_time=time.time()
        print(indexOverall)
        current_issue_number=repodf.iloc[i]['issue_number']

        current_timeline=gh_api.issue_pr_timeline(reposlug,int(current_issue_number))
        timeline_df=pd.DataFrame(current_timeline)
        timeline_df["repo_source"]=reposlug
        timeline_df["issue_number"]=current_issue_number
        timeline_df["issue_status"]="closed"
        currentrepo_timeline_dfs.append(timeline_df)
        indexOverall+=1
        end_time=time.time()
        times=round(end_time-start_time,2)
        print('total scraping time is{}s'.format(times))
        print(indexOverall)

    mergeddf=pd.concat(currentrepo_timeline_dfs,ignore_index=True)
    print(mergeddf)



#main 
if __name__ == '__main__':
    #save file path
    savefilepath="D:\\"

    # Your github tokens for using GithubAPI
    gh_api =extended_scraper.extendedScraper(githubSettings.tokens)


    # the list of repo slugs that you have already collected issues for. You can store the issues collected along with their repo slug into a json file.
    repo_list=['Nuri22/csDetector','repo_owner/repo_name2']
    
    for i in range(len(repo_list)):
        get_timeline_repo(savefilepath,repo_list[i])
