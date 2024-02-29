import polars as pl
import requests
from prefect import flow, task
from prefect.blocks.system import Secret

@task
def get_data():
    user = 'rgriffiths@extensiv.com'
    secret_block = Secret.load("jira-api-token")
    pwd = secret_block.get()
    query = 'issuetype = Bug AND priority in (P3-30, P3-60) order by created DESC'
    url = f'https://3plcentral.atlassian.net/rest/api/2/search?maxResults=200&jql={query}'
    r=requests.get(url,auth=(user,pwd)).json()
    rows = []

    for issue in r['issues']:
        key = f"'{issue['key']}'" 
        issue_type = f"'{issue['fields']['issuetype']['name']}'" 
        summary = f"'{issue['fields']['summary']}'".replace("'","")
        summary = f"'{summary}'"
        priority = f"'{issue['fields']['priority']['name']}'"
        product = issue['fields']['customfield_11612']
        if product:
            product=f"'{product['value']}'"
        comp=[]
        for component in issue['fields']['components']:
            comp.append(component['name'])
        component = ', '.join(comp)
        component = f"'{component}'" 
        created = f"'{issue['fields']['created']}'"
        sla_escalation = f"'{issue['fields']['customfield_11647']}'"
        resolved = f"'{issue['fields']['resolutiondate']}'"
        due = f"'{issue['fields']['customfield_11685']}'"
        status = f"'{issue['fields']['status']['name']}'"
        if not product:
            product='Null'
        if sla_escalation == "'None'":
            sla_escalation = 'Null'
        if resolved == "'None'":
            resolved = 'Null'
        if due == "'None'":
            due = 'Null'

        row = {'issue_type':issue_type,'key':key,'summary':summary,'priority':priority,'product':product,'component':component,'created':created,'sla_escalation':sla_escalation, 'resolved':resolved, 'due':due, 'status':status}
        rows.append(row)
        df = pl.DataFrame(rows)
    return df


@flow
def main():
    print(get_data())

if __name__ == main():
    main()