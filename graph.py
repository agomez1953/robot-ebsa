import json
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
def download_token():
    transport = AIOHTTPTransport('http://45.33.14.152:5010/graphql/')
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        '''
    mutation {
    signIn( payload:{
        user:"APERALTA"
        password:"xhksnbwj"
        id:"2"
    }){
        token
    }
    }
    '''
    )

    # Execute the query on the transport
    result = client.execute(query)
    result = str(result)
    file = open(file='token.txt', mode='w')
    file.write(result)
    file.close()

def read_header():
    download_token()
    header_full = open(file='token.txt', mode='r')
    txt_header = header_full.read()
    header_full.close
    txt_header = txt_header.replace("'", '"')
    txt_header = json.loads(txt_header)
    return txt_header['signIn']['token']
def get_info_marketer():
    token = read_header()
    header = {'Authorization': f'Bearer {token}'}
    transport = AIOHTTPTransport('http://45.33.14.152:5000/graphql/', header)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query_get_ebsa = gql(
        '''
        query {
  billPendingsForDownload(
    company_id: "cqsr41u0003jotggodd8r0b"
    date: "2021-11-18T00:00:00.000Z"
    marketer_id: "cqsyel2038rp7tgt7nwm75y"
  ) {
    account_id
    account_name
    company_id
    
  }
}# Write your query or mutation here
            '''    )
    result = client.execute(query_get_ebsa)
    return result['billPendingsForDownload']


if __name__ == '__main__':
    a = get_info_marketer()
    print(a)


