import os
import requests as r

def urs_authenticate():
    # AUTHENTICATION CONFIGURATION
    from netrc import netrc
    from subprocess import Popen
    from getpass import getpass

    urs = 'urs.earthdata.nasa.gov'    # Earthdata URL to call for authentication
    prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
               'Enter NASA Earthdata Login Password: ']

    # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
    try:
        netrcDir = os.path.expanduser("~/.netrc")
        netrc(netrcDir).authenticators(urs)[0]
        del netrcDir

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        homeDir = os.path.expanduser("~")
        Popen('touch {0}.netrc | chmod og-rw {0}.netrc | echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
        Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
        Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)
        del homeDir

    # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        homeDir = os.path.expanduser("~")
        Popen('echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
        Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
        Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)
        del homeDir
    del urs, prompts

    
def simple_hls_stac_search(bbox, date_time = "2020-10-01T00:00:00Z/2020-10-31T23:31:12Z"):
    stac = 'https://cmr.earthdata.nasa.gov/stac/' # CMR-STAC API Endpoint
    stac_response = r.get(stac).json()            # Call the STAC API endpoint
    stac_lp = [s for s in stac_response['links'] if 'LP' in s['title']]  
    lp_cloud = r.get([s for s in stac_lp if s['title'] == 'LPCLOUD'][0]['href']).json()
    lp_links = lp_cloud['links']
    
    lp_search = [l['href'] for l in lp_links if l['rel'] == 'search'][0]  # Define the search endpoint
    
    lim = 100
    search_query = f"{lp_search}?&limit={lim}"    # Add in a limit parameter to retrieve 100 items at a time.
    search_query2 = f"{search_query}&bbox={bbox}"  # Add bbox to query
    #Sdate_time = "2020-10-01T00:00:00Z/2020-10-31T23:31:12Z"  # Define start time period / end time period
    search_query3 = f"{search_query2}&datetime={date_time}"  # Add to query that already includes bounding_box
    search_response = r.get(search_query3).json()            
    print(f"{len(search_response['features'])} items found!") 
    FEATURES = search_response['features']
    return (FEATURES)
